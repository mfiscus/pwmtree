#!/usr/bin/python

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from Adafruit_PWM_Servo_Driver import PWM
from lirc import Lirc
from subprocess import call
import time


pwm = PWM(0x40) # Initialise the PWM device using the default address
pwm.setPWMFreq(600) # Set frequency in Hz

Off = 0  # Min pulse length out of 4096
Low = 1024
Lowest = 102  # Lowest visible pulse length out of 4096
Max = 4095  # Max pulse length out of 4096

train = Lirc('/home/pi/Projects/pwmtree/train.conf')

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()


def DimLights():
    pwm.setPWM(0, Off, Low)
    pwm.setPWM(1, Off, Low)

    return True


def VeryDimLights():
    pwm.setPWM(0, Off, Lowest)
    pwm.setPWM(1, Off, Lowest)

    return True


def Dimmer():
    pwm.setPWM(0, Off, Low)
    pwm.setPWM(1, Off, Low)

    return True


def BlinkLights():
    counter = 0
    blinks = 4
    while (counter < blinks):
        pwm.setPWM(0, Off, Lowest)
        pwm.setPWM(1, Off, Lowest)
        time.sleep(.2)
        pwm.setPWM(0, Off, Max)
        pwm.setPWM(1, Off, Max)
        time.sleep(.2)
        counter += 1

    return True


def PingPong():
    counter = 0
    blinks = 6
    pwm.setPWM(0, Off, Max)
    pwm.setPWM(1, Off, Max)
    time.sleep(.2)
    while (counter < blinks):
        pwm.setPWM(0, Off, Lowest)
        pwm.setPWM(1, Off, Max)
        time.sleep(.2)
        pwm.setPWM(0, Off, Max)
        pwm.setPWM(1, Off, Lowest)
        time.sleep(.2)
        counter += 1

    pwm.setPWM(1, Off, Max)

    return True


def LightsOn():
    pwm.setPWM(0, Off, Max)
    pwm.setPWM(1, Off, Max)

    return True


def LightsOff():
    pwm.setPWM(0, Off, Off)
    pwm.setPWM(1, Off, Off)

    return True


def TrainFast():
    device_id = ' '.join(train.devices())
    message = 'TrainFast'
    call(['irsend', 'SEND_ONCE', device_id, message, message])

    return True


def TrainStop():
    device_id = ' '.join(train.devices())
    message = 'TrainStop'
    call(['irsend', 'SEND_ONCE', device_id, message, message, message, message])

    return True


def TrainSlow():
    device_id = ' '.join(train.devices())
    message = 'TrainSlow'
    call(['irsend', 'SEND_ONCE', device_id, message, message])

    return True


def TrainReverse():
    device_id = ' '.join(train.devices())
    message = 'TrainReverse'
    call(['irsend', 'SEND_ONCE', device_id, message, message])

    return True


@auth.get_password
def get_password(username):
    if username == 'pi':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

tasks = [
    {
        'id': 1,
        'title': u'LightsOn',
        'description': u'Turn tree lights on', 
        'done': False
    },
    {
        'id': 2,
        'title': u'DimLights',
        'description': u'Make tree lights dim', 
        'done': False
    },
    {
        'id': 3,
        'title': u'VeryDimLights',
        'description': u'Make tree lights very dim', 
        'done': False
    },
    {
        'id': 4,
        'title': u'LightsOff',
        'description': u'Turn tree lights off', 
        'done': False
    },
    {
        'id': 5,
        'title': u'BlinkLights',
        'description': u'Pulse lights from dim to bright', 
        'done': False
    },
    {
        'id': 6,
        'title': u'PingPong',
        'description': u'Pulse lights from dim to bright on alternating channels', 
        'done': False
    },
    {
        'id': 7,
        'title': u'TrainSlow',
        'description': u'Move train forward slow', 
        'done': False
    },
        {
        'id': 8,
        'title': u'TrainFast',
        'description': u'Move train forward fast', 
        'done': False
    },
    {
        'id': 9,
        'title': u'TrainStop',
        'description': u'Stop train from moving', 
        'done': False
    },
    {
        'id': 10,
        'title': u'TrainReverse',
        'description': u'Move train in reverse', 
        'done': False
    }
]

task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}


class TaskListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return {'tasks': [marshal(task, task_fields) for task in tasks]}

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'id': tasks[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        tasks.append(task)
        method_name = args['title']
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(method_name)
        if not method:
            raise Exception("Method %s not implemented" % method_name)
        #result = method.apply_async()
        #result.wait()
        result = method()
        return {'task': marshal(task, task_fields)}, 201


class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'task': marshal(task[0], task_fields)}

    def put(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'task': marshal(task, task_fields)}

    def delete(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return {'result': True}


api.add_resource(TaskListAPI, '/pwmtree/api/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/pwmtree/api/tasks/<int:id>', endpoint='task')


if __name__ == '__main__':
    app.run(host = "", port = 8080, debug = True)
