"""Line-coverage gate using only the standard library (trace module).
Runs the unittest suite under tracing and fails if line coverage of --source
falls below --min percent."""
import argparse, os, sys, trace, unittest
from pathlib import Path

def executable_lines(path):
    # Python 3.13 can report a phantom line 0 or None; keep real line numbers only.
    return {ln for ln in trace._find_executable_linenos(str(path)) if isinstance(ln, int) and ln > 0}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="src")
    ap.add_argument("--min", type=float, default=80)
    a = ap.parse_args()
    src = Path(a.source).resolve()
    sys.path.insert(0, str(src))
    tracer = trace.Trace(count=1, trace=0, ignoredirs=[sys.prefix, sys.exec_prefix])
    result = {}
    def run():
        suite = unittest.defaultTestLoader.discover("tests", pattern="test_*.py")
        result["r"] = unittest.TextTestRunner(verbosity=2).run(suite)
    tracer.runfunc(run)
    counts = tracer.results().counts
    hit, total = 0, 0
    print("\nName                 Stmts   Miss  Cover")
    for f in sorted(src.rglob("*.py")):
        lines = executable_lines(f)
        executed = {ln for (fn, ln) in counts if Path(fn).resolve() == f}
        miss = len(lines - executed)
        total += len(lines); hit += len(lines) - miss
        pct = 100 * (len(lines) - miss) / len(lines) if lines else 100
        print(f"{str(f.relative_to(src.parent)):<20} {len(lines):>5} {miss:>6} {pct:>5.0f}%")
    cov = 100 * hit / total if total else 100
    print(f"TOTAL                {total:>5} {total-hit:>6} {cov:>5.0f}%")
    if not result["r"].wasSuccessful():
        print("ERROR: unit tests failed"); return 1
    if cov < a.min:
        print(f"ERROR: Coverage failure: total of {cov:.0f}% is less than fail-under={a.min:.0f}%")
        return 2
    print(f"Required coverage of {a.min:.0f}% reached. Total coverage: {cov:.0f}%")
    return 0

if __name__ == "__main__":
    sys.exit(main())
