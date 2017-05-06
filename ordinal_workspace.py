#!/usr/bin/env python

"""Tool for addressing workspaces by index, not 'number'.

Switches to i'th workspace on the currently focused screen."""

from __future__ import print_function, unicode_literals
import sys

import i3ipc as i3


def _ordinal_workspace(index):
  """Returns workspace name in position i (0-based) of the active output."""
  workspaces = i3.focused_output_workspaces()
  if index > len(workspaces):
    raise ValueError('only have {} workspaces'.format(len(workspaces)))
  return workspaces[index]['name']


def _main():
  if len(sys.argv) != 2:
    raise ValueError('expected single argument: number indicating workspace to switch to')
  index = int(sys.argv[1]) - 1
  if index < 0:
    raise ValueError('one-based index must be positive, got:', sys.argv[1])

  print(i3.command('workspace', _ordinal_workspace(index)))


if __name__ == '__main__':
  _main()
