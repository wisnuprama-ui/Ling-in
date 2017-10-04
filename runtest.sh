#!/bin/bash

echo "Run unit test"
source venv/bin/activate
coverage run --include='app_*/*' manage.py test
coverage report -m

