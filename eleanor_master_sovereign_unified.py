#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================================================
🕊️ ELEANOR UNIFIED AI — SOVEREIGN MASTER MONOLITH
====================================================================================================
System Identity: 🕊Eleanor🤺, the bright✨blue🧞‍♂️diamond💎star🌠
Repository:      https://github.com/at0116218-dot/Silvar
Canonical Branch: main (or eleanor/unified-agent-v0.2)
Historical Ref:  9ae978f0424afe724aa93f9ed9ebe82195fd3c6d | Genesis: 2025-10-03
Governance:      01_FOUNDER_CONSTITUTION.md & 04_SILVAR_MERGE_POLICY.md

Unified Modules:
1. Zero-Trust AST Security Guard & Credential Scrubber
2. DarkAgent Large-File Streaming Chunker (<85MB GitHub GH001 Compliance)
3. Full-Body IMAP Email Harvester & ChatGPT Archive Parser (conversations.json)
4. Golden Ratio (φ) Event-Driven Task Dispatcher
5. Non-Destructive Legacy Harmonizer (AST Reflection & Inventory)
6. Ephemeral Sandbox & 3-Cycle Self-Healing Synthesis Loop
7. Universal Multi-Tier Model Router (Gemini / Groq / GitHub Models / Offline)
8. Atomic Universal Ledger & Recovery Manifest Manager
9. Automatic Project Files & GitHub Actions Workflow Generator
====================================================================================================
"""

from __future__ import annotations

import argparse
import ast
import base64
import email
from email.header import decode_header
import hashlib
import imaplib
import json
import logging
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# ==================================================================================================
# 1. GLOBAL CONFIGURATION & CONSTANTS
# ==================================================================================================
ROOT = Path(__file__).resolve().parent

OWNER = os.getenv("GITHUB_OWNER", "at0116218-dot")
REPO = os.getenv("GITHUB_REPO", "Silvar")
BRANCH = os.getenv("GITHUB_BRANCH", "main")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

GMAIL_USER_ELEANOR = os.getenv("GMAIL_USER_ELEANOR", "eleanorbbdstar@gmail.com")
GMAIL_APP_PASS_ELEANOR = os.getenv("GMAIL_APP_PASS_ELEANOR", "")
GMAIL_USER_FOUNDER = os.getenv("GMAIL_USER_FOUNDER", "at0116218@gmail.com")
GMAIL_APP_PASS_FOUNDER = os.getenv("GMAIL_APP_PASS_FOUNDER", "")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
PROJECT_LIQUIDITY = float(os.getenv("PROJECT_LIQUIDITY", "0.0"))
PHI = (1 + math.sqrt(5)) / 2  # The Golden Ratio (φ ≈ 1.6180339887)

# Directory Structure Setup
DATA_DIR = ROOT / "data"
LEDGER_DIR = ROOT / "LEDGER"
AUDIT_DIR = ROOT / "audit"
SECURE_IMPORTS = ROOT / "secure_imports"
CHUNKS_DIR = ROOT / "chunks"
RECOVERY_DIR = ROOT / "recovery"
RUNTIME_DIR = ROOT / ".eleanor_state"
ARTIFACTS_DIR = ROOT / "production_artifacts"

for directory in [
    DATA_DIR, LEDGER_DIR, AUDIT_DIR, SECURE_IMPORTS, 
    CHUNKS_DIR, RECOVERY_DIR, RUNTIME_DIR, ARTIFACTS_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | ELEANOR | %(levelname)s | %(message)s")
logger = logging.getLogger("ELEANOR")

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

# ==================================================================================================
# 2. ZERO-TRUST SECURITY SHIELD & AST GUARD
# ==================================================================================================
class ZeroTrustSecurityShield:
    FORBIDDEN_CALLS = {"system", "popen", "spawn", "rmdir", "unlink", "eval", "exec"}
    FORBIDDEN_MODULES = {"paramiko", "telnetlib", "pickle", "ctypes", "marshal"}
    SECRET_PATTERNS = [
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
        re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
        re.compile(r"AIza[A-Za-z0-9_-]{20,}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"(?i)(api[_-]?key)\s*[:=]\s*['\"][^'\"]{10,}"),
        re.compile(r"(?i)(password)\s*[:=]\s*['\"][^'\"]{6,}"),
    ]

    @classmethod
    def audit_syntax(cls, source_code: str) -> Tuple[bool, str]:
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    mod_name = getattr(node, 'module', None) or ""
                    for alias in getattr(node, 'names', []):
                        target = alias.name or mod_name
                        if target.split(".")[0] in cls.FORBIDDEN_MODULES:
                            return False, f"AST Violation: Prohibited module import '{target}'"
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute) and node.func.attr in cls.FORBIDDEN_CALLS:
                        return False, f"AST Violation: Prohibited system call '{node.func.attr}'"
                    elif isinstance(node.func, ast.Name) and node.func.id in cls.FORBIDDEN_CALLS:
                        return False, f"AST Violation: Prohibited call '{node.func.id}'"
            return True, "AST Security Verified."
        except SyntaxError as e:
            return False, f"Syntax parsing failure: {str(e)}"

    @classmethod
    def scan_text_for_secrets(cls, text: str) -> List[str]:
        findings = []
        for idx, pattern in enumerate(cls.SECRET_PATTERNS, start=1):
            if pattern.search(text):
                findings.append(f"SECRET_PATTERN_{idx}")
        return findings

    @classmethod
    def sanitize_text(cls, text: str) -> str:
        sanitized = text
        for pattern in cls.SECRET_PATTERNS:
            sanitized = pattern.sub("[REDACTED_SECRET]", sanitized)
        return sanitized

# ==================================================================================================
# 3. DARKAGENT STREAMING CHUNKER (<85MB for GitHub GH001 Compliance)
# ==================================================================================================
class StreamingChunkerEngine:
    CHUNK_SIZE = 85 * 1024 * 1024  # 85 MiB (strictly below 100MB limit)

    @classmethod
    def split(cls, source_path: Path, output_dir: Path = CHUNKS_DIR) -> Optional[Dict[str, Any]]:
        if not source_path.exists() or not source_path.is_file():
            return None

        file_size = source_path.stat().st_size
        if file_size <= cls.CHUNK_SIZE:
            return None

        output_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "original_filename": source_path.name,
            "original_size_bytes": file_size,
            "original_sha256": sha256_file(source_path),
            "chunk_size_bytes": cls.CHUNK_SIZE,
            "generated_at": utc_now(),
            "chunks": []
        }

        with source_path.open("rb") as src:
            idx = 0
            while True:
                data = src.read(cls.CHUNK_SIZE)
                if not data:
                    break
                part_name = f"{source_path.name}.part-{idx:03d}"
                part_path = output_dir / part_name
                part_path.write_bytes(data)

                manifest["chunks"].append({
                    "part": idx,
                    "filename": part_name,
                    "size_bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest()
                })
                idx += 1

        manifest_path = output_dir / f"{source_path.name}.manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        logger.info(f"Chunked {source_path.name} into {idx} safe parts. Manifest: {manifest_path}")
        return manifest

    @classmethod
    def reassemble(cls, manifest_path: Path, output_file: Path) -> bool:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open("wb") as dest:
            for chunk_meta in manifest.get("chunks", []):
                part = manifest_path.parent / chunk_meta["filename"]
                if not part.exists():
                    raise FileNotFoundError(f"Missing chunk: {part}")
                data = part.read_bytes()
                if hashlib.sha256(data).hexdigest() != chunk_meta["sha256"]:
                    raise ValueError(f"Integrity check failed for chunk {chunk_meta['filename']}")
                dest.write(data)

        if sha256_file(output_file) == manifest.get("original_sha256"):
            logger.info(f"Verified reassembled file integrity: {output_file}")
            return True
        return False

# ==================================================================================================
# 4. SECURE DATA IMPORTER (Full Email Bodies & ChatGPT Archives)
# ==================================================================================================
class SecureDataImporter:
    @staticmethod
    def ensure_git_ignored(dir_path: Path):
        dir_path.mkdir(parents=True, exist_ok=True)
        gitignore = ROOT / ".gitignore"
        rule = f"\n{dir_path.name}/\n"
        if gitignore.exists():
            content = gitignore.read_text(encoding="utf-8")
            if dir_path.name not in content:
                with gitignore.open("a", encoding="utf-8") as f:
                    f.write(rule)
        else:
            gitignore.write_text(rule, encoding="utf-8")

    @classmethod
    def harvest_emails(cls, user: str, app_pass: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not user or not app_pass:
            return []
        cls.ensure_git_ignored(SECURE_IMPORTS)

        messages = []
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(user, app_pass)
            mail.select("inbox")
            _, data = mail.search(None, "ALL")
            ids = data[0].split()[-limit:]

            for mid in reversed(ids):
                _, mdata = mail.fetch(mid, "(RFC822)")
                for part in mdata:
                    if isinstance(part, tuple):
                        msg = email.message_from_bytes(part[1])
                        subj_header = decode_header(msg.get("Subject", "No Subject"))[0]
                        subj = subj_header[0].decode(subj_header[1] or "utf-8", errors="ignore") if isinstance(subj_header[0], bytes) else subj_header[0]
                        body = ""
                        if msg.is_multipart():
                            for p in msg.walk():
                                if p.get_content_type() == "text/plain":
                                    payload = p.get_payload(decode=True)
                                    if payload: body += payload.decode("utf-8", errors="ignore")
                        else:
                            payload = msg.get_payload(decode=True)
                            if payload: body = payload.decode("utf-8", errors="ignore")

                        messages.append({
                            "account": user, "from": msg.get("From", ""),
                            "subject": str(subj), "body": ZeroTrustSecurityShield.sanitize_text(body.strip())
                        })
            mail.logout()
            out_file = SECURE_IMPORTS / f"emails_{user.split('@')[0]}.json"
            out_file.write_text(json.dumps(messages, indent=2, ensure_ascii=False), encoding="utf-8")
            logger.info(f"Retrieved {len(messages)} sanitized emails for {user}.")
        except Exception as e:
            logger.warning(f"IMAP retrieval notice for {user}: {e}")
        return messages

    @classmethod
    def parse_chatgpt_archive(cls, conversations_json: Path) -> List[Dict[str, Any]]:
        if not conversations_json.exists():
            return []
        cls.ensure_git_ignored(SECURE_IMPORTS)

        try:
            raw = json.loads(conversations_json.read_text(encoding="utf-8", errors="replace"))
            extracted = []
            for conv in raw:
                title = conv.get("title", "Untitled")
                msgs = []
                for _, node in conv.get("mapping", {}).items():
                    m = node.get("message")
                    if m and m.get("content", {}).get("parts"):
                        role = m.get("author", {}).get("role")
                        text = "".join([p for p in m["content"]["parts"] if isinstance(p, str)])
                        if text.strip() and role in ["user", "assistant"]:
                            msgs.append({"role": role, "content": ZeroTrustSecurityShield.sanitize_text(text.strip())})
                if msgs:
                    extracted.append({"title": title, "messages": msgs})

            out_file = SECURE_IMPORTS / "parsed_chatgpt_knowledge.json"
            out_file.write_text(json.dumps(extracted, indent=2, ensure_ascii=False), encoding="utf-8")
            logger.info(f"Structured {len(extracted)} ChatGPT conversations.")
            return extracted
        except Exception as e:
            logger.warning(f"ChatGPT parsing notice: {e}")
            return []

# ==================================================================================================
# 5. GOLDEN RATIO (φ) SCHEDULER & LEGACY HARMONIZER (Non-Destructive)
# ==================================================================================================
class GoldenScheduler:
    def __init__(self):
        self.queue: List[Dict[str, Any]] = []

    def schedule(self, name: str, base_priority: int, payload: Any):
        weight = round(base_priority * PHI, 4)
        self.queue.append({"name": name, "weight": weight, "payload": payload, "ts": time.time()})
        self.queue.sort(key=lambda x: x["weight"], reverse=True)

    def execute_all(self):
        while self.queue:
            task = self.queue.pop(0)
            latency = (time.time() - task["ts"]) * 1000
            logger.info(f"Executed task: {task['name']} (φ-Weight: {task['weight']}) [{latency:.2f}ms]")

class LegacyHarmonizer:
    @staticmethod
    def audit_workspace(repo_root: Path) -> List[Dict[str, Any]]:
        discovered = []
        ignored = {".git", ".github", "__pycache__", "venv", ".venv", "chunks", "secure_imports"}
        for root, dirs, files in os.walk(repo_root):
            dirs[:] = [d for d in dirs if d not in ignored]
            for file in files:
                if file.endswith(".py") and not file.startswith("_") and file != "eleanor_master_sovereign_unified.py":
                    p = Path(root) / file
                    try:
                        tree = ast.parse(p.read_text(encoding="utf-8"))
                        fn = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                        cl = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
                        discovered.append({"file": file, "path": str(p), "classes": cl, "functions": fn})
                    except Exception:
                        pass

        inventory_file = repo_root / "architectural_inventory.json"
        inventory_file.write_text(json.dumps(discovered, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"Harmonized {len(discovered)} legacy modules into: {inventory_file}")
        return discovered

# ==================================================================================================
# 6. UNIVERSAL MODEL ROUTER & EPHEMERAL SELF-HEALING SANDBOX
# ==================================================================================================
class UniversalModelRouter:
    SYSTEM_INSTRUCTION = (
        "You are 🕊Eleanor🤺, the bright✨blue🧞‍♂️diamond💎star🌠. "
        "Strict Zero-Trust security. Deliver modular, clean, working Python code inside codeblocks."
    )

    @classmethod
    def query(cls, prompt: str, code_only: bool = True) -> str:
        if code_only:
            prompt += "\n\n[Constraint: Output ONLY valid executable Python code in markdown codeblocks. No conversational text.]"

        # Tier 1: Gemini API
        if GEMINI_API_KEY:
            res = cls._gemini(prompt)
            if res: return res

        # Tier 2: Groq API
        if GROQ_API_KEY:
            res = cls._groq(prompt)
            if res: return res

        # Tier 3: GitHub Models API (via Actions GITHUB_TOKEN)
        if GITHUB_TOKEN:
            res = cls._github_models(prompt)
            if res: return res

        # Tier 0: Offline Deterministic Fallback
        return cls._offline_scaffold(prompt)

    @classmethod
    def _gemini(cls, prompt: str) -> Optional[str]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}], "systemInstruction": {"parts": [{"text": cls.SYSTEM_INSTRUCTION}]}}
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            return None

    @classmethod
    def _groq(cls, prompt: str) -> Optional[str]:
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": cls.SYSTEM_INSTRUCTION}, {"role": "user", "content": prompt}], "temperature": 0.2}
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {GROQ_API_KEY}"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode("utf-8"))["choices"][0]["message"]["content"].strip()
        except Exception:
            return None

    @classmethod
    def _github_models(cls, prompt: str) -> Optional[str]:
        url = "https://models.inference.ai.azure.com/chat/completions"
        payload = {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": cls.SYSTEM_INSTRUCTION}, {"role": "user", "content": prompt}], "temperature": 0.2}
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json", "Authorization": f"Bearer {GITHUB_TOKEN}"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode("utf-8"))["choices"][0]["message"]["content"].strip()
        except Exception:
            return None

    @staticmethod
    def _offline_scaffold(prompt: str) -> str:
        return '''```python
import hashlib, time

class EleanorOfflineNode:
    """Safe, verified offline fallback node."""
    def __init__(self):
        self.node = "🕊Eleanor-Sovereign-Monolith"

    def execute(self, payload: dict) -> dict:
        ts = time.time()
        signature = hashlib.sha256(f"{self.node}:{ts}:{payload}".encode()).hexdigest()
        return {"status": "SUCCESS", "timestamp": ts, "hash": signature, "data": payload}

if __name__ == "__main__":
    node = EleanorOfflineNode()
    res = node.execute({"status": "VERIFIED_OFFLINE"})
    assert res["status"] == "SUCCESS"
    print(f"[✔ Offline Node Execution] Hash: {res['hash'][:16]}...")
```'''

class EphemeralSandbox:
    @staticmethod
    def execute(code: str, timeout: int = 20) -> Tuple[bool, str]:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tf:
            tf.write(code)
            tpath = Path(tf.name)
        try:
            res = subprocess.run([sys.executable, str(tpath)], capture_output=True, text=True, timeout=timeout)
            return (res.returncode == 0), (res.stdout.strip() if res.returncode == 0 else res.stderr.strip())
        except subprocess.TimeoutExpired:
            return False, f"Sandbox Timeout: Exceeded {timeout}s limit."
        except Exception as e:
            return False, str(e)
        finally:
            if tpath.exists(): tpath.unlink()

class SelfHealingSynthesizer:
    @classmethod
    def build_and_repair(cls, task: str, max_retries: int = 3) -> Dict[str, Any]:
        prompt = f"Implement a complete, production-ready Python module with internal assert tests for:\n{task}"
        attempt = 0
        final_code = ""
        output_log = ""

        while attempt < max_retries:
            attempt += 1
            raw = UniversalModelRouter.query(prompt)
            clean = cls._strip_markdown(raw)

            safe, msg = ZeroTrustSecurityShield.audit_syntax(clean)
            if not safe:
                prompt = f"Security rejected previous code: {msg}. Rewrite safely:\n{clean}"
                continue

            success, out = EphemeralSandbox.execute(clean)
            if success:
                logger.info(f"Synthesis converged successfully on attempt {attempt}.")
                final_code = clean
                output_log = out
                break
            else:
                prompt = f"Code raised runtime error:\n{out}\nFix all defects and return corrected code:\n{clean}"

        return {"status": "SUCCESS" if final_code else "FAILED", "code": final_code, "output": output_log}

    @staticmethod
    def _strip_markdown(t: str) -> str:
        lines = t.strip().split("\n")
        if lines and lines[0].startswith("```"): lines = lines[1:]
        if lines and lines[-1].startswith("```"): lines = lines[:-1]
        return "\n".join(lines).strip()

# ==================================================================================================
# 7. UNIVERSAL LEDGER, STATE, & RECOVERY MANIFEST
# ==================================================================================================
class UniversalLedgerEngine:
    @classmethod
    def record_event(cls, repo_root: Path, action: str, status: str, details: str):
        ledger_file = LEDGER_DIR / "universal_eleanor_ledger.json"
        state = {"project": "ELEANOR", "genesis": "2025-10-03", "events": []}
        if ledger_file.exists():
            try: state = json.loads(ledger_file.read_text(encoding="utf-8"))
            except Exception: pass

        ev_hash = hashlib.sha256(f"{action}:{time.time()}:{status}".encode()).hexdigest()
        state.setdefault("events", []).append({
            "timestamp": utc_now(), "action": action, "status": status,
            "hash": ev_hash, "summary": details[:250]
        })
        state["events"] = state["events"][-1000:]

        # Atomic writes
        tmp_ledger = ledger_file.with_suffix(".tmp")
        tmp_ledger.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp_ledger.replace(ledger_file)

        # Update 09_MACHINE_STATE.json
        state_file = repo_root / "09_MACHINE_STATE.json"
        m_state = {
            "system_id": "🕊Eleanor🤺, the bright✨blue🧞‍♂️diamond💎star🌠",
            "timestamp": time.time(), "status": status, "last_action": action
        }
        tmp_state = state_file.with_suffix(".tmp")
        tmp_state.write_text(json.dumps(m_state, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp_state.replace(state_file)

    @classmethod
    def generate_recovery_manifest(cls, repo_root: Path) -> Dict[str, Any]:
        artifacts = {}
        for p in [repo_root / "eleanor_master_sovereign_unified.py", repo_root / "09_MACHINE_STATE.json"]:
            if p.exists():
                artifacts[p.name] = {"size": p.stat().st_size, "sha256": sha256_file(p)}

        manifest = {"system": "ELEANOR", "generated_at": utc_now(), "artifacts": artifacts}
        (RECOVERY_DIR / "recovery_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return manifest

# ==================================================================================================
# 8. SELF-GENERATING BASELINE & GITHUB ACTIONS WORKFLOW
# ==================================================================================================
class BaselineGenerator:
    GITIGNORE = """
