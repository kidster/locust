Keystone performance test for revocation events
===============================================

Performance test script for Keystone using locust to test revocation events

The KeystoneTaskSet include two different tasks.
    Task 'start': Runs twices as much as Task 'increase_revocation_records'.
        Authenticates -> Validates(x10) -> revoke token
    Task 'increase_revocation_records':
        Gradually increate the number of revocation events in Keystone by authenticating the 'test_user' and revoking its token. (x100)

Setup:
~~~~~~

pip install locustio

The environment variables ADMIN_USER, ADMIN_PASSWORD, ADMIN_DOMAIN_NAME, ADMIN_DOMAIN_ID will need to be set in order to create the test data in Keystone.

The following example will generate 1000+ revocation events.
Run example:
export ADMIN_USER=admin
export ADMIN_PASSWORD=admin
export ADMIN_DOMAIN_NAME=Default
export ADMIN_PROJECT_ID=a9538f8a717f4215a90c9f41220499cb

locust -f locustfile.py --host=http://127.0.0.1 --num-request=2500

