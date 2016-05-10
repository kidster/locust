Keystone performance test for revocation events
===============================================

Simple locust script to test Keystone's performance as revocation events increase. This script is meant to be run with a clean instance of keystone.

On start
--------

The on_start method in locust creates user 'test_user' in order to authenticate, validate, and revoke his tokens.

The KeystoneTaskSet tasks
-------------------------

1. **start** Runs twices as much as Task 'increase_revocation_records'.
   - Authenticates  -> Validates(x10) -> revoke token
2. **increase_revocation_records**
   - Gradually increases the number of revocation events in Keystone by authenticating the 'test_user' and revoking its token. (x100)

Setup
-----

Install locust package::

    pip install locustio
    
Run
---

The environment variables ADMIN_USER, ADMIN_PASSWORD, ADMIN_DOMAIN_NAME, and ADMIN_DOMAIN_ID will need to be set in order to create the test data in Keystone.

The following example will generate 1000+ revocation events.
Run example:
- export ADMIN_USER=``admin_username``
- export ADMIN_PASSWORD=``admin_password``
- export ADMIN_DOMAIN_NAME=``admin_domain_name``
- export ADMIN_PROJECT_ID=``admin_project_id``

``locust -f locustfile.py -c 1 -r 1 --host=http://localhost:8000 --no-web --num-request=2500``

Keystone configuration
----------------------

Set global cache to true and enabled all region caching.

[cache]

backend = oslo_cache.memcache_pool

enabled = true

memcache_servers = 127.0.0.1:11211

[token]

provider = fernet


Results
-------
* Master (7a18200ff6fb80a2408dbbe3172fe73dfb13366c) vs  Rebased Patch 285134 - PDF: [`https://www.docdroid.net/yNvics9/keystonerevocationeventsperfresults.pdf.html`](https://www.docdroid.net/yNvics9/keystonerevocationeventsperfresults.pdf.html)
* * Master (b155387cdd470a038387495cdcd082728cd645f9) vs Rebased Patch 285134 - PDF: [`https://www.docdroid.net/zj6Gam2/keystonerevocationeventsperfresults-2.numbers.html`](https://www.docdroid.net/zj6Gam2/keystonerevocationeventsperfresults-2.numbers.html)
