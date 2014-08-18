#!/usr/bin/env python
"""
A small Python web app (using Flask) that serves a CSV file for
simple querying (using Pandas and pandas.DataFrame.query()). The
app consists of a to setup a single web page with a query inputn
field, query button and the query results (# rows returned and
the data in a table).

Usage:

./csv_server.py [--debug] <csv_file>
"""
import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os.path import abspath
from traceback import format_exc

from flask import Flask, request

from pandas.computation.ops import UndefinedVariableError
from pandas.io.parsers import read_csv

app = Flask(__name__)


@app.route('/query')
def query():
    try:
        query = request.args['q']
        result = DATA.query(query)
        response = '{}:'.format(len(result.index))
        if len(result.index):
            response += result.to_html()
        return response
    except (RuntimeError, SyntaxError):
        return 'Invalid Syntax', 400
    except UndefinedVariableError:
        bad_variable = format_exc().rsplit("'", 2)[-2]
        return 'Bad field name: {}'.format(bad_variable), 400


@app.route('/')
def index():
    print open(abspath(__file__).rsplit('/', 1)[0] + '/index.html').read()
    return open(abspath(__file__).rsplit('/', 1)[0] + '/index.html').read()


if __name__ == '__main__':

    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('csv_file', help='The csv file that the app will query')

    args = parser.parse_args()

    DATA = read_csv(args.csv_file)

    app.run(debug=args.debug)

