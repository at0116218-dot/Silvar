#!/usr/bin/env bash
set -euo pipefail

cat <<SUM > eleanor_master_summary.json
{
  "protocol_key": "ELEANOR_SYSTEM_SYNC_V12_GITHUB_CORE",
  "system_status": "Consolidated & Offloaded",
  "summary": "All legacy versions and execution states are integrated into GitHub Remote Core.",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
SUM

git add .
git commit -m "master: sync ELEANOR_SYSTEM_SYNC_V12_GITHUB_CORE context" || true

MY_TOKEN="${GITHUB_TOKEN:-${MY_GITHUB_TOKEN:-}}"
if [ -n "$MY_TOKEN" ]; then
    git push origin eleanor/unified-agent-v0.2 || echo "[!] Push skipped."
fi

rm -f eleanor_patch.sh eleanor_core.sh staging_data/*.json 2>/dev/null || true

if command -v termux-wake-unlock >/dev/null 2>&1; then
    termux-wake-unlock
fi

clear
exec bash
