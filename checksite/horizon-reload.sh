#!/bin/bash

# Target branch: master, stable/pike, ...
BRANCH=stable/pike

cd /opt/stack/horizon

# Remove stale compiled python files
find horizon -name '*.pyc' | xargs rm
find openstack_dashboard -name '*.pyc' | xargs rm

# Fetch the latest code from git
git checkout $BRANCH
git remote update origin
git merge origin/$BRANCH

python manage.py compilemessages
python manage.py collectstatic --noinput
python manage.py compress --force
sudo service apache2 reload
