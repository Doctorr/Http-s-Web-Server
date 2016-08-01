#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

app = Flask(__name__)

logs = [
    {
        'id': 1,
        'title': u'Header',
        'body': u'Rsyslog Test Data'
    }
]


@app.route('/rsyslog/syslog.log', methods=['GET'])
def get_logs():
    return jsonify({'logs': logs})


@app.route('/rsyslog/syslog.log/<int:log_id>', methods=['GET'])
def get_log(log_id):
    log = [log for log in logs if log['id'] == log_id]
    if len(log) == 0:
        abort(404)
    return jsonify({'log': log[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/rsyslog/syslog.log', methods=['POST'])
def create_log():
    if not request.json or not 'title' in request.json:
        abort(400)
    log = {
        'id': logs[-1]['id'] + 1,
        'title': request.json.get('title', ""),
        'body': request.json.get('body', ""),
    }
    logs.append(log)
    return jsonify({'log': log}), 201


@app.route('/rsyslog/syslog.log/<int:log_id>', methods=['PUT'])
def update_log(log_id):
    log = [log for log in logs if log['id'] == log_id]
    if len(log) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'body' in request.json and type(request.json['body']) is not unicode:
        abort(400)
    log[0]['title'] = request.json.get('title', log[0]['title'])
    log[0]['body'] = request.json.get('body', log[0]['body'])
    return jsonify({'log': log[0]})


@app.route('/rsyslog/syslog.log/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    log = [log for log in logs if log['id'] == log_id]
    if len(log) == 0:
        abort(404)
    logs.remove(log[0])
    return jsonify({'result': True})


# def make_public_log(log):
#     new_log = {}
#     for field in log:
#         if field == 'id':
#             new_log['uri'] = url_for('get_log', log_id=log['id'], _external=True)
#         else:
#             new_log[field] = log[field]
#     return new_log

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')