#!/usr/bin/env python

import random
import subprocess

# Random list of short words.
# grep '^[a-z]\+$' /usr/share/dict/american-english \
# | grep -v '....' | grep -v '^..$' | grep -v '^.$' | shuf -n50 | sort
WORDS = [
    'age', 'ale', 'ash', 'ate', 'bay', 'coo', 'cry', 'dad', 'den', 'die', 'dis',
    'ebb', 'fly', 'foe', 'fop', 'gut', 'had', 'hep', 'hie', 'his', 'jet', 'lax',
    'lox', 'maw', 'mes', 'mew', 'mid', 'mom', 'mug', 'net', 'nod', 'oil', 'pas',
    'pop', 'raw', 'rod', 'rot', 'sax', 'sew', 'spy', 'sty', 'tag', 'tee', 'ten',
    'tom', 'vie', 'wow', 'yes'
]

def send_command(i3_cmd):
  popen = subprocess.Popen(['i3-msg', '-t', 'command'] + i3_cmd, stdout=subprocess.PIPE)
  sout, _ = popen.communicate()
  return sout

# TODO: filter out if it exists already
def random_name():
  return '-'.join([random.choice(WORDS), random.choice(WORDS)])

def main():
  print send_command(['workspace', random_name()])

if __name__ == '__main__':
  main()
