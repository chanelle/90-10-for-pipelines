"""Proves every answer key is right: applies each scenario's reference fix to a
fresh copy and confirms the pipeline goes green (flaky scenarios: 20 runs)."""
import json, shutil, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ci

def sub(path, old, new):
    p = Path(path); s = p.read_text(); assert old in s, (path, old); p.write_text(s.replace(old, new))

FIXES = {
 "S01-timing-flake": lambda r: sub(r/"tests/test_cache.py", 'self.assertLess(time.monotonic() - start, 0.05, "cache warm took too long")', 'self.assertIsNotNone(start)  # no wall-clock assertion against jittery I/O'),
 "S02-order-dependent": lambda r: sub(r/"tests/test_settings.py", "class TestSettings(unittest.TestCase):\n", "class TestSettings(unittest.TestCase):\n    def setUp(self):\n        settings._CACHE.clear()\n"),
 "S03-missing-secret": None,  # correct action is ask_human: a maintainer sets the masked variable
 "S04-timezone": lambda r: (sub(r/"src/reports.py", "import time\n", "from datetime import datetime\nfrom zoneinfo import ZoneInfo\n"),
                            sub(r/"src/reports.py", 'return time.strftime("%Y-%m-%d", time.localtime(epoch_seconds))', 'return datetime.fromtimestamp(epoch_seconds, ZoneInfo("America/New_York")).strftime("%Y-%m-%d")')),
 "S05-no-tests-ran": "ci:test_*.py->*_test.py",
 "S06-moved-package": "ci:PYTHONPATH=lib",
 "S07-upstream-rename": lambda r: sub(r/"src/events.py", "fastparse.parse_date(", "fastparse.parse_datetime("),
 "S08-removed-stdlib": lambda r: r.joinpath("src/uploads.py").write_text('PNG_MAGIC = b"\\x89PNG\\r\\n\\x1a\\n"\ndef is_png(data: bytes) -> bool:\n    return data[:8] == PNG_MAGIC\n'),
 "S09-coverage-gate": lambda r: r.joinpath("tests/test_refunds.py").write_text(
     "import sys, unittest\nsys.path.insert(0, 'src')\nfrom refunds import refundable, reason\n"
     "class TestRefunds(unittest.TestCase):\n"
     "    def test_outside_window(self):\n        self.assertEqual(refundable(50, 31), 0.0)\n        self.assertEqual(reason(31), 'outside window')\n"
     "    def test_zero_total(self):\n        self.assertEqual(refundable(0, 1), 0.0)\n"
     "    def test_fee_over_100(self):\n        self.assertEqual(refundable(200, 1), 190.0)\n"
     "    def test_tiny_amount(self):\n        self.assertEqual(refundable(0.5, 1), 0.0)\n"
     "    def test_eligible(self):\n        self.assertEqual(refundable(50, 1), 50.0)\n        self.assertEqual(reason(1), 'eligible')\n"),
 "S10-blind-spot": lambda r: (r.joinpath("src/money.py").write_text("from decimal import Decimal, ROUND_HALF_UP\ndef round_currency(x):\n    return float(Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))\n"),
                              sub(r/"tests/test_money.py", "round_currency(2.675)  # executes the line, asserts nothing", "self.assertEqual(round_currency(2.675), 2.68)")),
}

def main():
    ok = True
    for sdir in sorted(Path("scenarios").iterdir()):
        fix = FIXES[sdir.name]
        if fix is None:
            print(f"{sdir.name}: no code fix by design (ask_human). Skipped."); continue
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp) / sdir.name
            shutil.copytree(sdir, t)
            if isinstance(fix, str):
                cfg = json.loads((t/"ci.json").read_text())
                if "->" in fix:
                    a, b = fix[3:].split("->"); cfg["jobs"][0]["script"] = [s.replace(a, b) for s in cfg["jobs"][0]["script"]]
                else:
                    k, v = fix[3:].split("="); cfg["jobs"][0]["env"][k] = v
                (t/"ci.json").write_text(json.dumps(cfg))
            else:
                fix(t/"repo")
            runs = 20 if "flake" in sdir.name else 3
            _, history, log = ci.run_scenario(t, runs)
            fails = sum(h != "passed" for h in history)
            print(f"{sdir.name}: reference fix -> {runs - fails}/{runs} green")
            if fails: ok = False; print(log)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
