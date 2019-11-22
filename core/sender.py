import requests
import yaml


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

    URLS_FILE = 'urls.yaml'

    def __init__(self, action, instance, body, *args):
        self.urls = {}
        self.load_urls()
        self.path = '/camunda/api/engine/engine/default/process-instance/'
        self.instance = instance
        self.body = body
        self.mode, self.action = self.apply_action(action, *args)

    def load_urls(self):
        with open(self.URLS_FILE, 'r') as file:
            data = file.read()
        self.urls = yaml.load(data, yaml.FullLoader)

    @classmethod
    def from_config(cls, action, config):
        body = BodyFactory.get_move_task_body(config.utils[action])
        a = getattr(cls, action.upper())
        ins = cls(a, config.instance, body)
        return ins

    def apply_action(self, action, *args):
        if action == self.MOVE_TASK:
            self.path = self.urls['move_task']
            return self.POST, 'modification'
        elif action == self.SET_VAR:
            return self.PUT, f'variables/{args[0]}'
        return None, None

    def get_path(self, host):
        return f'{host}{self.path}{self.instance}/{self.action}'
        # return f'{host}/camunda/api/engine/engine/default/process-instance/{self.instance}/{self.action}'

"""
"{host}/camunda/api/engine/engine/default/process-instance/{instance}/modification"
"{host}/camunda/api/engine/engine/default/process-instance/{instance}/variables/{name_variables}"
"{host}/camunda/api/engine/engine/default/process-instance/migration/{generate/validate/execute}"
"""


class Sender:

    def __init__(self, host, login_pass, logger):
        self.logger = logger
        self.host = host
        self.session = requests.session()
        self.session.auth = tuple(login_pass.split(':'))

    def auth(self, auth):
        url = f'{self.host}{auth}'
        self.logger.info(f'Auth url: {url}')
        return self.session.get(url)

    def send(self, request: Request):
        url = request.get_path(self.host)

        self.logger.info(f'Request url: {url}')
        self.logger.info(f'Request body: {request.body}')

        # if request.req_type == Request.GET:
        #     resp = self.session.get(request.get_path(self.host))
        if request.mode == Request.POST:
            resp = self.session.post(url, json=request.body)
        elif request.mode == Request.PUT:
            resp = self.session.put(url, json=request.body)
        else:
            resp = 'Incorrect request'
        return resp
