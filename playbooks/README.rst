Ansible playbooks for I18n maintenance
======================================

This folder contains Ansible playbooks for maintenance I18n work.
Typically the playbooks are running locally on user's workstation.
Ansible >= 2.9.22 is required to work with json_query and Jinja2.

Usage: "ansible-playbook <playbook.yml>"

More convenient way is to use **tox** like
   ``tox -e ansible -- ansible-playbook <playbook.yml>``.

generate_ac.yml
----------------

This playbook uses the output of zanata_stats.py, zanata_userinfo.py
and zanata_users.py and generates a list of extra-ACs (previously
extra-ATCs) in the target formats for the proposal to the governance repo
and the Wiki page:

https://opendev.org/openstack/governance/src/branch/master/reference/sigs-repos.yaml
https://wiki.openstack.org/wiki/I18nTeam/AC_statistics
