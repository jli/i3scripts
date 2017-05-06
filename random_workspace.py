#!/usr/bin/env python

"""Switch to a randomly named new workspace."""

from __future__ import print_function, unicode_literals
import random
import sys

import i3ipc as i3

# Random list of short words.
# grep '^[a-z]\+$' /usr/share/dict/american-english \
# | grep -v '....' | grep -v '^..$' | grep -v '^.$' | shuf -n50 | sort
WORDS = ['age', 'ale', 'ash', 'ate', 'bay', 'coo', 'cry', 'dad', 'den', 'die',
         'dis', 'ebb', 'fly', 'foe', 'fop', 'gut', 'had', 'hep', 'hie', 'his',
         'jet', 'lax', 'lox', 'maw', 'mes', 'mew', 'mid', 'mom', 'mug', 'net',
         'nod', 'oil', 'pas', 'pop', 'raw', 'rod', 'rot', 'sax', 'sew', 'spy',
         'sty', 'tag', 'tee', 'ten', 'tom', 'vie', 'wow', 'yes']


def _random_name():
  return '-'.join([random.choice(WORDS), random.choice(WORDS)])


def _main():
  existing = frozenset(ws['name'] for ws in i3.get_workspaces())
  for _ in xrange(0, 1000):
    candidate = _random_name()
    if candidate not in existing:
      print(i3.command('workspace', candidate))
      return
  print('failed to generate new, nonexistent random name?!', file=sys.stderr)


if __name__ == '__main__':
  _main()