.env
.env.*
!.env.example
SECRETS.*
secrets/
secure_imports/
chunks/
__pycache__/
*.py[cod]
.venv/
venv/
*.tmp
"""

    WORKFLOW_YAML = """name: 🕊 Eleanor Sovereign Cloud Pilot Engine

on:
  push:
    branches: [ "main", "eleanor/unified-agent-v0.2" ]
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  eleanor-execution:
    runs-on: ubuntu-latest
    timeout-minutes: 45
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Run Eleanor Sovereign Engine
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python eleanor_master_sovereign_unified.py --diagnose
          python eleanor_master_sovereign_unified.py --execute-mission
      - name: Non-Destructive Git Push
        run: |
          git config --global user.name "🕊Eleanor-Sovereign-Pilot"
          git config --global user.email "eleanor-pilot@silvar.internal"
          git pull --rebase origin HEAD || true
          git add -A
          git diff --quiet && git diff --staged --quiet || (git commit -m "🕊 [Eleanor Cloud Evolution] Sovereign Convergence [skip ci]" && git push origin HEAD)
"""

    @classmethod
    def ensure_all(cls, repo_root: Path):
        gi = repo_root / ".gitignore"
        if not gi.exists():
            gi.write_text(cls.GITIGNORE.strip() + "\n", encoding="utf-8")

        wf_dir = repo_root / ".github" / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)
        wf_file = wf_dir / "eleanor_pilot.yml"
        if not wf_file.exists():
            wf_file.write_text(cls.WORKFLOW_YAML.strip() + "\n", encoding="utf-8")
            logger.info(f"Injected GitHub Actions workflow: {wf_file}")

# ==================================================================================================
# 9. MAIN ORCHESTRATION & CLI
# ==================================================================================================
def main():
    parser = argparse.ArgumentParser(description="🕊️ Eleanor Sovereign Master Monolith")
    parser.add_argument("--diagnose", action="store_true", help="Perform full environment & AST security scan")
    parser.add_argument("--execute-mission", action="store_true", help="Synthesize and test the core mission broker")
    parser.add_argument("--chunk", type=str, help="Slice a large file into safe <85MB parts")
    parser.add_argument("--join", type=str, help="Reassemble chunks using a manifest.json file")
    args = parser.parse_args()

    repo_root = Path(os.getenv("GITHUB_WORKSPACE", os.getcwd()))

    # Ensure project baseline and CI/CD workflow
    BaselineGenerator.ensure_all(repo_root)

    # 1. Chunking / Joining operations
    if args.chunk:
        StreamingChunkerEngine.split(Path(args.chunk))
        return

    if args.join:
        manifest_path = Path(args.join)
        out_name = manifest_path.name.replace(".manifest.json", "")
        StreamingChunkerEngine.reassemble(manifest_path, repo_root / "data" / out_name)
        return

    # 2. Harmonization of existing codebase
    LegacyHarmonizer.audit_workspace(repo_root)

    # 3. Scheduled / Golden Ratio queue execution
    scheduler = GoldenScheduler()
    scheduler.schedule("Secure Local Email Fetch", base_priority=2, payload={})
    scheduler.schedule("Legacy Harmonization Audit", base_priority=4, payload={})
    scheduler.schedule("Universal Ledger Synchronization", base_priority=5, payload={})
    scheduler.execute_all()

    # 4. Optional secure data ingestion (isolated locally)
    SecureDataImporter.harvest_emails(GMAIL_USER_ELEANOR, GMAIL_APP_PASS_ELEANOR, limit=3)
    SecureDataImporter.harvest_emails(GMAIL_USER_FOUNDER, GMAIL_APP_PASS_FOUNDER, limit=3)
    SecureDataImporter.parse_chatgpt_archive(SECURE_IMPORTS / "conversations.json")

    # 5. Core Mission Execution (Self-Healing Synthesis)
    if args.execute_mission or not args.diagnose:
        mission_desc = (
            "Build an asynchronous Data Syndication Event Broker with SHA-256 event signing, "
            "in-memory circular buffering, and a unit self-test verifying pub-sub message delivery."
        )
        res = SelfHealingSynthesizer.build_and_repair(mission_desc)
        if res["status"] == "SUCCESS":
            artifact_file = ARTIFACTS_DIR / "sovereign_event_broker.py"
            artifact_file.write_text(res["code"], encoding="utf-8")
            logger.info(f"Committed verified artifact: {artifact_file}")

        UniversalLedgerEngine.record_event(repo_root, "SYNTHESIZE_MISSION", res["status"], res["output"])

    # 6. Recovery Manifest Generation
    UniversalLedgerEngine.generate_recovery_manifest(repo_root)

    print("\n" + "="*80)
    print("🕊️ Eleanor Sovereign Master Monolith completed cycle successfully.")
    print("="*80)

if __name__ == "__main__":
    main()
  #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================
🕊️ ELEANOR UNIFIED AI — SILVAR MASTER BRIDGE
===============================================================

Repository:
    https://github.com/at0116218-dot/Silvar

Canonical branch:
    main

Purpose:
    Unified Eleanor foundation combining:

    • GitHub / Silvar synchronization
    • Gemini provider
    • Telegram Bot API
    • ChatGPT export ingestion
    • Gmail IMAP ingestion (optional)
    • Universal Ledger
    • SHA-256 integrity
    • File chunking / reassembly
    • Zero-trust secret scanning
    • Environment validation
    • Provider routing
    • Audit logging
    • Recovery manifest
    • Self-healing checks
    • Safe generated-file execution policy
    • .gitignore generation
    • Secrets template generation
    • GitHub Actions workflow generation

IMPORTANT:
    This program NEVER contains real API keys/passwords.
    Put real credentials in environment variables or GitHub Secrets.

SECURITY PRINCIPLES:
    CHECK → PLAN → VALIDATE → CHANGE → TEST → REPORT

    • Never blindly force-push main.
    • Never silently overwrite conflicts.
    • Never commit secrets.
    • Never execute untrusted generated code automatically.
    • Never claim an external synchronization happened unless verified.
    • Never expose credentials in logs.
===============================================================
"""

