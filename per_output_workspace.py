#!/usr/bin/env python

"""Implements per-output replacements for workspace viewing/moving functions.

The idea is that there's a workspace "1" for each output. This makes it somewhat
more difficult to interact with workspaces on other outputs (eg, sending a
window to a hidden workspace on another screen may take 2 steps). However, this
frees you from having to keep track of which workspaces are on which outputs.
"""

from __future__ import print_function, unicode_literals
import argparse

import random_workspace
import i3ipc as i3


def _per_output_workspace_name(number):
  """Returns an output-namespaced workspace name."""
  all_spaces = i3.get_workspaces()
  output_spaces = i3.focused_output_workspaces(all_spaces)
  # If workspace number exists on current output, use the existing name.
  for ws in output_spaces:
    if ws['num'] == number:
      return ws['name']
  # If workspace number isn't used on another output, use the plain number as
  # the name.
  if number not in (w['num'] for w in all_spaces):
    return str(number)
  # Number is used by some other space, so we need a unique name for ours.
  name = random_workspace.new_random_name(frozenset(w['name'] for w in
                                                    all_spaces))
  return '{}:{}'.format(number, name)


def _main():
  parser = argparse.ArgumentParser()
  parser.add_argument('action', choices=['view', 'move', 'moveview'])
  parser.add_argument('number', type=int)
  args = parser.parse_args()
  if args.number < 1:
    raise ValueError('expected positive workspace number, got:', args.number)

  i3.move_window_and_or_view_workspace(args.action,
                                       _per_output_workspace_name(args.number))


if __name__ == '__main__':
  _main()
