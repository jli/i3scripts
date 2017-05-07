#!/usr/bin/env python

"""A tool that prints the container tree of the currently active workspace."""

from __future__ import print_function, unicode_literals
import argparse

import i3ipc as i3


def _main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-full', action='store_true',
                      help='print full tree, not just current workspace')
  args = parser.parse_args()
  tree = i3.get_tree() if args.full else i3.get_workspace_tree()
  tree.print_()


if __name__ == '__main__':
  _main()