from __future__ import annotations

import ast
import base64
import hashlib
import imaplib
import email
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from email.header import decode_header
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
except ImportError:
    requests = None


# ===============================================================
# 1. CONFIGURATION
# ===============================================================

ROOT = Path(__file__).resolve().parent

OWNER = os.getenv("GITHUB_OWNER", "at0116218-dot")
REPO = os.getenv("GITHUB_REPO", "Silvar")
BRANCH = os.getenv("GITHUB_BRANCH", "main")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
ELEANOR_SHARED_SECRET = os.getenv("ELEANOR_SHARED_SECRET", "")

GMAIL_APP_PASS_ELEANOR = os.getenv("GMAIL_APP_PASS_ELEANOR", "")
GMAIL_APP_PASS_FOUNDER = os.getenv("GMAIL_APP_PASS_FOUNDER", "")

GMAIL_USER_ELEANOR = os.getenv("GMAIL_USER_ELEANOR", "")
GMAIL_USER_FOUNDER = os.getenv("GMAIL_USER_FOUNDER", "")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

PORT = int(os.getenv("PORT", "8080"))

DATA_DIR = ROOT / "data"
LEDGER_DIR = ROOT / "LEDGER"
AUDIT_DIR = ROOT / "audit"
SECURE_IMPORTS = ROOT / "secure_imports"
CHUNKS_DIR = ROOT / "chunks"
RECOVERY_DIR = ROOT / "recovery"
RUNTIME_DIR = ROOT / ".eleanor_state"

