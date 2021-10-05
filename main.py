import sys
import os
import platform

import jsons as jsons
from flask import Flask, Response, stream_with_context, jsonify
from flask_cors import CORS
from pymwp import __version__
from pymwp.file_io import parse
from pymwp.analysis import Analysis

app = Flask(__name__)
CORS(app)

source_link = 'https://github.com/statycc/pymwp/tree/main/c_files/'
examples_directory = 'c_files'
pre_parser = "cpp"


@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred. ' + str(e), 500


@app.route('/')
def version():
    """Display pymwp version info."""
    result = f'pymwp version: {__version__}\n\n' + \
             f'OS/v: {platform.system()} {platform.release()}\n\n' + \
             f'C pre-parser: {pre_parser}'

    return Response(result, mimetype='text/plain')


@app.route('/examples')
def examples():
    """List all known examples."""
    result = {}
    for dirs in os.listdir(examples_directory):
        display = dirs.capitalize().replace('_', ' ')
        result[display] = {}
        for files in os.listdir(examples_directory + "/" + dirs):
            fname = files.capitalize().replace('_', ' ')[:-2]
            result[display][fname] = f'{dirs}/{files}'
    result['Version'] = {'Display system info': '/'}
    return jsonify(result)


@app.route('/v2/<category>/<filename>')
def analyze_v2(category, filename):
    """Run analysis on specified example."""
    if not os.path.isdir(os.path.join(examples_directory, category)):
        return 'invalid example category!', 500
    if not os.path.isfile(os.path.join(examples_directory, category, filename)):
        return 'example does not exits!', 500

    sample = os.path.join(category, filename)
    file = os.path.join(examples_directory, sample)

    result = {
        'url': f'{source_link}{sample}',
        'program': file_text(file) or "(File is empty)",
    }

    try:
        ast = parse(file, cpp_path=pre_parser)
        result['result'] = Analysis.run(ast, no_save=True)
    except:
        type_, value, tb = sys.exc_info()
        result['error'] = True
        result['error_msg'] = type_.__name__, value

    return Response(jsons.dumps(result), mimetype='application/json')


@app.route('/<path>/<file>')
def analyze(path, file):
    """Run analysis on specified example."""
    if not os.path.isdir(os.path.join(examples_directory, path)):
        return 'invalid example category!', 500
    if not os.path.isfile(os.path.join(examples_directory, path, file)):
        return 'example does not exits!', 500

    return Response(stream_with_context(
        analyze_(path, file)), mimetype='text/plain')


def analyze_(base, filename):
    sample = os.path.join(base, filename)
    file = os.path.join(examples_directory, sample)
    link = f'<a target="_blank" rel="noopener noreferrer"' + \
           f' href="{source_link}{sample}">{sample} ↗</a>'

    yield f'{header(f"Program ({link})")}' + \
          f'{file_text(file) or "(File is empty)"}\n\n'

    try:
        ast = parse(file, cpp_path=pre_parser)
        relation, choices, infinity = Analysis.run(ast, no_save=True)
        choice_values = f'Choices: {choices}' if not infinity else 'infinite'
        yield f'{header("Matrix")}{relation}\n\n' + \
              f'{header("Evaluation")}{choice_values}'
    except:
        type_, value, tb = sys.exc_info()

        yield f'{header("Analysis Ended")}' + \
              f'Analysis terminated with non-0 exit code. This happens ' + \
              f'when file cannot be analyzed (empty or invalid ' + \
              f'input that yields no result) or if an error occurs ' + \
              'during analysis.\n\n' + \
              f'{type_.__name__}: {value}'


def header(value):
    divider = '-' * 30
    return f'{divider}\n{value}\n{divider}\n\n'


def file_text(file_name):
    with open(file_name) as file_object:
        return file_object.read()


if __name__ == '__main__':
    # This is used when running locally only. When deployed, a webserver
    # process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
