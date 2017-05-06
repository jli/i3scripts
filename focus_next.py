#!/usr/bin/env python

"""Tool for shifting focusing through all windows, regardless of layout.

Handy to use as binding for Alt+Tab.
"""

from __future__ import print_function, unicode_literals
import argparse

import i3ipc as i3


def _type_from_enum(i):
  return ['root', 'output', 'con', 'floating_con', 'workspace', 'dockarea'][i]


class _TreeNode(object):
  def __init__(self, i3tree):
    self._name = i3tree['name']
    self._type = _type_from_enum(i3tree['type'])
    self._layout = i3tree['layout']
    self._window = i3tree['window']
    self._focused = i3tree['focused']
    self._nodes = map(_TreeNode, i3tree['nodes'])

  def _print(self, indent=0):
    print('{}<{}> {} {}{}{}'.format(
        ' ' * indent * 2,
        self._name,
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

  #### TODO: figure out how to determine the right focus operation...


if __name__ == '__main__':
  _main()
