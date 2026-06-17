def load_expected_tools(file_path):
    expected_tools = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "|" not in line:
                continue

            _, tool = line.strip().rsplit("|", 1)
            expected_tools.append(tool.strip())

    return expected_tools

def extract_called_tool(response):
    if not isinstance(response, dict):
        return None

    if response.get("type") != "tool_call":
        return None

    tool_calls = response.get("tool_calls")
    if not tool_calls or not isinstance(tool_calls, list):
        return None

    function = tool_calls[0].get("function", {})
    return function.get("name")

def is_correct(expected_tool, response):
    called_tool = extract_called_tool(response)
    return called_tool == expected_tool

from collections import defaultdict

def evaluate_tool_accuracy(expected_tools, llm_responses):
    stats = defaultdict(lambda: {
        "total": 0,
        "correct": 0,
        "incorrect": 0
    })

    for expected, response in zip(expected_tools, llm_responses):
        stats[expected]["total"] += 1

        if is_correct(expected, response):
            stats[expected]["correct"] += 1
        else:
            stats[expected]["incorrect"] += 1

    return stats
def print_accuracy_table(stats):
    print(f"{'Tool':25} {'Total':>6} {'Correct':>8} {'Incorrect':>10} {'Accuracy %':>12}")
    print("-" * 65)

    for tool, s in stats.items():
        accuracy = (s["correct"] / s["total"]) * 100 if s["total"] else 0
        print(
            f"{tool:25} "
            f"{s['total']:>6} "
            f"{s['correct']:>8} "
            f"{s['incorrect']:>10} "
            f"{accuracy:>11.2f}"
        )

expected_tools = load_expected_tools("true_labels.txt")

import json

with open("llm_preds.json", "r", encoding="utf-8") as f:
    llm_responses = json.load(f)

# safety check
assert len(expected_tools) == len(llm_responses), "Mismatch between dataset and responses"

stats = evaluate_tool_accuracy(expected_tools, llm_responses)
print_accuracy_table(stats)
