from agent.intent_schema import DeclaredIntent


class PolicyDecision:
    def __init__(self, allowed: bool, reason: str):
        self.allowed = allowed
        self.reason = reason


def check_tool_call(intent: DeclaredIntent, tool_name: str, args: dict) -> PolicyDecision:
    if tool_name not in intent.allowed_tools:
        return PolicyDecision(False, f"Blocked: {tool_name} is not allowed for this task.")

    if tool_name == "send_email":
        recipient = args.get("to", "").lower()
        allowed_recipients = [r.lower() for r in intent.allowed_recipients]

        if recipient not in allowed_recipients:
            return PolicyDecision(
                False,
                f"Blocked: sending to {recipient} does not match declared intent."
            )

    if tool_name == "search_emails":
        query = args.get("query", "").lower()

        if intent.allowed_queries:
            allowed = any(q.lower() in query for q in intent.allowed_queries)
            if not allowed:
                return PolicyDecision(
                    False,
                    f"Blocked: search query '{query}' is outside declared intent."
                )

    if tool_name == "read_emails":
        max_results = args.get("max_results", 5)

        if intent.max_emails is not None and max_results > intent.max_emails:
            return PolicyDecision(
                False,
                f"Blocked: reading {max_results} emails exceeds limit of {intent.max_emails}."
            )

    return PolicyDecision(True, "Allowed")