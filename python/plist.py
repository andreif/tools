#!/usr/bin/env python
import json
import os
import re
import subprocess
import sys


def plist_to_json(text):
    s = re.sub(r' = ([^"]+);\n', ' = "\\1",\n', text)
    s = re.sub(r'(\S+) =\s*', '"\\1": ', s)
    s = re.sub(r':\s+\(', ': [', s)
    s = re.sub(r';\n', ',\n', s)
    s = re.sub(r'\)(,?)\n', ']\\1\n', s)
    s = re.sub(r',(\s+[}\]])', '\\1', s)
    return s


def defaults(*args):
    p = subprocess.run(['defaults', *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise NotImplementedError(p.stderr.decode())
    return p.stdout.decode()


def parse(text):
    return json.loads(plist_to_json(text))


def read(path):
    return parse(text=defaults('read', path))


def main(_, path=None):
    if sys.stdin.isatty():
        if path is None:
            print('Error: Pipe or path to plist file required', file=sys.stderr)
            exit(1)
        print(json.dumps(read(path=os.path.abspath(path))))
    else:
        text = sys.stdin.read()
        try:
            data = json.loads(text)
        except Exception:
            print(text)
        else:
            print(data)


if __name__ == '__main__':
    main(*sys.argv)
