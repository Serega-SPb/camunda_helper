import base64

import requests


class BodyFactory:

    INSTRUCTIONS = 'instructions'
    TYPE = 'type'
    START = 'startBeforeActivity'
    CLOSE = 'cancel'
    ACTIVITY_ID = 'activityId'

    @staticmethod
    def get_move_task_body(util):
        instructions = []
        if util['is_start']:
            instructions.append({BodyFactory.TYPE: BodyFactory.START, BodyFactory.ACTIVITY_ID: util['start']})
        if util['is_close']:
            instructions.append({BodyFactory.TYPE: BodyFactory.CLOSE, BodyFactory.ACTIVITY_ID: util['close']})
        return {BodyFactory.INSTRUCTIONS: instructions}


class Request:

    POST = 0
    PUT = 1

    MOVE_TASK = 0
    SET_VAR = 1
    UPD_VER = 2

    def __init__(self, action, instance, body, *args):
        self.instance = instance
        self.body = body
        self.mode, self.action = self.apply_action(action, *args)

    @classmethod
    def from_config(cls, action, config):
        body = BodyFactory.get_move_task_body(config.utils[action])
        a = getattr(cls, action.upper())
        ins = cls(a, config.instance, body)
        return ins

    def apply_action(self, action, *args):
        if action == self.MOVE_TASK:
            return self.POST, 'modification'
        elif action == self.SET_VAR:
            return self.PUT, f'variables/{args[0]}'
        return None, None

    def get_path(self, host):
        return f'{host}/camunda/api/engine/engine/default/process-instance/{self.instance}/{self.action}'

"""
"{host}/camunda/api/engine/engine/default/process-instance/{instance}/modification"
"{host}/camunda/api/engine/engine/default/process-instance/{instance}/variables/{name_variables}"
"{host}/camunda/api/engine/engine/default/process-instance/migration/{generate/validate/execute}"
"""


class Sender:

    def __init__(self, host, login_pass_64):
        self.host = host
        self.session = requests.session()
        self.session.auth = tuple(base64.b64decode(login_pass_64).decode().split(':'))
        # self.auth_resp = self.session.get(host)

    def auth(self):
        return self.session.get(self.host)

    def send(self, request: Request):
        # if request.req_type == Request.GET:
        #     resp = self.session.get(request.get_path(self.host))
        if request.mode == Request.POST:
            resp = self.session.post(request.get_path(self.host), json=request.body)
        elif request.mode == Request.PUT:
            resp = self.session.put(request.get_path(self.host), json=request.body)
        else:
            resp = 'Incorrect request'
        return resp
