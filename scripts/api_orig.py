#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'pi':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

tasks = [
    {
        'id': 1,
        'title': u'Lights on',
        'description': u'Turn tree lights on', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Lights off',
        'description': u'Turn tree lights off', 
        'done': False
    },
        {
        'id': 3,
        'title': u'Pulse lights',
        'description': u'Pulse lights from dim to bright', 
        'done': False
    },
    {
        'id': 4,
        'title': u'Train forward',
        'description': u'Move train forward', 
        'done': False
    },
    {
        'id': 5,
        'title': u'Train stop',
        'description': u'Stop train from moving', 
        'done': False
    },
    {
        'id': 6,
        'title': u'Train reverse',
        'description': u'Move train in reverse', 
        'done': False
    }
]

options = [
    {
        'id': 1,
        'title': u'Lights on',
        'description': u'Turn tree lights on'
    },
    {
        'id': 2,
        'title': u'Lights off',
        'description': u'Turn tree lights off'
    },
        {
        'id': 3,
        'title': u'Pulse lights',
        'description': u'Pulse lights from dim to bright'
    },
    {
        'id': 4,
        'title': u'Train forward',
        'description': u'Move train forward'
    },
    {
        'id': 5,
        'title': u'Train stop',
        'description': u'Stop train from moving'
    },
    {
        'id': 6,
        'title': u'Train reverse',
        'description': u'Move train in reverse'
    }
]

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task
    
@app.route('/pwmtree/api/tasks', methods = ['GET'])
@auth.login_required
def get_tasks():
    return jsonify( { 'tasks': map(make_public_task, tasks) } )

@app.route('/pwmtree/api/tasks/<int:task_id>', methods = ['GET'])
@auth.login_required
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify( { 'task': make_public_task(task[0]) } )

@app.route('/pwmtree/api/tasks', methods = ['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify( { 'task': make_public_task(task) } ), 201

@app.route('/pwmtree/api/tasks/<int:task_id>', methods = ['PUT'])
@auth.login_required
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify( { 'task': make_public_task(task[0]) } )
    
@app.route('/pwmtree/api/tasks/<int:task_id>', methods = ['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(host = "", port = 8080, debug = True)
