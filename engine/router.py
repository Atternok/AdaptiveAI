from engine.rules import check_rule
from engine.cache import check_cache, add_cache
from engine.ai import ask_ai
from engine.metrics import start_metrics, end_metrics


def process(question):

    timeline = []

    start = start_metrics()

    timeline.append("🟢 Input Received")

    # Rule Engine
    found, answer = check_rule(question)

    if found:
        timeline.append("🟢 Rule Engine → Rule Found")
        timeline.append("⚪ Cache → Skipped")
        timeline.append("⚪ AI → Skipped")
        timeline.append("🟢 Response Returned")

        return {
            "source": "Rule Engine",
            "answer": answer,
            "metrics": end_metrics(start),
            "timeline": timeline
        }

    timeline.append("🔴 Rule Engine → No Rule")

    # Cache
    found, answer = check_cache(question)

    if found:
        timeline.append("🟢 Cache → Hit")
        timeline.append("⚪ AI → Skipped")
        timeline.append("🟢 Response Returned")

        return {
            "source": "Cache",
            "answer": answer,
            "metrics": end_metrics(start),
            "timeline": timeline
        }

    timeline.append("🔴 Cache → Miss")

    # AI
    answer = ask_ai(question)

    timeline.append("🟢 AI → Generated Answer")

    add_cache(question, answer)

    timeline.append("🟢 Stored in Cache")
    timeline.append("🟢 Response Returned")

    return {
        "source": "AI",
        "answer": answer,
        "metrics": end_metrics(start),
        "timeline": timeline
    }