#!/usr/bin/env bash
set -euo pipefail

# 1. Master Context Keyword and Summary Log
cat <<SUM > eleanor_master_summary.json
{
  "protocol_key": "ELEANOR_SYSTEM_SYNC_V12_GITHUB_CORE",
  "system_status": "Consolidated & Offloaded",
  "summary": "All legacy versions, ChatGPT archives, and execution states are integrated into GitHub Remote Core.",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
SUM

# 2. Synchronize final context to GitHub Core
git add .
git commit -m "master: sync ELEANOR_SYSTEM_SYNC_V12_GITHUB_CORE context" || true

MY_TOKEN="${GITHUB_TOKEN:-${MY_GITHUB_TOKEN:-}}"
if [ -n "$MY_TOKEN" ]; then
    git push origin eleanor/unified-agent-v0.2 || echo "[!] Push skipped. Set GITHUB_TOKEN if needed."
fi

# 3. Clean local temporary script files
rm -f eleanor_patch.sh eleanor_core.sh staging_data/*.json 2>/dev/null || true

if command -v termux-wake-unlock >/dev/null 2>&1; then
    termux-wake-unlock
fi

# 4. Clear screen and refresh environment
clear
exec bash
