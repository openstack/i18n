======================
Translation Statistics
======================

There are several ways to know your translation activity.

Zanata
======

Zanata provides ways to know your activity on Zanata.

* `Dashboard <https://translate.openstack.org/dashboard/>`__ page
  shows your recent activity statistics this month and detail activity.
* `Profile <https://translate.openstack.org/profile/>`__ page
  provides more nice statistics view.
  It shows your statistics in this month and last month.

Note that you need to log into Zanata to see your activity in the above pages.

Stackalytics
============

`Stackalytics <http://stackalytics.com/>`__ is a popular web site
which allows us to know various statistics related to OpenStack.
It supports translation statistics :)

Visit `Stackalytics <http://stackalytics.com/>`__ and
choose ``Translations`` as ``Metric`` dropdown menu at the upper-right.

FAQ: I cannot find my name in Stackalytics.
-------------------------------------------

There is a case where you cannot see your translation statistics
in Stackalytics even after you translate strings in Zanata.

Do you use a same ID for launchpad and Zanata?
If they are different, Stackalytics will not find your translation counts.

In this case, you need to let Stackalytics know your ID mappings.
To do this, you need to add your user data into ``etc/detault_data.json``
in `the Stackalytics repository <http://git.openstack.org/cgit/openstack/stackalytics/>`__.
An example is https://review.openstack.org/#/c/284638/1/etc/default_data.json.

If you are lucky to use a same name for launchpad and Zanata IDs,
you do not need to do the above.
Stackalytics will find your statistics automatically.

Also, since Stackalytics uses the `translator list
<http://git.openstack.org/cgit/openstack/i18n/tree/tools/zanata/translation_team.yaml>`_
as of now, if you cannot find your name or ID in Stackalytics, please email
I18n mailing list, or submit a update patch to add your ID by yourself.
