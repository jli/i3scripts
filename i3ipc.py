"""Wrapper around i3-msg for writing script to interact w/ i3wm.

Docs on IPC interface here: http://i3wm.org/docs/ipc.html.

"""

from __future__ import print_function
import json
import subprocess
import sys

import i3tree


def _i3msg(*args):
  """Wrapper around i3-msg. Calls i3-msg w/ all args and parses response."""
  popen = subprocess.Popen(['i3-msg'] + list(args), stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
  stdout, stderr = popen.communicate()
  if stderr:
    print('i3-msg stderr:', stderr, file=sys.stderr)
  return json.loads(stdout)


def command(*cmd):
  """Sends a command via i3-msg."""
  response = _i3msg('-t', 'command', *cmd)
  print(response)
  return response


def get_workspaces():
  """Returns i3 workspaces."""
  return _i3msg('-t', 'get_workspaces')


def get_tree():
  """Returns i3 tree."""
  return i3tree.TreeNode(_i3msg('-t', 'get_tree'))


def focused_workspace():
  """Returns currently focused workspace."""
  workspaces = get_workspaces()
  for ws in workspaces:
    if ws['focused']:
      return ws
  raise RuntimeError('no focused workspace?!', ws)


def focused_output_workspaces():
  """Returns workspaces on currently focused output."""
  workspaces = get_workspaces()
  # There should always be exactly 1 focused workspace, I think?
  for ws in workspaces:
    if ws['focused']:
      focused_output = ws['output']
      break
  return [ws for ws in workspaces if ws['output'] == focused_output]


def move_window_and_or_view_workspace(action, workspace_name):
  """Sends command to view or move window to (or both) a workspace."""
  if action == 'view':
    command('workspace', workspace_name)
  elif action == 'move':
    command('move', 'container', 'workspace', workspace_name)
  else:
    assert action == 'moveview'
    command('move', 'container', 'workspace', workspace_name)
    command('workspace', workspace_name)
