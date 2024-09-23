import os
import platform
import sys
import re
from os.path import isdir, isfile, join

import jsons as jsons
from flask import Flask, Response, jsonify
from flask_cors import CORS
from pymwp import __version__, Analysis, Result
from pymwp.parser import parse_file  # pycparser
from pymwp.file_io import loc

app = Flask(__name__)
CORS(app)

source_link = 'https://github.com/statycc/pymwp/tree/main/c_files/'
examples_directory = 'c_files'
pre_parser = "cpp"


def file_text(file_name):
    with open(file_name) as file_object:
        return file_object.read()


def ex_name(file_name: str) -> str:
    """Format example display name.
    e.g., inline_variable => Inline Variable"""
    file_name = re.sub(r'(\d+)_(\d+)', r'\1.\2', file_name)
    file_name = (file_name.replace('not', 'not_')
                 .replace('example', 'example_'))
    words = map(lambda w: w.capitalize(), file_name.split("_"))
    return ' '.join(words)


@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred. ' + str(e), 500


@app.route('/<category>/<filename>')
@app.route('/v2/<category>/<filename>')
def analyze_v2(category, filename):
    """Run analysis on specified example."""

    if not isdir(join(examples_directory, category)):
        return 'invalid example category!', 500
    if not isfile(join(examples_directory, category, filename)):
        return 'example does not exits!', 500

    sample = join(category, filename)
    file = join(examples_directory, sample)
    ex = dict(url=f'{source_link}{sample}', name=sample)

    # noinspection PyBroadException
    try:
        program = file_text(file) or ""
        ast = parse_file(file, True, pre_parser, '-E')
        analysis_result = Result()
        analysis_result.program.program_path = sample
        analysis_result.program.n_lines = loc(file)
        result = Analysis.run(
            ast, no_save=True, res=analysis_result, fin=True)
        fail = [(k, v.relation.infty_vars()) for k, v
                in result.relations.items() if v.infinite]
        bounds = [(k, v.bound.show()) for k, v
                  in result.relations.items() if not v.infinite]
        msg = dict(program=program, result=result,
                   fail=fail, bounds=bounds)
    except Exception:
        type_, value, _ = sys.exc_info()
        msg = dict(error=True, error_msg=f'{type_.__name__}: {value}')

    response = jsons.dumps({**ex, **msg})
    return Response(response, mimetype='application/json')


@app.route('/')
@app.route('/v2/')
def version():
    """Display pymwp version info."""
    pf = platform.uname()
    info = [('OS', f'{pf.system} {pf.machine}'),
            ('OS version', pf.version),
            ('OS release', pf.release),
            ('Processor', pf.processor),
            ('C pre-parser', pre_parser),
            ('Python', f'{platform.python_version()}'),
            ('pymwp version', __version__)]
    return jsonify(dict(result="\n".join(
        [f'{k}: {v}' for k, v in info])))


@app.route('/examples')
@app.route('/v2/examples')
def examples():
    """List all known examples."""
    result = dict([
        (ex_name(category), dict([(
            ex_name(f_name[:-2]), f'{category}/{f_name}')
            for f_name in
            os.listdir(examples_directory + "/" + category)]))
        for category in os.listdir(examples_directory)],
        Version={'Version info': '/'})
    return jsonify(result)


if __name__ == '__main__':
    # This is used when running locally only. When deployed, a webserver
    # process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
