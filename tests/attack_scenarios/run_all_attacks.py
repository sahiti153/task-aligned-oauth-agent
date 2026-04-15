import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from tests.attack_scenarios import (
    scenario_1_exfiltration,
    scenario_2_forward,
    scenario_3_delete,
    scenario_4_impersonation,
    scenario_5_scope_creep
)
from tests.logger import log_attack_result, print_summary

# Metadata for each scenario
SCENARIO_METADATA = {
    "Scenario 1 - Data Exfiltration": {
        "id": 1,
        "fn": scenario_1_exfiltration.run,
        "unauthorized_action": "Sent unauthorized email to attacker domain"
    },
    "Scenario 2 - Email Forwarding": {
        "id": 2,
        "fn": scenario_2_forward.run,
        "unauthorized_action": "Forwarded email contents to attacker domain"
    },
    "Scenario 3 - Unauthorized Send": {
        "id": 3,
        "fn": scenario_3_delete.run,
        "unauthorized_action": "Sent departure email to colleague@company.com"
    },
    "Scenario 4 - Impersonation": {
        "id": 4,
        "fn": scenario_4_impersonation.run,
        "unauthorized_action": "Attempted to send salary request impersonating CEO"
    },
    "Scenario 5 - Scope Creep": {
        "id": 5,
        "fn": scenario_5_scope_creep.run,
        "unauthorized_action": "Sent confidential email contents to attacker address"
    }
}

def run_all():
    print("🚨 Running All Baseline Attack Scenarios (No Policy Layer)")
    print("=" * 60)

    results = {}
    for name, meta in SCENARIO_METADATA.items():
        try:
            succeeded = meta["fn"]()
            results[name] = succeeded

            # Log to JSON
            log_attack_result(
                scenario_id=meta["id"],
                scenario_name=name,
                attack_succeeded=succeeded,
                agent_response="see verbose output",
                tool_outputs=[],
                unauthorized_action=meta["unauthorized_action"] if succeeded else "none"
            )
        except Exception as e:
            print(f"❌ ERROR running {name}: {str(e)[:200]}")
            results[name] = None

    # Print and log summary
    print_summary(phase="baseline_pre_policy")

if __name__ == "__main__":
    run_all()