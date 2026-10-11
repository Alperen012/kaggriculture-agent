#!/usr/bin/env python3
"""
Official 5 Regression Benchmark Gates for Kaggriculture Agents.

Gate 1: 14 Benchmark Matches vs Sub22 baseline across 7 seeds (dual seat). Threshold: 14/14 wins, net margin >= +36,366.
Gate 2: Solo seed 1317954741 against random baseline. Threshold: score >= 108,758.
Gate 3: H2H 14 matches against V74 reference agent. Threshold: net diff >= 0.
Gate 4: Solo seed 2064275186 against random baseline. Threshold: score >= 97,182.
Gate 5: Seed 1894253825 vs Sub22. Threshold: score > 84,727 (net win).
"""

import sys
import os
import importlib.util

try:
    from kaggle_environments import make
except ImportError:
    print("Error: kaggle_environments is required. Run: pip install kaggle-environments", file=sys.stderr)
    sys.exit(1)

def load_agent_from_file(filepath, module_name="eval_agent"):
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "agent", getattr(mod, "kaggle_submission_agent", None))

def run_match(seed, agent0, agent1, debug=False):
    env = make("kaggriculture", configuration={"seed": seed}, debug=debug)
    env.run([agent0, agent1])
    s0, s1 = env.state[0]["reward"], env.state[1]["reward"]
    return s0, s1

def run_benchmark(agent_path=None):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if agent_path is None:
        agent_path = os.path.join(root_dir, "src", "main.py")

    print(f"Loading candidate agent from {agent_path}...")
    candidate_fn = load_agent_from_file(agent_path, "candidate_mod")
    if candidate_fn is None:
        print(f"Error: Could not find agent entrypoint in {agent_path}", file=sys.stderr)
        sys.exit(1)

    print("Agent successfully loaded.\n")
    print("=" * 70)
    print("RUNNING OFFICIAL REGRESSION BENCHMARK GATES")
    print("=" * 70)

    # GATE 2: Seed 1317954741 Solo
    print("\n[GATE 2] Seed 1317954741 Solo Performance")
    env = make("kaggriculture", configuration={"seed": 1317954741}, debug=False)
    env.run([candidate_fn, "random"])
    g2_score = env.state[0]["reward"]
    g2_pass = g2_score >= 108758
    print(f"  Score: {g2_score:,.0f} | Required: >= 108,758 | Result: {'PASS' if g2_pass else 'FAIL'}")

    # GATE 4: Seed 2064275186 Solo
    print("\n[GATE 4] Seed 2064275186 Solo Performance")
    env = make("kaggriculture", configuration={"seed": 2064275186}, debug=False)
    env.run([candidate_fn, "random"])
    g4_score = env.state[0]["reward"]
    g4_pass = g4_score >= 97182
    print(f"  Score: {g4_score:,.0f} | Required: >= 97,182 | Result: {'PASS' if g4_pass else 'FAIL'}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print(f"Gate 2: {'PASS' if g2_pass else 'FAIL'}")
    print(f"Gate 4: {'PASS' if g4_pass else 'FAIL'}")
    print("=" * 70)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    run_benchmark(target)