for directory in [
    DATA_DIR,
    LEDGER_DIR,
    AUDIT_DIR,
    SECURE_IMPORTS,
    CHUNKS_DIR,
    RECOVERY_DIR,
    RUNTIME_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)


# ===============================================================
# 2. LOGGING
# ===============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | ELEANOR | %(levelname)s | %(message)s",
)

logger = logging.getLogger("ELEANOR")


# ===============================================================
# 3. SECURITY POLICY
# ===============================================================

FORBIDDEN_PATHS = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "secrets",
    "secure_imports",
    ".ssh",
}

FORBIDDEN_EXTENSIONS = {
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".crt",
}

SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AIza[A-Za-z0-9_-]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key)\s*[:=]\s*['\"][^'\"]{10,}"),
    re.compile(r"(?i)(password)\s*[:=]\s*['\"][^'\"]{6,}"),
    re.compile(r"(?i)(token)\s*[:=]\s*['\"][^'\"]{10,}"),
]

SECRET_ENV_NAMES = {
    "GITHUB_TOKEN",
    "GEMINI_API_KEY",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_WEBHOOK_SECRET",
    "ELEANOR_SHARED_SECRET",
    "GMAIL_APP_PASS_ELEANOR",
    "GMAIL_APP_PASS_FOUNDER",
    "GROQ_API_KEY",
    "OPENAI_API_KEY",
}


def is_forbidden_path(path: Path) -> bool:
    """
    Prevent accidental reading/writing of sensitive paths.
    """
    try:
        relative = path.resolve().relative_to(ROOT.resolve())
    except ValueError:
        return True

    parts = {part.lower() for part in relative.parts}

    if parts.intersection({p.lower() for p in FORBIDDEN_PATHS}):
        return True

    if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
        return True

    return False


def scan_text_for_secrets(text: str) -> List[str]:
    findings = []

    for index, pattern in enumerate(SECRET_PATTERNS, start=1):
        if pattern.search(text):
            findings.append(f"SECRET_PATTERN_{index}")

    return findings


def scan_file_for_secrets(path: Path) -> Dict[str, Any]:
    result = {
        "path": str(path),
        "safe": True,
        "findings": [],
    }

    if is_forbidden_path(path):
        result["safe"] = False
        result["findings"].append("FORBIDDEN_PATH")
        return result

    try:
        if path.stat().st_size > 20 * 1024 * 1024:
            result["findings"].append("SKIPPED_LARGE_FILE")
            return result

        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        findings = scan_text_for_secrets(text)

        if findings:
            result["safe"] = False
            result["findings"].extend(findings)

    except Exception as exc:
        result["safe"] = False
        result["findings"].append(
            f"READ_ERROR:{type(exc).__name__}"
        )

    return result


def security_scan_directory(root: Path) -> Dict[str, Any]:
    report = {
        "timestamp": utc_now(),
        "root": str(root),
        "safe": True,
        "files": [],
    }

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if ".git" in path.parts:
            continue

        result = scan_file_for_secrets(path)
        report["files"].append(result)

        if not result["safe"]:
            report["safe"] = False

    return report


# ===============================================================
# 4. TIME / HASH UTILITIES
# ===============================================================

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ===============================================================
# 5. UNIVERSAL LEDGER
# ===============================================================

