from __future__ import print_function
import json
import subprocess
import sys

def _i3msg(*args):
  """Wrapper around i3-msg. Calls i3-msg w/ all args and parses response."""
  popen = subprocess.Popen(['i3-msg'] + list(args), stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
  stdout, stderr = popen.communicate()
  if stderr:
    print('i3-msg stderr:', stderr, file=sys.stderr)
  return json.loads(stdout)


def command(*cmd):
  """Sends a command via i3-msg."""
  return _i3msg('-t', 'command', *cmd)
