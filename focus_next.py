#!/usr/bin/env python

"""Tool for shifting focusing through all windows, regardless of layout.

Handy to use as binding for Alt+Tab.
"""

from __future__ import print_function, unicode_literals
import argparse
import itertools

import i3ipc as i3


def _focus_next(prev):
  """Focuses the next (or previous) window in the current workspace.
  Window ordering is pre-order depth-first traversal of the container tree.
  """
  tree = i3.get_tree()
  current_workspace_tree = tree.find_workspace(i3.focused_workspace()['name'])
  wins = list(current_workspace_tree.windows_dfs())
  if prev:
    wins = list(reversed(wins))
  # Add boundary windows to either end so that focus wraps around.
  wins = list(itertools.chain([wins[-1]], wins, [wins[0]]))

  for (w1, w2) in itertools.izip(wins, wins[1:]):
    if w1.focused:
      i3.command('[con_id={}]'.format(w2.id_), 'focus')
      return


def _main():
  parser = argparse.ArgumentParser()
  parser.add_argument('dir', choices=['next', 'prev'])
  args = parser.parse_args()

  _focus_next(args.dir == 'prev')


if __name__ == '__main__':
  _main()
