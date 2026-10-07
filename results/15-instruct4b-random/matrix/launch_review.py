"""Launch one read-only Claude reviewer (VK AI Proxy profile), same pattern as ../launch_claude.py."""
import json, os, subprocess
from pathlib import Path
d = Path(__file__).resolve().parent / 'parallel_check_review'
profile = Path('/Users/v.charkin/.claude/settings.json'); settings = json.loads(profile.read_text())
endpoint = settings['env']['ANTHROPIC_BASE_URL']; assert endpoint == 'https://ai-proxy.vk.team/direct/anthropic'
if (d / 'launch.json').exists(): raise RuntimeError('already launched')
env = {k: v for k, v in os.environ.items() if not k.startswith('ANTHROPIC_') and k != 'CLAUDE_CODE_SUBAGENT_MODEL'}; env.update(settings['env'])
cmd = ['/Users/v.charkin/.local/bin/claude', '-p', '--settings', str(profile), '--setting-sources', '', '--strict-mcp-config',
       '--mcp-config', '{"mcpServers":{}}', '--tools', 'Read,Write,Grep,Glob,Bash', '--allowedTools', 'Read,Write,Grep,Glob,Bash',
       '--permission-mode', 'dontAsk', '--output-format', 'json',
       '--add-dir', '/Users/v.charkin/Documents/dev/projects/parallel-r1-instruct4b-filtered', str(d.parent), '/tmp',
       '--agents', json.dumps({'review': {'description': 'Independent read-only review of a parallel eval post-check finding',
                                          'prompt': 'Read-only. Independent assessment. Use VK AI Proxy only. No credentials.'}}),
       '--agent', 'review', '--model', settings['model']]
with (d / 'response.json').open('w') as so, (d / 'stderr.log').open('w') as se:
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=so, stderr=se, env=env, cwd=d, start_new_session=True)
    p.stdin.write((d / 'task.md').read_bytes()); p.stdin.close()
(d / 'launch.json').write_text(json.dumps({'pid': p.pid, 'model': settings['model'], 'endpoint': endpoint, 'task': str(d / 'task.md')}, indent=2))
print('review', p.pid)
