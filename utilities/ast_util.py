import os.path
import re
import sys
from pathlib import Path

# import from sibling
sys.path.append("..")
from pymwp.parser import Parser

"""
This is a utility script reads and parses a C file, then generates an AST.
 
It uses gcc and pycparser, then writes the AST to a file. This script is 
mainly useful for generating/updating test cases for unit testing, or
inspecting AST structure and nodes. 

# Arguments (positional):

1. input path -- give a C file, or path to a directory of C files 
2. output directory -- where to save AST 

Note the parser options are hard-coded, and assumes C file has no custom
headers, and that gcc is a valid C compiler. 
"""

PARSER_ARGS = {'use_cpp': True, 'cpp_path': 'gcc', 'cpp_args': '-E'}
_RE_COMBINE_WHITESPACE = re.compile(r'\s+')

in_path, out_dir = sys.argv[1:3]

# identify the files to parse
files = [in_path] if os.path.isfile(in_path) else \
    [os.path.join(in_path, file) for file in os.listdir(in_path)
     if file.endswith(".c")]

for c_file in files:
    out_fn = f'{Path(c_file).stem}.txt'
    ast_str = str(Parser.parse(c_file, **PARSER_ARGS))
    minified = re.sub(_RE_COMBINE_WHITESPACE, ' ', ast_str)

    with open(os.path.join(out_dir, out_fn), "w") as text_file:
        text_file.write(minified)

    print('wrote', len(minified), f'chars to {out_fn}')

