import requests
import json


class Sender:

    def __init__(self, logger, host, login_pass, urls):
        self.logger = logger
        self.host = host
        self.urls = urls
        self.session = requests.session()
        self.session.auth = tuple(login_pass.split(':'))
        self.question_method = None

    def auth(self):
        url = f'{self.host}{self.urls["auth"]}'
        msg = f'Auth url: {url}'
        self.logger.info(msg)
        if self.question_method and not self.question_method(msg):
            self.logger.warning('Canceled')
            return False
        return self.session.get(url)

    def send_request(self, instance, request):
        method = request.METHOD
        url = f'{self.host}{self.urls["engine"]}{request.get_url(instance)}'
        body = json.dumps(request.get_body())

        result_msg = f'\n' \
                     f'REQUEST:\n' \
                     f'METHOD: {method}\n' \
                     f'URL: {url}\n' \
                     f'BODY: {body}'

        self.logger.info(result_msg)
        if self.question_method and not self.question_method(result_msg):
            self.logger.warning('Canceled')
            return

        response = self.session.request(method, url, json=body)
        self.logger.info(f'Response status code: {response.status_code}')
        if response.status_code != 200:
            self.logger.debug(f'Response:\n{response.json()}')
        return response
