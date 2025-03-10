# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import os
import sys
import inspect
import os.path as osp
from flask_cors import CORS

from flask import Flask, redirect, url_for, request, render_template, send_from_directory
from qa_engine import QAEngine
from chatgpt_engine import ChatGPTEngine

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


app = Flask(__name__)
CORS(app)

# # for profiling
# from werkzeug.middleware.profiler import ProfilerMiddleware
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app)

# Digital data QA engine
qa_engine = None

# ChatGPT Engine (for baseline purpose)
chatgpt_engine = None

@app.route('/test', methods=['GET'])
def test():
    """
    TODO: make calls to the appropriate python function
    TODO: we may want to change these API's to POST apis
    """
    # query = request.args.get('event')
    for key in request.args:
        print(key, request.args[key])
    return {'message': 'okay'}

@app.route('/launch', methods=['GET'])
def launch():
    """Launch a query engine.
    """
    global qa_engine
    global chatgpt_engine
    
    qa_engine = QAEngine('public/digital_data')
    chatgpt_engine = ChatGPTEngine()
    return {'message': 'okay'}


@app.route('/query', methods=['GET'])
def query():
    """Query the posttext engine.
    """
    # return {'message': 'okay'}
    query = request.args.get('query')
    method = request.args.get('qa')
    print(method)

    if method == 'ChatGPT':
        return {"question": query, "method": method, "answer": chatgpt_engine.query(query), "sources": []}

    # embedding-based QA
    if qa_engine != None:
        res = qa_engine.query(query, method=method)
        res["method"] = method
        return res


if __name__ == '__main__':
    app.run(host="::", port=8085, debug=True)
