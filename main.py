import sys
import os

from flask import Flask, Response, stream_with_context, jsonify
from flask_cors import CORS
from pymwp import __version__, __title__
from pymwp.analysis import Analysis

app = Flask(__name__)
ex_dir = 'c_files'
CORS(app)


@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred. ' + str(e), 500


@app.route('/')
def version():
    return Response(f'{__title__} {__version__}', mimetype='text/plain')


@app.route('/examples')
def examples():
    result = {}
    for dirs in os.listdir(ex_dir):
        display = dirs.capitalize().replace('_', ' ')
        result[display] = {}
        for files in os.listdir(ex_dir + "/" + dirs):
            fname = files.capitalize().replace('_', ' ')[:-2]
            result[display][fname] = f'{dirs}/{files}'
    result['Version'] = {'Show version': '/'}
    return jsonify(result)


@app.route('/<path>/<file>')
def analyze(path, file):
    return Response(stream_with_context(
        analyze_(path, file)), mimetype='text/plain')


def analyze_(base, filename):
    sample = f'{base}/{filename}'
    file = f'{ex_dir}/{sample}'

    yield f'{header(f"Program ({sample})")}' + \
          f'{file_text(file) or "(File is empty)"}\n\n'

    try:
        relation, choices = Analysis.run(
            file, no_save=True, use_cpp=True,
            cpp_path="cpp", cpp_args="-E")
        if len(choices) > 0:
            choice_values = f'Choices: {choices}'
        else:
            choice_values = "Infinite"
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
