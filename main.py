import sys
import os
import platform

import jsons as jsons
from flask import Flask, Response, jsonify
from flask_cors import CORS
from pymwp import __version__
from pymwp.parser import parse_file
from pymwp.analysis import Analysis, Result

app = Flask(__name__)
CORS(app)

source_link = 'https://github.com/statycc/pymwp/tree/main/c_files/'
examples_directory = 'c_files'
pre_parser = "cpp"


@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred. ' + str(e), 500


@app.route('/<category>/<filename>')
@app.route('/v2/<category>/<filename>')
def analyze_v2(category, filename):
    """Run analysis on specified example."""
    if not os.path.isdir(os.path.join(examples_directory, category)):
        return 'invalid example category!', 500
    if not os.path.isfile(
            os.path.join(examples_directory, category, filename)):
        return 'example does not exits!', 500

    sample = os.path.join(category, filename)
    file = os.path.join(examples_directory, sample)
    result = {
        'url': f'{source_link}{sample}',
        'name': sample
    }

    try:
        result['program'] = file_text(file) or ""
        ast = parse_file(file, use_cpp=True, cpp_path=pre_parser,
                         cpp_args='-E')
        analysis_result = Result()
        analysis_result.program.program_path = sample
        analysis_result.program.n_lines = \
            len(result['program'].split("\n"))
        res = Analysis.run(
            ast, no_save=True, res=analysis_result, fin=True)
        result['fail'] = dict([
            (r, vals.relation.infty_vars())
            for r, vals in res.relations.items() if vals.infinite])
        result['bounds'] = dict([
            (r, vals.bound.show())
            for r, vals in res.relations.items() if not vals.infinite])
        result['result'] = res
    except:
        type_, value, tb = sys.exc_info()
        result['error'] = True
        result['error_msg'] = f'{type_.__name__}: {value}'

    return Response(jsons.dumps(result), mimetype='application/json')


@app.route('/')
@app.route('/v2/')
def version():
    """Display pymwp version info."""
    result = {
        'result': f'pymwp version: {__version__}\n\n' + \
                  f'OS/v: {platform.system()} {platform.release()}\n\n' + \
                  f'C pre-parser: {pre_parser}'
    }
    return jsonify(result)


@app.route('/examples')
@app.route('/v2/examples')
def examples():
    """List all known examples."""
    result = {}
    for dirs in os.listdir(examples_directory):
        display = dirs.capitalize().replace('_', ' ')
        result[display] = {}
        for files in os.listdir(examples_directory + "/" + dirs):
            fname = files.capitalize().replace('_', ' ')[:-2]
            result[display][fname] = f'{dirs}/{files}'
    result['Version'] = {'Version info': '/'}
    return jsonify(result)


def file_text(file_name):
    with open(file_name) as file_object:
        return file_object.read()


if __name__ == '__main__':
    # This is used when running locally only. When deployed, a webserver
    # process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
