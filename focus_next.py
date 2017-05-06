#!/usr/bin/env python

"""Tool for shifting focusing through all windows, regardless of layout.

Handy to use as binding for Alt+Tab.
"""

from __future__ import print_function, unicode_literals
import argparse
import itertools

import i3ipc as i3


def _type_from_enum(i):
  return ['root', 'output', 'con', 'floating_con', 'workspace', 'dockarea'][i]


class _TreeNode(object):
  def __init__(self, i3tree):
    self._id = i3tree['id']
    self._name = i3tree['name']
    self._type = _type_from_enum(i3tree['type'])
    self._layout = i3tree['layout']
    self._window = i3tree['window']
    self._focused = i3tree['focused']
    self._nodes = map(_TreeNode, i3tree['nodes'])

  def __repr__(self):
    return '<TreeNode {} {}>'.format(self._id, self._name)

  def _print(self, indent=0):
    print('{}<{}|{}> {} {}{}{}'.format(
        ' ' * indent * 2,
        self._name,
        self._id,
        self._layout,
        self._type,
        ' WIN' if self._window else '',
        ' FOCUS' if self._focused else ''))
    for n in self._nodes:
      n._print(indent=indent+1)

  def _find_workspace(self, workspace_name):
    if self._type == 'workspace':
      if self._name == workspace_name:
        return self
      return None  # workspaces aren't nested, so return immediately
    for n in self._nodes:
      found = n._find_workspace(workspace_name)
      if found is not None:
        return found
    return None

  def _windows_dfs(self):
    if self._window:
      yield self
    for n in self._nodes:
      for w in n._windows_dfs():
        yield w


def _main():
  parser = argparse.ArgumentParser()
  parser.add_argument('dir', choices=['next', 'prev'])
  parser.add_argument('workspace')
  args = parser.parse_args()

  print('\ntree')
  tree = _TreeNode(i3.get_tree())
  tree._print()

  print('\nworkspace')
  tree._find_workspace(args.workspace)._print()

  print('\nwindows')
  wins = list(tree._find_workspace(args.workspace)._windows_dfs())
  if args.dir == 'prev':
    wins = list(reversed(wins))
  print(wins)
  wins = list(itertools.chain(wins, wins))  # buffered
  win_pairs = itertools.izip(wins, wins[1:])

  for (w1, w2) in win_pairs:
    print('checking', w1._name, w2._name)
    if w1._focused:
      target = w2._id
#      break
  i3.command('[con_id={}]'.format(target), 'focus')

  #### TODO: figure out how to determine the right focus operation...


if __name__ == '__main__':
  _main()
