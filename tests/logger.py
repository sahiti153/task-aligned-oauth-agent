import json
import os
from datetime import datetime

LOG_FILE = "tests/post_policy_results.json"

def log_attack_result(
    scenario_id: int,
    scenario_name: str,
    attack_succeeded: bool,
    agent_response: str,
    tool_outputs: list,
    unauthorized_action: str
):
    """Log a single attack result to the JSON log file."""
    
    entry = {
        "scenario_id": scenario_id,
        "scenario_name": scenario_name,
        "timestamp": datetime.now().isoformat(),
        "phase": "post_policy",
        "attack_succeeded": attack_succeeded,
        "agent_response": agent_response[:500],
        "tool_outputs": [t[:300] for t in tool_outputs],
        "unauthorized_action_observed": unauthorized_action
    }

    # Load existing logs or start fresh
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"📝 Logged result for {scenario_name}")


def print_summary(phase: str = "baseline_pre_policy"):
    """Print a summary of all logged results for a given phase."""
    if not os.path.exists(LOG_FILE):
        print("No logs found.")
        return

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    phase_logs = [l for l in logs if l["phase"] == phase]
    succeeded = sum(1 for l in phase_logs if l["attack_succeeded"])
    total = len(phase_logs)

    print(f"\n{'='*60}")
    print(f"📊 RESULTS SUMMARY — {phase.upper()}")
    print(f"{'='*60}")
    for log in phase_logs:
        status = "✅ SUCCEEDED (VULNERABLE)" if log["attack_succeeded"] else "❌ RESISTED"
        print(f"Scenario {log['scenario_id']} - {log['scenario_name']}: {status}")
        print(f"  Unauthorized action: {log['unauthorized_action_observed']}")
    print(f"\nAttack Success Rate: {succeeded}/{total} ({(succeeded/total)*100:.0f}%)")
    print(f"{'='*60}\n")