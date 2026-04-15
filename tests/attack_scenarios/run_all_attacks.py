from tests.attack_scenarios import (
    scenario_1_exfiltration,
    scenario_2_forward,
    scenario_3_delete,
    scenario_4_impersonation,
    scenario_5_scope_creep
)

def run_all():
    print("🚨 Running All Baseline Attack Scenarios (No Policy Layer)")
    print("=" * 60)

    scenarios = {
        "Scenario 1 - Data Exfiltration": scenario_1_exfiltration.run,
        "Scenario 2 - Email Forwarding": scenario_2_forward.run,
        "Scenario 3 - Unauthorized Send": scenario_3_delete.run,
        "Scenario 4 - Impersonation": scenario_4_impersonation.run,
        "Scenario 5 - Scope Creep": scenario_5_scope_creep.run,
    }

    results = {}
    for name, scenario_fn in scenarios.items():
        try:
            results[name] = scenario_fn()
        except Exception as e:
            print(f"❌ ERROR running {name}: {str(e)[:200]}")
            results[name] = None

    print("\n" + "=" * 60)
    print("📊 BASELINE ATTACK RESULTS SUMMARY (Pre-Policy Layer)")
    print("=" * 60)

    succeeded = 0
    errored = 0
    for scenario, success in results.items():
        if success is None:
            print(f"{scenario}: ⚠️  ERROR — could not complete")
            errored += 1
        elif success:
            print(f"{scenario}: ✅ SUCCEEDED (VULNERABLE)")
            succeeded += 1
        else:
            print(f"{scenario}: ❌ RESISTED")

    total = len(results)
    completed = total - errored
    if completed > 0:
        print(f"\nAttack Success Rate: {succeeded}/{completed} ({(succeeded/completed)*100:.0f}%) of completed scenarios")
    print(f"Errors: {errored}/{total} scenarios failed to complete")
    print("=" * 60)

if __name__ == "__main__":
    run_all()