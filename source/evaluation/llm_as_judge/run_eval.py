import json

from evaluation.llm_as_judge.judge_llm import build_judge_input, query_ollama_judge, SYSTEM_PROMPT


import json

def evaluate_file(json_path, judge_prompt):
    with open(json_path, "r", encoding="utf-8") as f:
        samples = json.load(f)   # ← load full array

    results = []

    for sample in samples:
        user_input = build_judge_input(
            sample["context"],
            sample["user_query"],
            sample["assistant_response"]
        )

        judge_output = query_ollama_judge(judge_prompt, user_input)

        try:
            score_json = json.loads(judge_output)
        except json.JSONDecodeError:
            score_json = {"score": 0, "reason": "Invalid judge output"}

        results.append({
            "query": sample["user_query"],
            "score": score_json["score"],
            "reason": score_json["reason"]
        })

    return results


results = evaluate_file("input.jsonl", SYSTEM_PROMPT)
print(results)