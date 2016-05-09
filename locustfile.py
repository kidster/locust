import copy
import json
import os
import uuid

from locust import HttpLocust, TaskSet, task

HEADERS = {'content-type': 'application/json'}
PROJECT_PATH = '/v3/projects'
TOKEN_PATH = '/v3/auth/tokens'
USER_PATH = '/v3/users'

class KeystoneTaskSet(TaskSet):
    """ Performance Task

    The KeystoneTaskSet include two different tasks.
    Task 'start': Runs twices as much as Task 'increase_revocation_records'.
        Authenticates -> Validates(x10) -> revoke token
    Task 'increase_revocation_records':
        Gradually increate the number of revocation events in Keystone by
        authenticating the 'test_user' and revoking the token. (x100)
    """

    def on_start(self):
        """ Setup admin and test user. """
        admin_user = os.environ['ADMIN_USER']
        admin_password = os.environ['ADMIN_PASSWORD']
        admin_domain_name = os.environ['ADMIN_DOMAIN_NAME']
        admin_project_id = os.environ['ADMIN_PROJECT_ID']
        HEADERS['X-Auth-Token'] = self._get_token(admin_user,
                                                  admin_password,
                                                  admin_domain_name,
                                                  project_id=admin_project_id)
        # Create test user
        self.username = 'test_user'
        self.password = 'Password1'
        self.user_domain_id = 'default'
        self.user_domain_name = 'Default'
        self.project_id = self._create_project()['project']['id']
        self._create_user(self.username, self.password, self.user_domain_id,
                          self.project_id)

    def _get_token(self, username, password, user_domain, project_id=None):
        """ Authenticate user and return token. """
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
            msg = "Failed to authenticate %s user. Status %s" % (username,
                response.status_code)
            raise SystemExit(msg)

    def _create_user(self, username, password, domain_id, project_id):
        """ Create user request in Keystone. """
        request = {
            "user": {
                "name": username,
                "password": password,
                "domain_id": domain_id,
                "default_project_id": project_id,
                "description": "description",
                "email": "test@example.com",
                "enabled": True,
            }
        }
        response = self.client.post(USER_PATH, data=json.dumps(request),
                                    headers=HEADERS)
        if response.status_code == 409:
            return
        elif response.status_code == 201:
            return response.json()
        else:
            raise SystemExit("Failed to create test user.")

    def _create_project(self):
        """ Create project in Keystone. """
        request = {
            "project": {
                "description": "description",
                "enabled": True,
                "name":  uuid.uuid4().hex,
                "domain_id": "default",
            }
        }
        response = self.client.post(PROJECT_PATH, data=json.dumps(request),
                                    headers=HEADERS)

        if response.status_code == 201:
            return response.json()
        else:
            raise SystemExit("Failed to create project.")

    @task(2)
    def start(self):
        headers = copy.deepcopy(HEADERS)
        headers['X-Subject-Token'] = self._get_token(self.username,
                                                     self.password,
                                                     self.user_domain_name)
        for i in range(10):
            self.client.get(TOKEN_PATH, headers=headers)
        self.client.delete(TOKEN_PATH, headers=headers)

    @task(1)
    def increase_revocation_records(self):
        headers = copy.deepcopy(HEADERS)

        for i in range(100):
            headers['X-Subject-Token'] = self._get_token(self.username,
                                                         self.password,
                                                         self.user_domain_name)
            self.client.delete(TOKEN_PATH, headers=headers)


class KeystoneRevocationTest(HttpLocust):
    task_set = KeystoneTaskSet
    min_wait=1000
    max_wait=1000
