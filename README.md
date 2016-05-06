# locust
Performance test script for Keystone using locust to test revocation events

Setup:
pip install locustio

Run:
locust -f locustfile.py --host=<host_address> --num-request=2500
