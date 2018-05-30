#!/bin/sh
ps -ef | grep 0.0.0.0:8000 | awk '{ print $2 }' |xargs kill -9
nohup /opt/ActivePython-3.5/bin/python3 manage.py runserver 0.0.0.0:8000 &
