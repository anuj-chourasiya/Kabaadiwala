import os
port = os.environ.get('PORT', 80)
os.system('gunicorn -b 0.0.0.0:' + str(port) +
              ' --chdir kabaadiwala/ kabaadiwala.wsgi --log-file -')