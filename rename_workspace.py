#!/usr/bin/env python

"""Rename current workspace while preserving existing number.

I like to rename workspaces a lot. It's annoying to have to type the number
prefix, though. This tool wraps the call to rename:
- If the new name has a number prefix, it's passed through.
- Otherwise, the existing workspace number is used so the workspace retains its
  number and position.
- If the workspace isn't already numbered, it stays unnumbered.
"""

from __future__ import print_function, unicode_literals
import argparse
import re

import i3ipc as i3


def _has_number_prefix(text):
  return bool(re.search('^[0-9]', text))


def _rename_workspace(new_name):
  new_name = new_name.strip()
  if not _has_number_prefix(new_name):
    current_num = i3.focused_workspace()['num']
    if current_num != -1:
      new_name = '{}:{}'.format(current_num, new_name)
  i3.command('rename', 'workspace', 'to', new_name)


def _main():
  parser = argparse.ArgumentParser()
  parser.add_argument('new_name', help='new name for current workspace')
  args = parser.parse_args()
  _rename_workspace(args.new_name)

if __name__ == '__main__':
  _main()
