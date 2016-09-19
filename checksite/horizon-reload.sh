#!/bin/bash

# Target branch: master, stable/newton, ...
BRANCH=stable/newton

cd /opt/stack/horizon
git checkout $BRANCH
git remote update origin
git merge origin/$BRANCH
./run_tests.sh --compilemessages -N
DJANGO_SETTINGS_MODULE=openstack_dashboard.settings python manage.py collectstatic --noinput
DJANGO_SETTINGS_MODULE=openstack_dashboard.settings python manage.py compress --force
sudo service apache2 reload
