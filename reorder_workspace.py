#!/usr/bin/env python

"""A tool that reorders adjacent workspaces.

Only works for numbered workspaces currently.
"""

from __future__ import print_function, unicode_literals
import argparse
import itertools
import re

import i3ipc as i3


def _swap_name_numbers(ws1, ws2):
  """Returns new workspace names with number prefix switched."""
  new_ws1_name = re.sub('^[0-9]+', str(ws2['num']), ws1['name'])
  new_ws2_name = re.sub('^[0-9]+', str(ws1['num']), ws2['name'])
  return new_ws1_name, new_ws2_name


def _add_number_to_workspace(workspace, all_workspaces):
  """Adds a number prefix to the workspace name."""
  max_num = max(ws['num'] for ws in all_workspaces)
  # Don't think I technically need to specific current name, because it should
  # be focused.
  i3.command('rename', 'workspace', workspace['name'], 'to',
             '{}:{}'.format(max_num + 1, workspace['name']))


def _reorder_workspaces(prev, debug=False):
  """Reorders adjacent workspaces by renaming and swapping their numbers."""
  all_ws = i3.focused_output_workspaces()

  focused = i3.focused_workspace(all_ws)
  if focused['num'] == -1:
    _add_number_to_workspace(focused, all_ws)
    return

  numbered_ws = [ws for ws in all_ws if ws['num'] != -1]
  if debug: print('numbered workspaces:', numbered_ws)
  # Add buffer for wrapping.
  ws = list(itertools.chain([numbered_ws[-1]], numbered_ws, [numbered_ws[0]]))
  if prev:
    ws = list(reversed(ws))
  workspace_pairs = list(itertools.izip(ws, ws[1:]))

  for (ws1, ws2) in workspace_pairs:
    if debug: print('checking <{}>  vs  <{}>'.format(ws1['name'], ws2['name']))
    if ws1['focused']:
      new_ws1_name, new_ws2_name = _swap_name_numbers(ws1, ws2)
      # TODO: sending 2 renames in 1 command causes weird inconsistencies. is
      # that expected?
      i3.command('rename', 'workspace', ws1['name'], 'to', new_ws1_name)
      i3.command('rename', 'workspace', ws2['name'], 'to', new_ws2_name)
      break
  else:
    raise RuntimeError("this shouldn't happen")


def _main():
  parser = argparse.ArgumentParser()
  parser.add_argument('dir', choices=['next', 'prev'])
  parser.add_argument('-debug', action='store_true')
  args = parser.parse_args()

  _reorder_workspaces(args.dir == 'prev', args.debug)


if __name__ == '__main__':
  _main()
