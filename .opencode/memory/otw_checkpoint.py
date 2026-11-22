#!/usr/bin/env python3
"""Atomically checkpoint one OverTheWire level into otw_campaign_state.json.

Usage:
  python3 otw_checkpoint.py '{"wargame":"bandit","level":1,"status":"solved",
      "password":"<next-level-password>","attempts":1,
      "commands":["cmd1","cmd2"],"notes":"short note"}'

Fields:
  wargame, level, status (solved|NEEDS_RETRY|in_progress), password (credential
  for the NEXT level), attempts, commands (list), notes, blocker (optional).
Also advances state.next to the following level when status == solved.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE = Path(__file__).resolve().parent / 'otw_campaign_state.json'
ORDER = ['bandit', 'natas', 'krypton', 'leviathan', 'narnia', 'behemoth',
         'utumno', 'maze', 'vortex', 'manpage', 'drifter', 'formulaone']

def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    update = json.loads(sys.argv[1])
    state = json.loads(STATE.read_text())
    game = update['wargame']
    level = int(update['level'])
    status = update['status']

    entry = state['wargames'][game]['levels'].setdefault(str(level), {})
    entry.update({
        'status': status,
        'attempts': int(update.get('attempts', entry.get('attempts', 0))),
        'commands': update.get('commands', entry.get('commands', [])),
        'notes': update.get('notes', entry.get('notes', '')),
        'updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    })
    if update.get('blocker'):
        entry['blocker'] = update['blocker']
    if update.get('password'):
        entry['password_for_next'] = update['password']

    state['stats']['attempts'] += int(update.get('attempts', 0))
    if status == 'solved':
        state['stats']['solved'] = sum(
            1 for g in state['wargames'].values()
            for l in g['levels'].values() if l.get('status') == 'solved')
    elif status == 'NEEDS_RETRY':
        state['stats']['needs_retry'] = sum(
            1 for g in state['wargames'].values()
            for l in g['levels'].values() if l.get('status') == 'NEEDS_RETRY')

    if status == 'solved':
        nxt = level + 1
        total = state['wargames'][game].get('levels_total')
        if total is not None and nxt >= total:
            idx = ORDER.index(game)
            if idx + 1 < len(ORDER):
                game_n, nxt = ORDER[idx + 1], 0
                prefix = game_n
            else:
                game_n, nxt, prefix = game, nxt, game
        else:
            game_n, prefix = game, game
        state['current_wargame'] = game_n
        state['current_level'] = nxt
        state['next'] = {
            'wargame': game_n, 'level': nxt,
            'username': f'{prefix}{nxt}',
            'password': update.get('password', ''),
        }

    state['last_updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    tmp = STATE.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(state, indent=2) + '\n')
    tmp.replace(STATE)
    print(f"checkpoint: {game} level {level} -> {status}; next={state['next']['wargame']}/{state['next']['level']}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
