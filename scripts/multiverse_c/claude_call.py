"""One plain LLM call through the VK AI Proxy: the local Claude CLI with no tools, the profile's endpoint and model.

Credentials stay in the environment of the child process (copied from ~/.claude/settings.json, never printed or written).
call(system, user) -> {"text", "usage", "cost_usd", "duration_ms", "is_error"}.
"""
import json
import os
import subprocess
from pathlib import Path

PROFILE = Path("/Users/v.charkin/.claude/settings.json")
CLAUDE = "/Users/v.charkin/.local/bin/claude"
ENDPOINT = "https://ai-proxy.vk.team/direct/anthropic"


def _env_and_model():
    settings = json.loads(PROFILE.read_text())
    assert settings["env"]["ANTHROPIC_BASE_URL"] == ENDPOINT
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_") and k != "CLAUDE_CODE_SUBAGENT_MODEL"}
    env.update(settings["env"])
    return env, settings["model"]


def call(system, user, timeout=1800, model=None):
    env, default_model = _env_and_model()
    cmd = [CLAUDE, "-p", "--settings", str(PROFILE), "--setting-sources", "", "--strict-mcp-config",
           "--mcp-config", '{"mcpServers":{}}', "--tools", "", "--output-format", "json",
           "--system-prompt", system, "--model", model or default_model]
    p = subprocess.run(cmd, input=user, capture_output=True, text=True, env=env, timeout=timeout, cwd="/tmp")
    try:
        out = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"text": "", "is_error": True, "error": (p.stderr or p.stdout)[-500:], "usage": {}, "cost_usd": None}
    return {"text": out.get("result", ""), "is_error": bool(out.get("is_error")), "usage": out.get("usage", {}),
            "cost_usd": out.get("total_cost_usd"), "duration_ms": out.get("duration_ms"), "stop_reason": out.get("stop_reason"),
            "model_usage": out.get("modelUsage")}


if __name__ == "__main__":
    r = call("Answer with one word.", "What is the capital of France?")
    print(json.dumps({k: r[k] for k in ("text", "is_error", "usage", "cost_usd", "model_usage")}, indent=1))
