"""Mini CI runner. Executes a scenario's jobs (scenarios/<id>/ci.json) the way a
pipeline would, captures the job log, and records pass/fail history across runs.

Usage: python harness/ci.py <scenario_dir> [--runs N] [--out runs/reference]
"""
import argparse, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run_job(workdir, job):
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(workdir), "LANG": "C.UTF-8"}
    env.update(job.get("env", {}))
    log, code = [], 0
    for cmd in job["script"]:
        log.append(f"$ {cmd}")
        p = subprocess.run(cmd, shell=True, cwd=workdir, env=env, capture_output=True, text=True, timeout=120)
        log.append((p.stdout + p.stderr).rstrip())
        if p.returncode != 0:
            code = p.returncode
            log.append(f"ERROR: Job failed: exit code {p.returncode}")
            break
    if code == 0:
        log.append("Job succeeded")
    return code, "\n".join(log)

def run_scenario(sdir, runs):
    cfg = json.loads((sdir / "ci.json").read_text())
    history, first_fail_log = [], None
    for i in range(runs):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "repo"
            shutil.copytree(sdir / "repo", work)
            status = "passed"
            logs = []
            for job in cfg["jobs"]:
                code, log = run_job(work, job)
                logs.append(f"Running job: {job['name']} (image: {cfg.get('image', 'python:3.13')})\n{log}")
                if code != 0:
                    status = f"failed ({job['name']})"
                    break
            history.append(status)
            if status != "passed" and first_fail_log is None:
                first_fail_log = "\n\n".join(logs)
    return cfg, history, first_fail_log

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario")
    ap.add_argument("--runs", type=int, default=None)
    ap.add_argument("--out", default=str(ROOT / "runs" / "reproduction"))
    a = ap.parse_args()
    sdir = Path(a.scenario).resolve()
    cfg = json.loads((sdir / "ci.json").read_text())
    runs = a.runs or cfg.get("history_runs", 5)
    cfg, history, log = run_scenario(sdir, runs)
    out = Path(a.out) / sdir.name
    out.mkdir(parents=True, exist_ok=True)
    fails = sum(1 for h in history if h != "passed")
    summary = {"scenario": sdir.name, "runs": runs, "failed": fails, "history": history,
               "reproduces": fails > 0, "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (out / "history.json").write_text(json.dumps(summary, indent=2))
    if log:
        (out / "failure.log").write_text(log + "\n")
    print(f"{sdir.name}: {fails}/{runs} runs failed")
    return 0 if fails else 1

if __name__ == "__main__":
    sys.exit(main())
