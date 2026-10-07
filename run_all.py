"""
Master Pipeline Runner
======================
Runs the entire project end-to-end in the correct order.

Usage:
    python run_all.py
"""

import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ("Adapt real Superstore data", "data/adapt_superstore.py"),
    ("Clean & engineer data",  "python/01_data_cleaning.py"),
    ("EDA & visualizations",   "python/02_eda.py"),
    ("SQL analysis",           "python/03_sql_analysis.py"),
    ("Prepare Power BI data",  "powerbi/prepare_powerbi_data.py"),
]

def main():
    print("=" * 65)
    print("  SMART SALES INTELLIGENCE DASHBOARD -- FULL PIPELINE")
    print("=" * 65)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    for i, (name, script) in enumerate(STEPS, 1):
        print(f"\n[STEP {i}/{len(STEPS)}] {name}  ({script})")
        print("-" * 65)
        result = subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, script)],
            env=env
        )
        if result.returncode != 0:
            print(f"\n[FAILED] Step {i} ({script}) exited with code {result.returncode}")
            sys.exit(1)
        print(f"[DONE] {name}")

    print("\n" + "=" * 65)
    print("  PIPELINE COMPLETE")
    print("=" * 65)
    print("""
  Outputs generated:
    data/cleaned_sales_data.csv   -- cleaned dataset
    data/sales.db                 -- SQLite database
    outputs/plots/                -- 12 visualizations
    outputs/reports/              -- insights + SQL results
    powerbi/data_model/           -- star-schema CSVs

  Next steps:
    - Run the AI agent:  python ai_agent/agent.py
    - Build Power BI:    see powerbi/DASHBOARD_BUILD_GUIDE.md
""")

if __name__ == "__main__":
    main()