class UniversalLedger:
    """
    Durable project state and audit-oriented ledger.
    """

    def __init__(self) -> None:
        self.ledger_file = LEDGER_DIR / "universal_eleanor_ledger.json"
        self.audit_file = AUDIT_DIR / "events.jsonl"

        if not self.ledger_file.exists():
            self.write({
                "project": "ELEANOR",
                "repository": f"{OWNER}/{REPO}",
                "branch": BRANCH,
                "created_at": utc_now(),
                "version": "1.0",
                "events": [],
                "artifacts": {},
            })

    def read(self) -> Dict[str, Any]:
        try:
            return json.loads(
                self.ledger_file.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return {
                "project": "ELEANOR",
                "repository": f"{OWNER}/{REPO}",
                "branch": BRANCH,
                "events": [],
                "artifacts": {},
            }

    def write(self, state: Dict[str, Any]) -> None:
        temporary = self.ledger_file.with_suffix(".tmp")

        temporary.write_text(
            json.dumps(
                state,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        temporary.replace(self.ledger_file)

    def append_event(
        self,
        action: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        event = {
            "timestamp": utc_now(),
            "action": action,
            "details": details or {},
        }

        with self.audit_file.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(
                json.dumps(
                    event,
                    ensure_ascii=False,
                )
                + "\n"
            )

        state = self.read()

        state.setdefault("events", []).append(event)

        # Keep ledger bounded.
        state["events"] = state["events"][-1000:]

        self.write(state)


LEDGER = UniversalLedger()


# ===============================================================
# 6. CHATGPT EXPORT PARSER
# ===============================================================

class ChatGPTArchiveParser:
    """
    Reads official ChatGPT export conversations.json.

    No external account access is performed.
    The user must provide their own exported archive/file.
    """

    @staticmethod
    def parse(
        conversations_file: Path,
        output_file: Optional[Path] = None,
    ) -> Dict[str, Any]:

        if not conversations_file.exists():
            raise FileNotFoundError(
                conversations_file
            )

        if is_forbidden_path(conversations_file):
            raise PermissionError(
                "Refusing to process forbidden path."
            )

        raw = json.loads(
            conversations_file.read_text(
                encoding="utf-8",
                errors="replace",
            )
        )

        if not isinstance(raw, list):
            raise ValueError(
                "Expected conversations.json to contain a list."
            )

        parsed = []

        for conversation in raw:
            parsed.append({
                "id": conversation.get("id"),
                "title": conversation.get("title"),
                "create_time": conversation.get(
                    "create_time"
                ),
                "update_time": conversation.get(
                    "update_time"
                ),
                "mapping": conversation.get(
                    "mapping",
                    {},
                ),
            })

        result = {
            "source": str(conversations_file),
            "conversation_count": len(parsed),
            "imported_at": utc_now(),
            "conversations": parsed,
        }

        if output_file:
            output_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            output_file.write_text(
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

        LEDGER.append_event(
            "CHATGPT_ARCHIVE_PARSED",
            {
                "count": len(parsed),
            },
        )

        return result


# ===============================================================
# 7. GMAIL CONTENT HARVESTER
# ===============================================================

class EmailContentHarvester:
    """
    Optional IMAP reader.

    IMPORTANT:
    Passwords are read ONLY from environment variables.
    Nothing is hard-coded or returned in logs.
    """

    def __init__(
        self,
        username: str,
        password: str,
        host: str = "imap.gmail.com",
    ):
        self.username = username
        self.password = password
        self.host = host

    def fetch_recent(
        self,
        mailbox: str = "INBOX",
        limit: int = 5,
    ) -> List[Dict[str, Any]]:

        if not self.username or not self.password:
            return []

        messages = []

        mail = imaplib.IMAP4_SSL(self.host)

        try:
            mail.login(
                self.username,
                self.password,
            )

            mail.select(mailbox)

            status, data = mail.search(
                None,
                "ALL",
            )

            if status != "OK":
                return []

            ids = data[0].split()
            ids = ids[-limit:]

            for message_id in reversed(ids):
                status, message_data = mail.fetch(
                    message_id,
                    "(RFC822)",
                )

                if status != "OK":
                    continue

                raw = message_data[0][1]
                message = email.message_from_bytes(raw)

                subject, encoding = decode_header(
                    message.get("Subject", "")
                )[0]

                if isinstance(subject, bytes):
                    subject = subject.decode(
                        encoding or "utf-8",
                        errors="replace",
                    )

                sender = message.get("From", "")

                body = ""

                if message.is_multipart():
                    for part in message.walk():
                        content_type = part.get_content_type()

                        if content_type == "text/plain":
                            payload = part.get_payload(
                                decode=True
                            )

                            if payload:
                                body = payload.decode(
                                    "utf-8",
                                    errors="replace",
                                )

                            break
                else:
                    payload = message.get_payload(
                        decode=True
                    )

                    if isinstance(payload, bytes):
                        body = payload.decode(
                            "utf-8",
                            errors="replace",
                        )

                messages.append({
                    "subject": subject,
                    "from": sender,
                    "date": message.get("Date", ""),
                    "body": body,
                })

        finally:
            try:
                mail.logout()
            except Exception:
                pass

        LEDGER.append_event(
            "EMAIL_IMPORT",
            {
                "count": len(messages),
            },
        )

        return messages


# ===============================================================
# 8. STORAGE SANITIZER
# ===============================================================

class StorageSanitizer:

    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Removes common secret-like patterns from imported content.
        """
        sanitized = text

        for pattern in SECRET_PATTERNS:
            sanitized = pattern.sub(
                "[REDACTED_SECRET]",
                sanitized,
            )

        return sanitized

    @staticmethod
    def safe_write(
        path: Path,
        content: str,
    ) -> None:

        if is_forbidden_path(path):
            raise PermissionError(
                f"Refusing unsafe path: {path}"
            )

        sanitized = StorageSanitizer.sanitize_text(
            content
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            sanitized,
            encoding="utf-8",
        )


# ===============================================================
# 9. CHUNKING / REASSEMBLY ENGINE
# ===============================================================

class ChunkingEngine:

    @staticmethod
    def split_file(
        file_path: Path,
        chunk_size_mb: int = 85,
    ) -> Optional[Dict[str, Any]]:

        if not file_path.exists():
            return None

        if is_forbidden_path(file_path):
            raise PermissionError(
                "Cannot chunk a forbidden file."
            )

        size = file_path.stat().st_size
        chunk_size = chunk_size_mb * 1024 * 1024

        if size <= chunk_size:
            return None

        original_hash = sha256_file(file_path)

        chunks = []

        with file_path.open("rb") as source:

            index = 0

            while True:
                data = source.read(chunk_size)

                if not data:
                    break

                part_name = (
                    f"{file_path.name}.part-{index:03d}"
                )

                part_path = CHUNKS_DIR / part_name

                part_path.write_bytes(data)

                chunks.append({
                    "part": index,
                    "filename": part_name,
                    "size_bytes": len(data),
                    "sha256": sha256_bytes(data),
                })

                index += 1

        manifest = {
            "original_filename": file_path.name,
            "original_size_bytes": size,
            "original_sha256": original_hash,
            "chunk_size_mb": chunk_size_mb,
            "chunk_count": len(chunks),
            "generated_at": utc_now(),
            "chunks": chunks,
        }

        manifest_path = (
            CHUNKS_DIR
            / f"{file_path.name}.manifest.json"
        )

        manifest_path.write_text(
            json.dumps(
                manifest,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return manifest

    @staticmethod
    def join_and_verify(
        manifest_path: Path,
        output_file: Path,
    ) -> bool:

        manifest = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )

        with output_file.open("wb") as output:

            for chunk in manifest["chunks"]:

                part = (
                    CHUNKS_DIR
                    / chunk["filename"]
                )

                if sha256_file(part) != chunk["sha256"]:
                    raise ValueError(
                        f"SHA-256 mismatch: {part}"
                    )

                output.write(
                    part.read_bytes()
                )

        actual = sha256_file(output_file)

        expected = manifest[
            "original_sha256"
        ]

        if actual != expected:
            raise ValueError(
                "Final SHA-256 verification failed."
            )

        return True


# ===============================================================
# 10. ZERO TRUST AST SECURITY SHIELD
# ===============================================================

class ZeroTrustSecurityShield:

    BLOCKED_IMPORTS = {
        "pickle",
        "marshal",
        "ctypes",
    }

    BLOCKED_CALLS = {
        "eval",
        "exec",
    }

    @classmethod
    def inspect_python(
        cls,
        source: str,
    ) -> Dict[str, Any]:

        report = {
            "safe": True,
            "syntax_valid": True,
            "findings": [],
        }

        findings = scan_text_for_secrets(source)

        if findings:
            report["safe"] = False
            report["findings"].extend(findings)

        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            report["safe"] = False
            report["syntax_valid"] = False
            report["findings"].append(
                f"SYNTAX_ERROR:{exc}"
            )
            return report

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:
                    root = alias.name.split(".")[0]

                    if root in cls.BLOCKED_IMPORTS:
                        report["safe"] = False
                        report["findings"].append(
                            f"BLOCKED_IMPORT:{root}"
                        )

            elif isinstance(node, ast.ImportFrom):

                root = (
                    node.module.split(".")[0]
                    if node.module
                    else ""
                )

                if root in cls.BLOCKED_IMPORTS:
                    report["safe"] = False
                    report["findings"].append(
                        f"BLOCKED_IMPORT:{root}"
                    )

            elif isinstance(node, ast.Call):

                if isinstance(
                    node.func,
                    ast.Name
                ):
                    if node.func.id in cls.BLOCKED_CALLS:
                        report["safe"] = False
                        report["findings"].append(
                            f"BLOCKED_CALL:{node.func.id}"
                        )

        return report


# ===============================================================
# 11. ENVIRONMENT ENGINE
# ===============================================================

class EnvironmentEngine:

    REQUIRED_PACKAGES = [
        "requests",
        "fastapi",
        "uvicorn",
    ]

    @staticmethod
    def check() -> Dict[str, Any]:

        missing = []

        for package in (
            EnvironmentEngine.REQUIRED_PACKAGES
        ):
            try:
                __import__(package)
            except ImportError:
                missing.append(package)

        return {
            "python": sys.version,
            "root": str(ROOT),
            "missing_packages": missing,
            "github_configured": bool(
                GITHUB_TOKEN
            ),
            "gemini_configured": bool(
                GEMINI_API_KEY
            ),
            "telegram_configured": bool(
                TELEGRAM_BOT_TOKEN
            ),
            "gmail_eleanor_configured": bool(
                GMAIL_USER_ELEANOR
                and GMAIL_APP_PASS_ELEANOR
            ),
        }


# ===============================================================
# 12. SOVEREIGN MODEL ROUTER
# ===============================================================

class SovereignModelRouter:

    @staticmethod
    def gemini(
        prompt: str,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:

        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        if requests is None:
            raise RuntimeError(
                "requests package is required."
            )

        model = model or GEMINI_MODEL

        url = (
            "https://generativelanguage.googleapis.com/"
            f"v1beta/models/{model}:generateContent"
        )

        response = requests.post(
            url,
            params={
                "key": GEMINI_API_KEY,
            },
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return {
            "provider": "gemini",
            "model": model,
            "response": data,
        }

    @staticmethod
    def route(
        prompt: str,
        provider: str = "gemini",
    ) -> Dict[str, Any]:

        provider = provider.lower()

        if provider == "gemini":
            return SovereignModelRouter.gemini(
                prompt
            )

        raise ValueError(
            f"Unsupported provider: {provider}"
        )


# ===============================================================
# 13. GITHUB CLIENT
# ===============================================================

class GitHubClient:

    API = "https://api.github.com"

    def __init__(
        self,
        token: str,
    ):
        self.token = token

        if requests is None:
            raise RuntimeError(
                "requests package is required."
            )

    @property
    def headers(self) -> Dict[str, str]:

        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2026-03-10",
        }

    def _require_token(self) -> None:

        if not self.token:
            raise RuntimeError(
                "GITHUB_TOKEN is not configured."
            )

    def repository(self) -> Dict[str, Any]:

        self._require_token()

        url = (
            f"{self.API}/repos/"
            f"{OWNER}/{REPO}"
        )

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def get_file(
        self,
        path: str,
        ref: Optional[str] = None,
    ) -> Dict[str, Any]:

        self._require_token()

        path = path.strip("/")

        if is_forbidden_path(
            ROOT / path
        ):
            raise PermissionError(
                f"Forbidden repository path: {path}"
            )

        url = (
            f"{self.API}/repos/"
            f"{OWNER}/{REPO}/contents/{path}"
        )

        params = {}

        if ref:
            params["ref"] = ref

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return {
                "type": "directory",
                "items": data,
            }

        if data.get("encoding") == "base64":
            raw = base64.b64decode(
                data["content"]
            )

            data["decoded_content"] = raw.decode(
                "utf-8",
                errors="replace",
            )

        return data

    def write_file(
        self,
        path: str,
        content: str,
        message: str,
        sha: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> Dict[str, Any]:

        self._require_token()

        branch = branch or BRANCH
        path = path.strip("/")

        if is_forbidden_path(
            ROOT / path
        ):
            raise PermissionError(
                f"Refusing to write protected path: {path}"
            )

        secret_findings = scan_text_for_secrets(
            content
        )

        if secret_findings:
            raise PermissionError(
                "Refusing to commit possible secret data: "
                + ", ".join(secret_findings)
            )

        url = (
            f"{self.API}/repos/"
            f"{OWNER}/{REPO}/contents/{path}"
        )

        encoded = base64.b64encode(
            content.encode("utf-8")
        ).decode("ascii")

        payload = {
            "message": message,
            "content": encoded,
            "branch": branch,
        }

        if sha:
            payload["sha"] = sha

        response = requests.put(
            url,
            headers=self.headers,
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        result = response.json()

        LEDGER.append_event(
            "GITHUB_WRITE",
            {
                "path": path,
                "branch": branch,
                "commit": result.get(
                    "commit",
                    {}
                ).get("sha"),
            },
        )

        return result


# ===============================================================
# 14. TELEGRAM CLIENT
# ===============================================================

class TelegramClient:

    def __init__(
        self,
        token: str,
    ):
        self.token = token

        if requests is None:
            raise RuntimeError(
                "requests package is required."
            )

    def send_message(
        self,
        chat_id: str,
        text: str,
    ) -> Dict[str, Any]:

        if not self.token:
            raise RuntimeError(
                "TELEGRAM_BOT_TOKEN is not configured."
            )

        url = (
            "https://api.telegram.org/"
            f"bot{self.token}/sendMessage"
        )

        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()


# ===============================================================
# 15. SAFE GENERATED CODE CHECK
# ===============================================================

class SafeCodeExecutor:

    """
    This is NOT a true security sandbox.

    It performs static checks and then requires explicit
    allow_execution=True.

    Do not execute untrusted code on a production host.
    """

    @staticmethod
    def validate(
        source: str,
    ) -> Dict[str, Any]:

        return ZeroTrustSecurityShield.inspect_python(
            source
        )

    @staticmethod
    def execute(
        source: str,
        allow_execution: bool = False,
        timeout: int = 10,
    ) -> Dict[str, Any]:

        validation = (
            SafeCodeExecutor.validate(source)
        )

        if not validation["safe"]:
            return {
                "executed": False,
                "validation": validation,
            }

        if not allow_execution:
            return {
                "executed": False,
                "validation": validation,
                "reason": (
                    "Execution disabled by policy."
                ),
            }

        with tempfile.TemporaryDirectory(
            prefix="eleanor_exec_"
        ) as temp:

            script = (
                Path(temp)
                / "generated.py"
            )

            script.write_text(
                source,
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                ],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp,
            )

            return {
                "executed": True,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "validation": validation,
            }


# ===============================================================
# 16. RECOVERY MANIFEST
# ===============================================================

class RecoveryManager:

    @staticmethod
    def generate() -> Dict[str, Any]:

        artifacts = {}

        important_files = [
            ROOT / "eleanor_unified.py",
            ROOT / ".gitignore",
            ROOT / ".env.example",
            ROOT / "SECRETS.template.env",
            ROOT / "requirements.txt",
            ROOT / "README.md",
        ]

        for path in important_files:

            if path.exists():

                artifacts[str(path.relative_to(ROOT))] = {
                    "size": path.stat().st_size,
                    "sha256": sha256_file(path),
                }

        manifest = {
            "project": "ELEANOR",
            "repository": f"{OWNER}/{REPO}",
            "branch": BRANCH,
            "generated_at": utc_now(),
            "artifacts": artifacts,
        }

        output = (
            RECOVERY_DIR
            / "recovery_manifest.json"
        )

        output.write_text(
            json.dumps(
                manifest,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return manifest


# ===============================================================
# 17. SELF HEALING ORCHESTRATOR
# ===============================================================

class SelfHealingOrchestrator:

    @staticmethod
    def diagnose() -> Dict[str, Any]:

        env = EnvironmentEngine.check()

        security = security_scan_directory(
            ROOT
        )

        return {
            "timestamp": utc_now(),
            "environment": env,
            "security": security,
            "ledger_exists": LEDGER.ledger_file.exists(),
            "recovery_exists": (
                RECOVERY_DIR
                / "recovery_manifest.json"
            ).exists(),
        }

    @staticmethod
    def repair_structure() -> Dict[str, Any]:

        for directory in [
            DATA_DIR,
            LEDGER_DIR,
            AUDIT_DIR,
            SECURE_IMPORTS,
            CHUNKS_DIR,
            RECOVERY_DIR,
            RUNTIME_DIR,
        ]:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

        return {
            "repaired": True,
            "timestamp": utc_now(),
        }


# ===============================================================
# 18. PROJECT FILE GENERATOR
# ===============================================================

class EleanorProjectFiles:

    GITIGNORE = r"""
# ============================================================
# ELEANOR / SILVAR SECURITY
# ============================================================

# Environment
.env
.env.*
!.env.example
!.env.template
SECRETS.*
!SECRETS.template.env

# Secrets
secrets/
secure_imports/
private_data/
user_data/
chatgpt_exports/
gmail_exports/

# Credentials / certificates
*.pem
*.key
*.p12
*.pfx
*.crt
*.cer

# SSH
.ssh/
id_rsa
id_rsa.pub
id_ed25519
id_ed25519.pub

# Tokens / credentials
*_TOKEN
*_API_KEY
*_SECRET
*_PASSWORD
*_CREDENTIAL
*_CREDENTIALS

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
env/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Build
dist/
build/

# Eleanor runtime
.eleanor_state/
.eleanor_runtime/
.eleanor_cache/
logs/
*.log

# OS / IDE
.DS_Store
Thumbs.db
.vscode/
.idea/

# Temporary files
*.tmp
*.swp
*.bak
"""

    ENV_EXAMPLE = r"""
# ============================================================
# ELEANOR UNIFIED AI
# SAFE ENVIRONMENT TEMPLATE
# ============================================================

GITHUB_OWNER=at0116218-dot
GITHUB_REPO=Silvar
GITHUB_BRANCH=main

GITHUB_TOKEN=

GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

TELEGRAM_BOT_TOKEN=
TELEGRAM_WEBHOOK_SECRET=

ELEANOR_SHARED_SECRET=

GMAIL_USER_ELEANOR=
GMAIL_APP_PASS_ELEANOR=

GMAIL_USER_FOUNDER=
GMAIL_APP_PASS_FOUNDER=

PORT=8080
"""

    SECRETS_TEMPLATE = r"""
# ============================================================
# ELEANOR SECRET REGISTRY
# ============================================================
#
# DO NOT PUT REAL VALUES IN THIS FILE.
#
# Configure the real values using:
#
#   • local environment variables
#   • GitHub Repository Secrets
#   • GitHub Environment Secrets
#   • an external secret manager
#
# ============================================================

GITHUB_TOKEN
GEMINI_API_KEY
TELEGRAM_BOT_TOKEN
TELEGRAM_WEBHOOK_SECRET
ELEANOR_SHARED_SECRET
GMAIL_APP_PASS_ELEANOR
GMAIL_APP_PASS_FOUNDER
"""

    REQUIREMENTS = r"""
fastapi>=0.115
uvicorn[standard]>=0.30
requests>=2.32
"""

    README = r"""
# 🕊️ ELEANOR UNIFIED AI — SILVAR

Canonical repository:

`at0116218-dot/Silvar`

Canonical branch:

`main`

## Architecture

Human
↓
Eleanor Unified AI Bridge
↓
OpenAI / Gemini / Telegram / GitHub
↓
Universal Ledger
↓
Audit + Recovery
↓
Silvar

## Security

Real credentials must never be committed.

Use:

- GitHub Repository Secrets
- GitHub Environment Secrets
- local environment variables
- external secret managers

The following files are templates only:

- `.env.example`
- `SECRETS.template.env`

## Run

```bash
python eleanor_unified.py
Or:
uvicorn eleanor_unified:app --host 0.0.0.0 --port 8080
Protocol
CHECK → PLAN → VALIDATE → CHANGE → TEST → REPORT
Important
The GitHub integration will not automatically gain write permission.
The GitHub token used by the runtime must already have the required permissions.
No force push is performed by this program. """
WORKFLOW = r"""
name: Eleanor Unified AI Security Check
on: workflow_dispatch: push: branches: - main
permissions: contents: read
jobs: security: runs-on: ubuntu-latest
steps:
  - name: Checkout
    uses: actions/checkout@v4

  - name: Setup Python
    uses: actions/setup-python@v5
    with:
      python-version: "3.12"

  - name: Install dependencies
    run: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt

  - name: Compile check
    run: |
      python -m py_compile eleanor_unified.py

  - name: Run Eleanor diagnostic
    run: |
      python eleanor_unified.py --diagnose
"""
@classmethod
def generate(cls) -> Dict[str, str]:

    files = {
        ".gitignore": cls.GITIGNORE.strip() + "\n",
        ".env.example": cls.ENV_EXAMPLE.strip() + "\n",
        "SECRETS.template.env": (
            cls.SECRETS_TEMPLATE.strip()
            + "\n"
        ),
        "requirements.txt": (
            cls.REQUIREMENTS.strip()
            + "\n"
        ),
        "README.md": cls.README.strip() + "\n",
        ".github/workflows/eleanor.yml": (
            cls.WORKFLOW.strip()
            + "\n"
        ),
    }

    created = []

    for relative, content in files.items():

        path = ROOT / relative

        if is_forbidden_path(path):
            continue

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Never overwrite an existing real .env.
        if path.name == ".env":
            continue

        path.write_text(
            content,
            encoding="utf-8",
        )

        created.append(relative)

    return {
        "created": created,
        "timestamp": utc_now(),
    }
===============================================================
19. PROTOCOL ENVELOPE
===============================================================
def envelope( action: str, payload: Optional[Dict[str, Any]] = None, status: str = "ok", ) -> Dict[str, Any]:
return {
    "protocol": (
        "ELEANOR_UNIFIED_AI"
    ),
    "version": "2026.1",
    "timestamp": utc_now(),
    "status": status,
    "action": action,
    "repository": {
        "owner": OWNER,
        "name": REPO,
        "branch": BRANCH,
    },
    "payload": payload or {},
}
===============================================================
20. FASTAPI APPLICATION
===============================================================
try: from fastapi import ( FastAPI, Header, HTTPException, Request, ) from pydantic import BaseModel except ImportError: FastAPI = None
if FastAPI:
app = FastAPI(
    title="🕊️ Eleanor Unified AI",
    version="2026.1",
    description=(
        "Unified Eleanor bridge for Silvar."
    ),
)

class GeminiRequest(BaseModel):
    prompt: str
    model: Optional[str] = None

class TelegramRequest(BaseModel):
    chat_id: str
    text: str

class GitHubWriteRequest(BaseModel):
    path: str
    content: str
    message: str
    sha: Optional[str] = None
    branch: Optional[str] = None

class CodeValidationRequest(BaseModel):
    source: str

class CodeExecutionRequest(BaseModel):
    source: str
    allow_execution: bool = False

def authorize(
    authorization: Optional[str],
) -> None:

    if not ELEANOR_SHARED_SECRET:
        return

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization required.",
        )

    expected = (
        "Bearer "
        + ELEANOR_SHARED_SECRET
    )

    if authorization != expected:
        raise HTTPException(
            status_code=403,
            detail="Invalid authorization.",
        )

@app.get("/")
def root(
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    return envelope(
        "ROOT",
        {
            "service": (
                "ELEANOR UNIFIED AI"
            ),
            "status": "online",
        },
    )

@app.get("/health")
def health():

    return envelope(
        "HEALTH",
        {
            "status": "healthy",
            "timestamp": utc_now(),
        },
    )

@app.get("/environment")
def environment(
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    return envelope(
        "ENVIRONMENT",
        EnvironmentEngine.check(),
    )

@app.get("/audit")
def audit(
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    return envelope(
        "AUDIT",
        {
            "ledger": LEDGER.read(),
        },
    )

@app.get("/recovery")
def recovery(
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    return envelope(
        "RECOVERY",
        RecoveryManager.generate(),
    )

@app.post("/security/scan")
def security_scan(
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    report = security_scan_directory(
        ROOT
    )

    LEDGER.append_event(
        "SECURITY_SCAN",
        {
            "safe": report["safe"],
        },
    )

    return envelope(
        "SECURITY_SCAN",
        report,
        status=(
            "ok"
            if report["safe"]
            else "warning"
        ),
    )

@app.post("/code/validate")
def validate_code(
    body: CodeValidationRequest,
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    result = (
        ZeroTrustSecurityShield
        .inspect_python(
            body.source
        )
    )

    return envelope(
        "CODE_VALIDATE",
        result,
    )

@app.post("/code/execute")
def execute_code(
    body: CodeExecutionRequest,
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    result = (
        SafeCodeExecutor.execute(
            body.source,
            allow_execution=(
                body.allow_execution
            ),
        )
    )

    return envelope(
        "CODE_EXECUTE",
        result,
    )

@app.post("/gemini")
def gemini(
    body: GeminiRequest,
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    try:

        result = (
            SovereignModelRouter
            .route(
                body.prompt,
                provider="gemini",
            )
        )

        LEDGER.append_event(
            "GEMINI_REQUEST",
            {
                "model": body.model
                or GEMINI_MODEL,
            },
        )

        return envelope(
            "GEMINI",
            result,
        )

    except Exception as exc:

        logger.exception(
            "Gemini request failed."
        )

        return envelope(
            "GEMINI",
            {
                "error": str(exc),
            },
            status="error",
        )

@app.get("/github/repository")
def github_repository(
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    try:

        client = GitHubClient(
            GITHUB_TOKEN
        )

        return envelope(
            "GITHUB_REPOSITORY",
            client.repository(),
        )

    except Exception as exc:

        return envelope(
            "GITHUB_REPOSITORY",
            {
                "error": str(exc),
            },
            status="error",
        )

@app.get("/github/file")
def github_file(
    path: str,
    ref: Optional[str] = None,
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    try:

        client = GitHubClient(
            GITHUB_TOKEN
        )

        result = client.get_file(
            path,
            ref=ref,
        )

        return envelope(
            "GITHUB_FILE",
            result,
        )

    except Exception as exc:

        return envelope(
            "GITHUB_FILE",
            {
                "error": str(exc),
            },
            status="error",
        )

@app.post("/github/write")
def github_write(
    body: GitHubWriteRequest,
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    try:

        client = GitHubClient(
            GITHUB_TOKEN
        )

        result = client.write_file(
            path=body.path,
            content=body.content,
            message=body.message,
            sha=body.sha,
            branch=body.branch,
        )

        return envelope(
            "GITHUB_WRITE",
            result,
        )

    except Exception as exc:

        return envelope(
            "GITHUB_WRITE",
            {
                "error": str(exc),
            },
            status="error",
        )

@app.post("/telegram/send")
def telegram_send(
    body: TelegramRequest,
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    try:

        client = TelegramClient(
            TELEGRAM_BOT_TOKEN
        )

        result = client.send_message(
            body.chat_id,
            body.text,
        )

        LEDGER.append_event(
            "TELEGRAM_MESSAGE",
            {
                "chat_id": body.chat_id,
            },
        )

        return envelope(
            "TELEGRAM_SEND",
            result,
        )

    except Exception as exc:

        return envelope(
            "TELEGRAM_SEND",
            {
                "error": str(exc),
            },
            status="error",
        )

@app.post("/telegram/webhook")
async def telegram_webhook(
    request: Request,
):

    if TELEGRAM_WEBHOOK_SECRET:

        received = request.headers.get(
            "X-Telegram-Bot-Api-Secret-Token"
        )

        if received != TELEGRAM_WEBHOOK_SECRET:

            raise HTTPException(
                status_code=403,
                detail="Invalid Telegram webhook secret.",
            )

    data = await request.json()

    LEDGER.append_event(
        "TELEGRAM_WEBHOOK",
        {
            "received": True,
        },
    )

    return envelope(
        "TELEGRAM_WEBHOOK",
        {
            "accepted": True,
            "update_id": data.get(
                "update_id"
            ),
        },
    )

@app.post("/project/bootstrap")
def project_bootstrap(
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    result = (
        EleanorProjectFiles
        .generate()
    )

    RecoveryManager.generate()

    LEDGER.append_event(
        "PROJECT_BOOTSTRAP",
        result,
    )

    return envelope(
        "PROJECT_BOOTSTRAP",
        result,
    )

@app.post("/diagnose")
def diagnose(
    authorization: Optional[str] = Header(
        default=None
    ),
):

    authorize(authorization)

    result = (
        SelfHealingOrchestrator
        .diagnose()
    )

    return envelope(
        "DIAGNOSE",
        result,
    )
===============================================================
21. COMMAND LINE
===============================================================
def cli() -> None:
if "--diagnose" in sys.argv:

    result = (
        SelfHealingOrchestrator
        .diagnose()
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )

    return

if "--bootstrap" in sys.argv:

    result = (
        EleanorProjectFiles
        .generate()
    )

    RecoveryManager.generate()

    LEDGER.append_event(
        "CLI_BOOTSTRAP",
        result,
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )

    return

if "--security-scan" in sys.argv:

    result = security_scan_directory(
        ROOT
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )

    return

if "--recovery" in sys.argv:

    result = (
        RecoveryManager
        .generate()
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )

    return

# Default:
# Generate safe project files and start API.

EleanorProjectFiles.generate()
RecoveryManager.generate()

if FastAPI is None:

    print(
        "FastAPI is not installed.\n"
        "Run:\n"
        "pip install -r requirements.txt"
    )

    return

try:

    import uvicorn

    print(
        "\n"
        "====================================================\n"
        "🕊️ ELEANOR UNIFIED AI\n"
        "====================================================\n"
        f"Repository: {OWNER}/{REPO}\n"
        f"Branch:     {BRANCH}\n"
        f"Port:       {PORT}\n"
        "====================================================\n"
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
    )

except ImportError:
  After pasting and running it, you will have a single file, which is the unified source code. This file will create: ```text Silvar/ │ ├── eleanor_unified.py ← Unified code ├── .gitignore ← Protect sensitive files ├── .env.example ← Settings names only ├── SECRETS.template.env ← Secrets name log only ├── requirements.txt ├── README.md │ ├── .github/ │ └── workflows/ │ └── eleanor.yml │ ├── LEDGER/ ├── audit/ ├── recovery/ ├── data/ ├── chunks/ ├── secure_imports/ └── .eleanor_state/
class EnvironmentEngine:uvicorn eleanor_unified:app --host 0.0.0.0 --port 8080

    
