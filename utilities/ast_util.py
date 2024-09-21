#!/usr/bin/env python3
# noinspection PyUnresolvedReferences
"""
This is a utility script that reads and parses a C file, or a directory of
C files, then generates an AST.
It uses gcc and pycparser, then writes the AST to a file.
This script is mainly useful for generating/updating test cases for unit
testing, and for inspecting AST structure and nodes.
The parser options are hard-coded, and assumes C files have no custom headers,
and that gcc is an existing system C compiler.

<h4>Usage:</h4>

```
python3 utilities/ast_util.py IN_PATH OUT_DIR
```

Arguments:
    IN_PATH (str): A C file or path to a directory of C files.
    OUT_DIR (str): Directory where to save AST.
"""

import os.path
import re
import sys
from pathlib import Path
from os.path import join, abspath, dirname

# run relative to repository root
cwd = abspath(join(dirname(__file__), '../'))
sys.path.insert(0, cwd)

from pymwp.parser import Parser  # noqa: E402

PARSER_ARGS = {'use_cpp': True, 'cpp_path': 'gcc', 'cpp_args': '-E'}
_RE_COMBINE_WHITESPACE = re.compile(r'\s+')
headers = []

in_path, out_dir = sys.argv[1:3]

# identify the files to parse
files = [in_path] if os.path.isfile(in_path) else \
    [os.path.join(in_path, file) for file in os.listdir(in_path)
     if file.endswith(".c")]

for c_file in files:
    out_fn = f'{Path(c_file).stem}.txt'
    ast_str = str(Parser.parse(c_file, headers=headers, **PARSER_ARGS))
    minified = re.sub(_RE_COMBINE_WHITESPACE, ' ', ast_str)

    with open(os.path.join(out_dir, out_fn), "w") as text_file:
        text_file.write(minified)

    print('wrote', len(minified), f'chars to {out_fn}')
