#!/usr/bin/env python

"""Tool for shifting focusing through all windows, regardless of layout.

Handy to use as binding for Alt+Tab.
"""

from __future__ import print_function, unicode_literals
import argparse
import itertools

import i3ipc as i3


# I think this is only needed for older versions. I'm stuck on 4.7.2 for various
# reasons.
def _type_from_enum(i):
  """Map node type from int to string value."""
  if type(i) != int:
    print('tree node type wasnt an int, no need to convert?', i)
    return i
  return ['root', 'output', 'con', 'floating_con', 'workspace', 'dockarea'][i]


class _TreeNode(object):
  """Mirrors the i3 container tree.

  See http://i3wm.org/docs/ipc.html#_tree_reply
  """

  def __init__(self, i3tree):
    # Internal ID for node.
    self.id_ = i3tree['id']
    # Internal name. Set to _NET_WM_NAME for windows.
    self.name = i3tree['name']
    # Container type. One of 'root', 'output', 'con', 'floating_con',
    # 'workspace', 'dockarea'.
    self.type_ = _type_from_enum(i3tree['type'])
    # One of 'splith', 'splitv', 'stacked', 'tabbed', 'dockarea', 'output'. May
    # change in the future.
    self.layout = i3tree['layout']
    # X11 window ID if node contains a window. Else, None.
    self.window = i3tree['window']
    # True if this node is the window that is currently focused.
    self.focused = i3tree['focused']
    self.nodes = map(_TreeNode, i3tree['nodes'])

  def __repr__(self):
    return '<TreeNode {} {}>'.format(self.id, self._name)

  def _print(self, indent=0):
    """Prints indented representation of tree for debugging."""
    print('{}<{}|{}> {} {}{}{}'.format(
        ' ' * indent * 2, self.name, self.id_, self.layout, self.type_,
        ' WIN' if self.window else '', ' FOCUS' if self.focused else ''))
    for n in self.nodes:
      n._print(indent=indent+1)

  def find_workspace(self, workspace_name):
    """Returns TreeNode representing the workspace name, or None."""
    if self.type_ == 'workspace':
      if self.name == workspace_name:
        return self
      return None  # workspaces aren't nested, so return immediately
    for n in self.nodes:
      found = n.find_workspace(workspace_name)
      if found is not None:
        return found
    return None

  def windows_dfs(self):
    """Yields pre-order DFS traversal of windows rooted at this node."""
    if self.window:
      yield self
    for n in self.nodes:
      for w in n.windows_dfs():
        yield w


def _focus_next(prev):
  """Focuses the next (or previous) window in the current workspace.
  Window ordering is pre-order depth-first traversal of the container tree.
  """
  tree = _TreeNode(i3.get_tree())
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
