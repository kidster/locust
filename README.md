Keystone performance test for revocation events
===============================================

Locust script to test Keystone's performance as revocation events increase.

The KeystoneTaskSet tasks
-------------------------

1. **start** Runs twices as much as Task 'increase_revocation_records'.
   - Authenticates -> Validates(x10) -> revoke token
2. **increase_revocation_records**
   - Gradually increases the number of revocation events in Keystone by authenticating the 'test_user' and revoking its token. (x100)

Setup
-----

Install locust package::

    pip install locustio
    
Run
---

The environment variables ADMIN_USER, ADMIN_PASSWORD, ADMIN_DOMAIN_NAME, ADMIN_DOMAIN_ID will need to be set in order to create the test data in Keystone.

The following example will generate 1000+ revocation events.
Run example:
- export ADMIN_USER=``admin_username``
- export ADMIN_PASSWORD=``admin_password``
- export ADMIN_DOMAIN_NAME=``admin_domain_name``
- export ADMIN_PROJECT_ID=``admin_project_id``

locust -f locustfile.py --host=http://127.0.0.1 --num-request=2500

