import copy
import json
import uuid

from locust import HttpLocust, TaskSet, task

TOKEN_PATH = '/v3/auth/tokens'
DOMAIN_PATH = '/v3/domains'
HEADERS = {'content-type': 'application/json'}

class KeystoneTaskSet(TaskSet):

    def on_start(self):
        HEADERS['X-Auth-Token'] = self._get_token(
            'admin', 'admin', 'Default',
            'e07767c6cb844c939b78add51c76f9b5')

    def _get_token(self, username, password, user_domain, project_id=None):
        request = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "domain": {
                                "name": user_domain
                            },
                            "name": username,
                            "password": password
                        }
                    }
                }
            }
        }

        if project_id:
            request['auth']['scope'] = {
                "project": {
                    "id": project_id
                }
            }
        response = self.client.post(TOKEN_PATH, data=json.dumps(request),
                                    headers=HEADERS)
        if response.status_code == 201:
            return response.headers['X-Subject-Token']
        else:
            raise SystemExit(response.status_code)

    def _create_domain(self):
        request = {
            "domain": {
                "description": "description",
                "enabled": False,
                "name":  uuid.uuid4().hex,
            }
        }
        response = self.client.post(DOMAIN_PATH, data=json.dumps(request),
                                    headers=HEADERS)
        return response

    @task(2)
    def start(self):
        headers = copy.deepcopy(HEADERS)
        headers['X-Subject-Token'] = self._get_token('test_user', 'Password1',
                                                     'test_domain')
        for i in range(10):
            self.client.get(TOKEN_PATH, headers=headers)
        self.client.delete(TOKEN_PATH, headers=headers)

    @task(1)
    def increase_revocation_records(self):
        headers = copy.deepcopy(HEADERS)

        for i in range(100):
            headers['X-Subject-Token'] = self._get_token('test_user',
                                                         'Password1',
                                                         'test_domain')
            self.client.delete(TOKEN_PATH, headers=headers)


class KeystoneRevocationTest(HttpLocust):
    task_set = KeystoneTaskSet
    host = 'http://10.190.237.41:8000'
    min_wait=1000
    max_wait=1000
