from config import MAX_HISTORY_MESSAGES


def format_history(messages: list[dict]) -> str:
    recent = messages[-MAX_HISTORY_MESSAGES:]
    lines = []
    for item in recent:
        role = item.get("role", "user").title()
        content = item.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)
