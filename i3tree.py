"""Container tree manipulation helpers."""


# I think this is only needed for older versions. I'm stuck on 4.7.2 for various
# reasons.
def _type_from_enum(i):
  """Map node type from int to string value."""
  if type(i) != int:
    # print('tree node type wasnt an int, no need to convert?', i)
    return i
  return ['root', 'output', 'con', 'floating_con', 'workspace', 'dockarea'][i]


class TreeNode(object):
  """Wrapper around i3 container tree with helper methods.

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
    self.nodes = map(TreeNode, i3tree['nodes'])

  def __repr__(self):
    return '<TreeNode {} {}>'.format(self.id_, self.name)

  def print_(self, indent=0):
    """Prints indented representation of tree for debugging."""
    print('{}<{}|{}> {} {}{}{}'.format(
        ' ' * indent * 2, self.name, self.id_, self.layout, self.type_,
        ' WIN' if self.window else '', ' FOCUS' if self.focused else ''))
    for n in self.nodes:
      n.print_(indent=indent+1)

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
