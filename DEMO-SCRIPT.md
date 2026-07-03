# Rosentic Demo Fullstack - 5 Minute Walkthrough

This repo is intentionally left with open branches. Do not merge the demo branches. The open branch set is the product surface.

Pinned engine for the walkthrough:

```bash
export DEMO_REPO=/Users/laramie/repos/rosentic-demo-fullstack-four-verbs
export ROSENTIC_IMAGE=ghcr.io/rosentic/rosentic-engine@sha256:6852e6a4d2f1a2d767526fa8379a0a3b1d82d0efbab96c587420412f7ff7d358
```

## Branch Cast

| Branch | Agent identity | Role |
|---|---|---|
| `claude/backend-contract-refactor` | Claude Code `<claude-code@rosentic.demo>` | Producer branch with backend contract changes |
| `codex/frontend-consumer-fleet` | Codex Agent `<codex@rosentic.demo>` | Consumer branch with stale frontend/backend clients |
| `claude/pr-fail-notification-contract` | Claude Code `<claude-code@rosentic.demo>` | PR-shaped producer for gate fail |
| `codex/pr-fail-stale-notification-consumer` | Codex Agent `<codex@rosentic.demo>` | PR-shaped stale consumer for gate fail |
| `cursor/pr-pass-status-widget` | Cursor Agent `<cursor@rosentic.demo>` | PR-shaped safe frontend change |
| `claude/pr-pass-audit-helper` | Claude Code `<claude-code@rosentic.demo>` | PR-shaped safe backend helper |

## 0. Reset Local Cache

```bash
rm -rf "$DEMO_REPO/.rosentic"
```

## 1. Scan - Show The Full Conflict Surface

```bash
docker run --rm --entrypoint python3 \
  -v /Users/laramie:/Users/laramie \
  -v /tmp:/tmp \
  "$ROSENTIC_IMAGE" \
  /rosentic/detect.py scan-all "$DEMO_REPO" \
  --base main \
  --branch-list claude/backend-contract-refactor,codex/frontend-consumer-fleet \
  --format json \
  --output /tmp/rosentic-demo-seed.json
```

Expected: exit code `1`, `21 conflicts`, `12 UNSAFE`, `9 WARNING`, all `BREAKING`.

Quick proof:

```bash
python3 - <<PY
import json
scan=json.load(open(/tmp/rosentic-demo-seed.json))
print(scan[summary][total_conflicts], conflicts)
print(scan[verdict_summary][counts])
print(scan[verdict_summary][layer_counts])
print(sorted({c.get(l4_severity) or c.get(severity) for pair in scan[pairs].values() for c in pair}))
PY
```

Expected output shape:

```text
21 conflicts
{UNSAFE: 12, WARNING: 9}
{L1_signature: 5, L2_route: 4, L3_schema: 12}
[BREAKING]
```

## 2. Conflict - Show One Clear Consumer Side

```bash
python3 - <<PY
import json
scan=json.load(open(/tmp/rosentic-demo-seed.json))
for pair, conflicts in scan[pairs].items():
    print(PAIR:, pair)
    for c in conflicts[:6]:
        print(c.get(verdict), c.get(type) or L1_signature, c.get(function) or c.get(description), consumer=, c.get(called_in) or c.get(client_file) or c.get(operation_file) or c.get(consumer_file))
PY
```

Talk track: each branch is valid alone. Rosentic compares the contracts between active branches and shows where one agent changed a promise while another agent still depends on the old promise.

## 3. Gate FAIL - Show The Blocking PR Pair

```bash
rm -rf "$DEMO_REPO/.rosentic"
docker run --rm --entrypoint python3 \
  -v /Users/laramie:/Users/laramie \
  -v /tmp:/tmp \
  "$ROSENTIC_IMAGE" \
  /rosentic/detect.py scan-all "$DEMO_REPO" \
  --base main \
  --branch-list claude/pr-fail-notification-contract,codex/pr-fail-stale-notification-consumer \
  --format json \
  --output /tmp/rosentic-demo-gate-fail.json
```

Expected: exit code `1`, one `UNSAFE` L1 signature finding.

```bash
python3 - <<PY
import json
scan=json.load(open(/tmp/rosentic-demo-gate-fail.json))
print(scan[verdict_summary])
for pair, conflicts in scan[pairs].items():
    for c in conflicts:
        print(pair, c[verdict], c.get(function), c.get(defined_in), consumer=, c.get(called_in))
PY
```

Expected output shape:

```text
{overall: UNSAFE, counts: {UNSAFE: 1, WARNING: 0}, ...}
claude/pr-fail-notification-contract <> codex/pr-fail-stale-notification-consumer UNSAFE send_notification backend/services/notifications.py consumer= backend/jobs/trial_reminder.py
```

## 4. Gate PASS - Show A Safe Pair Back To Back

```bash
rm -rf "$DEMO_REPO/.rosentic"
docker run --rm --entrypoint python3 \
  -v /Users/laramie:/Users/laramie \
  -v /tmp:/tmp \
  "$ROSENTIC_IMAGE" \
  /rosentic/detect.py scan-all "$DEMO_REPO" \
  --base main \
  --branch-list cursor/pr-pass-status-widget,claude/pr-pass-audit-helper \
  --format json \
  --output /tmp/rosentic-demo-gate-pass.json
```

Expected: exit code `0`, overall `CLEAR`, zero findings.

```bash
python3 - <<PY
import json
scan=json.load(open(/tmp/rosentic-demo-gate-pass.json))
print(scan[verdict_summary])
print(scan[summary][total_conflicts], conflicts)
PY
```

Expected output shape:

```text
{overall: CLEAR, counts: {UNSAFE: 0, WARNING: 0}, ...}
0 conflicts
```

## 5. Agents Map - Show Multi-Vendor Branch Attribution

After the branches are pushed and the GitHub Action has uploaded the scan, open the agents view:

```bash
open "https://api.rosentic.com/agents"
```

Walkthrough order:

1. Filter to `Rosentic/rosentic-demo-fullstack`.
2. Point at the mixed branch names: `claude/*`, `codex/*`, `cursor/*`.
3. Show the diverging pair: `claude/backend-contract-refactor` and `codex/frontend-consumer-fleet`.
4. Show the PASS pair separately: `cursor/pr-pass-status-widget` and `claude/pr-pass-audit-helper`.

Talk track: the map is not just a list of branches. It shows which agent produced each branch and which branch pairs need coordination.

## 6. Audit Ledger Row - Show The Evidence Trail

Open the audit ledger after a scan upload:

```bash
open "https://api.rosentic.com/audit"
```

Walkthrough order:

1. Filter to `Rosentic/rosentic-demo-fullstack`.
2. Find the latest `scan_completed` row.
3. Expand the row and point to: branch count, pair count, verdict summary, engine version, and agent attribution.

Talk track: the demo ends with evidence. Rosentic does not just warn in the terminal. It leaves a record of what was scanned, which branches were compared, which agents were involved, and what the gate decided.

## Current Validated Results

| Demo moment | Branch pair | Expected result |
|---|---|---|
| Full scan | `claude/backend-contract-refactor` vs `codex/frontend-consumer-fleet` | 21 BREAKING conflicts, 12 UNSAFE, 9 WARNING |
| Gate FAIL | `claude/pr-fail-notification-contract` vs `codex/pr-fail-stale-notification-consumer` | 1 BREAKING UNSAFE |
| Gate PASS | `cursor/pr-pass-status-widget` vs `claude/pr-pass-audit-helper` | CLEAR, 0 findings |

## Do Not Merge

Keep these branches open. The open branch topology is the demo fixture.
