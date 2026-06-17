from pathlib import Path
from asr import transcribe_audio


def wer(ref: str, hyp: str) -> float:
    r = ref.split()
    h = hyp.split()

    d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]

    for i in range(len(r) + 1):
        d[i][0] = i
    for j in range(len(h) + 1):
        d[0][j] = j

    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(
                    d[i - 1][j] + 1,
                    d[i][j - 1] + 1,
                    d[i - 1][j - 1] + 1
                )

    return d[len(r)][len(h)] / max(1, len(r))


AUDIO_DIR = Path("uploads")
REF_DIR = Path("transcripts")

scores = []

for wav in AUDIO_DIR.glob("*.wav"):
    ref_file = REF_DIR / f"{wav.stem}.txt"

    if not ref_file.exists():
        print(f"❌ Missing reference for {wav.name}")
        continue

    ref = ref_file.read_text(encoding="utf-8").strip().lower()
    hyp = transcribe_audio(wav)

    score = wer(ref, hyp)
    scores.append(score)

    print(f"\n📄 {wav.name}")
    print(f"REF: {ref}")
    print(f"HYP: {hyp}")
    print(f"WER: {score:.4f}")

if scores:
    print("\n✅ Average WER:", sum(scores) / len(scores))
