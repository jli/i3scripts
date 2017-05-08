#!/usr/bin/env python

"""A tool that reorders adjacent workspaces.

Only works for numbered workspaces currently.
"""

from __future__ import print_function, unicode_literals
import argparse
import itertools
import random
import re

import i3ipc as i3
import random_workspace


def _swap_numbers(ws1, ws2, all_workspaces):
  """Returns new workspace names with number prefix switched."""
  new_ws1_name = re.sub('^[0-9]+', str(ws2['num']), ws1['name'])
  new_ws2_name = re.sub('^[0-9]+', str(ws1['num']), ws2['name'])
  used_names = frozenset(ws['name'] for ws in all_workspaces)
  def _avoid_used(new_name):
    while new_name in used_names:
      new_name = '{}__{}'.format(new_name,
                                 random.choice(random_workspace.WORDS))
    return new_name
  return _avoid_used(new_ws1_name),  _avoid_used(new_ws2_name)


# TODO: need to avoid trying to rename to an existing name.
def _add_number_to_workspace(workspace, all_workspaces):
  """Adds a number prefix to the workspace name."""
  max_num = i3.max_workspace_number(all_workspaces)
  # If there are no numbered workspaces, start at 1.
  target_num = 1 if max_num is None else 1 + max_num
  i3.command('rename', 'workspace', workspace['name'], 'to',
             '{}:{}'.format(target_num, workspace['name']))


def _reorder_workspaces(prev, debug=False):
  """Reorders adjacent workspaces by renaming and swapping their numbers."""
  all_ws = i3.get_workspaces()
  output_ws = i3.focused_output_workspaces(all_ws)

  focused = i3.focused_workspace(output_ws)
  if focused['num'] == -1:
    _add_number_to_workspace(focused, output_ws)
    return

  numbered_ws = [ws for ws in output_ws if ws['num'] != -1]
  if debug: print('numbered workspaces:', numbered_ws)
  # Add buffer for wrapping.
  ws = list(itertools.chain([numbered_ws[-1]], numbered_ws, [numbered_ws[0]]))
  if prev:
    ws = list(reversed(ws))
  workspace_pairs = list(itertools.izip(ws, ws[1:]))

  for (ws1, ws2) in workspace_pairs:
    if debug: print('checking <{}>  vs  <{}>'.format(ws1['name'], ws2['name']))
    if ws1['focused']:
      new_ws1_name, new_ws2_name = _swap_numbers(ws1, ws2, all_ws)
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
