Ansible playbooks for I18n maintenance
======================================

This folder contains Ansible playbooks for maintenance I18n work.
Typically the playbooks are running locally on user's workstation.
Ansible >= 2.2.0.0 is required to work with json_query.

Usage: "ansible-playbook <playbook.yml>"

More convenient way is to use **tox** like
   ``tox -e ansible -- ansible-playbook <playbook.yml>``.

generate_atc.yml
----------------

This playbook uses the output of zanata_stats.py, zanata_userinfo.py
and zanata_users.py and generates a list of Extra-ATCS in the target
formats for the proposal to the governance repo and the Wiki page:

http://git.openstack.org/cgit/openstack/governance/tree/reference/projects.yaml
https://wiki.openstack.org/wiki/I18nTeam/ATC_statistics
