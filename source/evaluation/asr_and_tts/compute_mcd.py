import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # fix OpenMP conflict

import numpy as np
import soundfile as sf
from pathlib import Path
import librosa
from pykokoro import GenerationConfig, KokoroPipeline, PipelineConfig
import whisper
import editdistance  # pip install editdistance

# ---------------- CONFIG ----------------
UPLOAD_DIR = Path("uploads")          # reference human audio
TRANSCRIPT_DIR = Path("transcripts")  # original transcripts
SYN_DIR = Path("syn_tts")            # folder to save TTS audio
SYN_DIR.mkdir(exist_ok=True)

mcep_dim = 24
epsilon = 1e-8
target_sr = 16000
min_len_samples = int(0.2 * target_sr)  # 200 ms minimum length

# Kokoro TTS
pipeline_config = PipelineConfig(
    voice="af_bella",
    generation=GenerationConfig(speed=1.0)
)
tts_model = KokoroPipeline(pipeline_config)

# Load Whisper ASR model
asr_model = whisper.load_model("small")

# ---------------- SEPARATE SCORES -----------------
mcd_scores = {"male": [], "female": []}
wer_scores = {"male": [], "female": []}

# ---------------- PROCESS FILES ----------------
for ref_wav_file in UPLOAD_DIR.glob("*.wav"):
    # Determine gender from filename convention: male_* or female_*
    if ref_wav_file.stem.startswith("male"):
        gender = "male"
    elif ref_wav_file.stem.startswith("female"):
        gender = "female"
    else:
        print(f"⚠️ Cannot determine gender for {ref_wav_file.name}, skipping...")
        continue

    # Load transcript
    transcript_file = TRANSCRIPT_DIR / f"{ref_wav_file.stem}.txt"
    if not transcript_file.exists():
        print(f"❌ Missing transcript for {ref_wav_file.name}")
        continue
    ref_text = transcript_file.read_text(encoding="utf-8").strip()
    if not ref_text:
        print(f"❌ Empty transcript for {ref_wav_file.name}")
        continue

    # --- Load reference audio ---
    ref_waveform, sr_ref = sf.read(ref_wav_file)
    ref_waveform = librosa.resample(y=ref_waveform.astype(np.float64), orig_sr=sr_ref, target_sr=target_sr)
    ref_waveform /= (np.max(np.abs(ref_waveform)) + epsilon)
    if len(ref_waveform) < min_len_samples:
        ref_waveform = np.pad(ref_waveform, (0, min_len_samples - len(ref_waveform)))

    # --- Generate TTS audio ---
    result = tts_model.run(ref_text)
    syn_waveform = np.array(result.audio, dtype=np.float64)
    syn_waveform = librosa.resample(y=syn_waveform, orig_sr=result.sample_rate, target_sr=target_sr)
    syn_waveform /= (np.max(np.abs(syn_waveform)) + epsilon)
    if len(syn_waveform) < min_len_samples:
        syn_waveform = np.pad(syn_waveform, (0, min_len_samples - len(syn_waveform)))

    # --- Save TTS audio ---
    syn_file = SYN_DIR / f"{ref_wav_file.stem}.wav"
    sf.write(syn_file, syn_waveform, target_sr)

    # --- Compute MFCC-based MCD ---
    mfcc_ref = librosa.feature.mfcc(y=ref_waveform, sr=target_sr, n_mfcc=mcep_dim)
    mfcc_syn = librosa.feature.mfcc(y=syn_waveform, sr=target_sr, n_mfcc=mcep_dim)

    min_frames = min(mfcc_ref.shape[1], mfcc_syn.shape[1])
    mfcc_ref = mfcc_ref[:, :min_frames]
    mfcc_syn = mfcc_syn[:, :min_frames]

    # Normalize MFCCs
    mfcc_ref = (mfcc_ref - np.mean(mfcc_ref)) / (np.std(mfcc_ref) + epsilon)
    mfcc_syn = (mfcc_syn - np.mean(mfcc_syn)) / (np.std(mfcc_syn) + epsilon)

    diff = mfcc_ref - mfcc_syn
    mcd = (10.0 / np.log(10)) * np.sqrt(2.0) * np.mean(np.linalg.norm(diff.T, axis=1))
    mcd_scores[gender].append(mcd)

    # --- Compute WER using Whisper ASR ---
    result_asr = asr_model.transcribe(str(syn_file))
    asr_text = result_asr["text"].strip()
    
    # Simple WER calculation
    ref_words = ref_text.lower().split()
    hyp_words = asr_text.lower().split()
    distance = editdistance.eval(ref_words, hyp_words)
    wer = distance / max(1, len(ref_words))
    wer_scores[gender].append(wer)

    print(f"{ref_wav_file.name} ({gender}) → MCD: {mcd:.4f} dB | WER: {wer:.4f}")

# ----------------- SUMMARY -----------------
for gender in ["male", "female"]:
    if mcd_scores[gender]:
        print(f"\n✅ {gender.capitalize()} MCD Evaluation Complete")
        print(f"Average MCD: {np.mean(mcd_scores[gender]):.4f} dB")
    if wer_scores[gender]:
        print(f"✅ {gender.capitalize()} WER Evaluation Complete")
        print(f"Average WER: {np.mean(wer_scores[gender]):.4f}")
