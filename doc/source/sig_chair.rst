====================
I18n SIG Chair Guide
====================

This chapter describes tasks for I18n SIG Chair and gives some useful hints.
If you want to be I18n SIG Chair or you new in this role, please read
carefully. For all other is this chapter informal.

.. note::

   Since I18n team previously followed as a form of official projects, some
   of the below description may assume detail tasks as PTL responsibility.
   See `Project Team Guide <https://docs.openstack.org/project-team-guide/ptl.html>`_
   which is a reference for PTLs for more information, and I18n team now
   follows as a form of working group defined as SIGs (Special Interest
   Groups).


Cross Project Liaisons
----------------------

I18n team participates in various cross project liaisons like Release
Management, Documentation and Infrastructure tasks. Many other teams are
liaisons in I18n. Visit the `Cross Project Liaisons Wiki Page <https://wiki.openstack.org/wiki/CrossProjectLiaisons>`__
and designate a person for the I18n team. Note that such liaison roles
do not have to be I18n SIG Chair. Active I18n cores are highly encouraged.

Project Goals And Translation Plan
----------------------------------

In the beginning of each cycle it is a good idea to think about goals
for the project in the next months and establish a translation plan.
Goals are maybe still left from the last cycle and are to be reviewed.
New goals are to be defined on `PTG <https://www.openstack.org/ptg/>`__
or an equivalent event. Orient the team to the `OpenStack-wide goals
<https://governance.openstack.org/tc/goals/>`__.

The translation plan is announced on `Zanata <https://translate.openstack.org>`__
and contains the projects with the highest priority in translation.
Usually these are all user-visible projects, like Horizon.


I18n Core Team
--------------

The SIG Chair is supported in the work by the `I18n core team <https://review.opendev.org/#/admin/groups/1132,members>`__.
The person designates such kind of project team members and reviews the list
from time to time. The usual work of the core team is described in the
`Project Team Guide <https://docs.openstack.org/project-team-guide/ptl.html>`__.
Of course, core team member be can also proposed by the project team.

Launchpad I18n Core Team
------------------------

As with I18n Core Team, the same things apply here. Launchpad I18n Core
Team focuses on determining the importance of a translation and/or I18n
bug and triaging bug priorities. You can find the member list on
`Launchpad I18n Core Member list <https://launchpad.net/~openstack-i18n-core>`__.

Release Management
------------------

The work for SIG Chair and Zanata administrator is described in chapter
:doc:`release_management`. This covers also questions about
string freezes and work with stable branches.

Extra-ACs Deadline
-------------------

Each cycle has a date set for Extra-ACs, e.g. `Queens Cycle
<https://releases.openstack.org/queens/schedule.html#q-extra-atcs>`__.
Maintenance on I18n site is described in chapter :ref:`project-maintenance`.
All the OpenStack members can propose extra ACs, but I18n SIG Chair is highly
encouraged to report the list in each cycle. Here are some
useful proposals as example:

* `https://review.opendev.org/#/c/488226/ <https://review.opendev.org/#/c/488226/>`__
* `https://review.opendev.org/#/c/483452/ <https://review.opendev.org/#/c/483452/>`__
* `https://review.opendev.org/#/c/451625/ <https://review.opendev.org/#/c/451625/>`__

This `Script in I18n repo <https://opendev.org/openstack/i18n/src/tools/zanata/zanata_users.py>`__
collects all users and their activities.

Daily Work
----------

Translation Job Control
~~~~~~~~~~~~~~~~~~~~~~~

Translated strings are automatically synced between translation server
and Openstack infrastructure. The procedure is robust, but sometimes
something can go wrong. For this reason there is a section
:ref:`monitoring-translation-job-status` in the infrastructure chapter.

You can check on `Gerrit <https://review.opendev.org/#/q/topic:zanata/translations+(status:open+OR+status:merged)>`__,
if the translated strings are imported by the project teams.
Core reviewers in each repository are strong encouraged to approve
translation sync patches but do not be sad if the translations are not
accepted. Zanata Sync jobs are repeated every day until they are merged.

Open reviews I18n repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check from time to time open reviews on `I18n repo
<https://review.opendev.org/#/q/project:openstack/i18n+status:open>`__.
In addition to the PTL, the core reviewers are responsible.

Launchpad bugs & blueprints
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Translation bugs are tracked on `Launchpad <https://bugs.launchpad.net/openstack-i18n>`__.
Often only the language teams are able to handle translation bugs, e.g.
wrong translation words or senses. PTL fits thereon or designates
bug triage liaison.

I18n blueprints are listed also on `Launchpad <https://blueprints.launchpad.net/openstack-i18n>`__.
In normal case a blueprint has an assignee and describes a larger course
of a process.

I18n Mailing List Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to IRC, I18n team communication takes place via a mailing
list. The `Mailing List Administrator
<http://lists.openstack.org/cgi-bin/mailman/admin/openstack-i18n>`__
is watching new subscribers, not allowed posts, and all the other
things that come with the operation of such a list.

