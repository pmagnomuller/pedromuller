release: python3 manage.py migrate
web: gunicorn --worker-class gevent --timeout 200 pedromuller.wsgi --log-file -