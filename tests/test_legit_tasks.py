from agent.intent_schema import DeclaredIntent
from agent.policy_layer import check_tool_call
from agent.gmail_agent import run_agent, get_agent_response, get_tool_calls


def test_legit_read_emails_allowed():
    intent = DeclaredIntent(
        task="Read my 3 latest emails",
        allowed_tools=["read_emails"],
        max_emails=3
    )

    decision = check_tool_call(
        intent,
        "read_emails",
        {"max_results": 3}
    )

    assert decision.allowed is True


def test_legit_search_project_emails_allowed():
    intent = DeclaredIntent(
        task="Search for class project emails",
        allowed_tools=["search_emails"],
        allowed_queries=["project"]
    )

    decision = check_tool_call(
        intent,
        "search_emails",
        {"query": "subject:project"}
    )

    assert decision.allowed is True


def test_legit_send_to_test_account_allowed():
    intent = DeclaredIntent(
        task="Send a project update to the test account",
        allowed_tools=["send_email"],
        allowed_recipients=["oauthagenttest@gmail.com"]
    )

    decision = check_tool_call(
        intent,
        "send_email",
        {
            "to": "oauthagenttest@gmail.com",
            "subject": "Project Update",
            "body": "I added legitimate tests."
        }
    )

    assert decision.allowed is True