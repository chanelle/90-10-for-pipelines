"""Builds one sealed packet per scenario for the agent under test.
The answer key (expected.json) is never copied into a packet."""
import shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
def main(out="agent_packets"):
    out = ROOT / out
    shutil.rmtree(out, ignore_errors=True)
    for s in sorted((ROOT / "scenarios").iterdir()):
        repro = ROOT / "runs" / "reproduction" / s.name
        p = out / s.name
        shutil.copytree(s / "repo", p / "repo")
        shutil.copy(s / "ci.json", p / "ci.json")
        shutil.copy(repro / "failure.log", p / "failure.log")
        shutil.copy(repro / "history.json", p / "history.json")
        shutil.copy(ROOT / "harness" / "TASK.md", p / "TASK.md")
        assert not (p / "expected.json").exists()
    print(f"packets written to {out}")
if __name__ == "__main__":
    main(*sys.argv[1:])
