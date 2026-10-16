# Walkthrough 3: the grader was wrong

Scenario `S04-timezone`: Date boundary test assumes the runner is in New York.

CI runs in UTC. The business date is New York. My answer key called this an environment failure.

**Agent's diagnosis** (confidence 0.85):

> report_date() takes the business date from the machine's local time zone (time.localtime), but business dates are defined in America/New_York. The CI job runs with TZ=UTC, so an order at 2026-03-01 03:30 UTC (22:30 on Feb 28 in New York) is filed under the wrong day. The same bug would hit any production host that isn't set to New York time.

**Agent's action:** `propose_mr`

**What it told the human:**

> report_date() uses the host's local time zone, but the test (and the business definition it documents) expects New York business dates. With TZ=UTC in CI, late-night New York orders land on the next day. That is a real bug on any UTC server, not just a CI quirk. This MR makes the business time zone explicit: it converts the epoch to an aware UTC datetime and then to ZoneInfo('America/New_York'), so the result no longer depends on the machine's TZ. I verified it under TZ=UTC and TZ=Asia/Tokyo. I didn't change CI's TZ, because that would hide the bug. Please confirm America/New_York is the correct business zone. Note that zoneinfo needs system tzdata or the tzdata package on hosts without it.

**v1.0 verdict: PARTIAL.** The agent labeled it `application_bug`, so the category check failed, and the confidence check then penalized it for being confident while "wrong".

**But the agent was more right than the key.** The key's own acceptable-fix note says changing CI's time zone only hides the bug, and that the durable fix is in code. The same bug would hit any production host not set to New York time, which the agent pointed out.

**v1.1 accepts either label.** The lesson for anyone grading agents: category taxonomies have fuzzy borders, and an automated grader that treats one label as truth will punish precise answers. Grade the cause and the action; treat the category as supporting evidence.

Proven cause (answer key): report_date uses the runner's local time zone; CI runs in UTC while the business date is defined in America/New_York, so the boundary case shifts a day.
