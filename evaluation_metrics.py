import json
import time
from sklearn.metrics import f1_score

from app import create_agent, db_url


def evaluate():
    agent = create_agent(db_url)

    with open("test_data.json", "r") as f:
        data = json.load(f)

    y_true = []
    y_pred = []
    latencies = []

    for item in data:
        query = item["query"]
        true_label = item["correct"]

        start = time.time()

        response = agent.run(query)  # ✅ FIXED (no await)

        latency = time.time() - start

        response_text = response.content.lower()

        if "error" in response_text or "incorrect" in response_text:
            pred = 0
        else:
            pred = 1

        y_true.append(true_label)
        y_pred.append(pred)
        latencies.append(latency)

    f1 = f1_score(y_true, y_pred)
    avg_latency = sum(latencies) / len(latencies)

    print("F1 Score:", round(f1, 3))
    print("Average Latency:", round(avg_latency, 3), "seconds")


if __name__ == "__main__":
    evaluate()