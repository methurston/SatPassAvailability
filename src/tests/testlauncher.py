#!/usr/bin/env python
import subprocess
from time import sleep

"""launches the api and serves HTML directly from the code base for quick testing."""

with open('httpoutput.txt', 'w') as output:
    print('Starting HTTP server')
    http_cmd = ['python',
                '-m', 'http.server',
                '8181']
    http_working_dir = '../../html'
    http_process = subprocess.Popen(http_cmd, cwd=http_working_dir, stdout=output)
    print('Starting API server')
    gunoutput = 'tests/gunicornout.txt'
    host = '127.0.0.1'
    port = 8000
    api_cmd = ['gunicorn',
               '-b', '{}:{}'.format(host, port),
               '--error-logfile', gunoutput,
               '--capture-output',
               'app']
    api_working_dir = '../'
    api_process = subprocess.Popen(api_cmd, cwd=api_working_dir, stdout=output)
    sleep(3)
    try:
        while True:
            sleep(5)
    except KeyboardInterrupt:
        print('Exiting')
        http_process.kill()
        http_process.wait()
        print('Shutting down API server')
        api_process.kill()
        api_process.wait()
