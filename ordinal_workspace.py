#!/usr/bin/env python

"""Tool for addressing workspaces by index, not 'number'.

Targets the i'th workspace on the currently focused screen. Can either view
workspace, move focused container to workspace, or both.

"""

from __future__ import print_function, unicode_literals
import argparse
import sys

import i3ipc as i3


def _ordinal_workspace(index):
  """Returns workspace name in position i (0-based) of the active output."""
  workspaces = i3.focused_output_workspaces()
  if index > len(workspaces):
    raise ValueError('only have {} workspaces'.format(len(workspaces)))
  return workspaces[index]['name']


def _main():
  parser = argparse.ArgumentParser()
  parser.add_argument('action', choices=['view', 'move', 'moveview'])
  parser.add_argument('number', type=int)
  args = parser.parse_args()
  if args.number < 1:
    raise ValueError('one-based index must be positive, got:', args.number)

  target = _ordinal_workspace(args.number - 1)
  i3.move_window_and_or_view_workspace(args.action, target)


if __name__ == '__main__':
  _main()
