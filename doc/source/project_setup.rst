===================================
Enabling Translation Infrastructure
===================================

Once you have your project set up, you might want to enable
translations. For this, you first need to mark all strings so that
they can be localized, for Python projects use `oslo.i18n`_ for this
and follow the `guidelines`_.

.. _oslo.i18n: https://docs.openstack.org/oslo.i18n/
.. _guidelines: https://docs.openstack.org/oslo.i18n/latest/user/guidelines.html

Note that this is just enabling translations, the actual translations
are done by the i18n team, and they have to prioritize which projects
to translate.

First enable translation in your project, depending on whether it is a
Django project, a Python project or a ReactJS project.

.. note::

   The infra scripts consider a project as a Django project when your repository
   name ends with ``-dashboard``, ``-ui``, ``horizon`` or ``django_openstack_auth``.
   Otherwise your project will be recognized as a Python project.
   Projects using ReactJS need special treatment.

   If your repository structure is more complex, for example, with multiple
   python modules, or with both Django and Python projects, see
   :ref:`translation-setup-complex-case` as well.

Python Projects
---------------

For translation of strings in Python files, only a few changes are
needed inside a project.

.. note::
   Previously ``setup.cfg`` needed sections ``compile_catalog``,
   ``update_catalog``, and ``extract_messages`` and a ``babel.cfg``
   file. These are not needed anymore and can be removed.

Update your ``setup.cfg`` file. It should contain a ``packages`` entry
in the ``files`` section:

.. code-block:: ini

   [files]
   packages = ${MODULENAME}


Replace ``${MODULENAME}`` with the name of your main module like
``nova`` or ``novaclient``. Your i18n setup file, normally named
``_i18n.py``, should use the name of your module as domain name:

.. code-block:: python

   _translators = oslo_i18n.TranslatorFactory(domain='${MODULENAME}')

Django Projects
---------------

Update your ``setup.cfg`` file. It should contain a ``packages`` entry
in the ``files`` section:

.. code-block:: ini

   [files]
   packages = ${MODULENAME}

Create file ``babel-django.cfg`` with the following content:

.. code-block:: ini

   [python: **.py]
   [django: **/templates/**.html]
   [django: **/templates/**.csv]

Create  file ``babel-djangojs.cfg`` with the following content:

.. code-block:: ini

   [javascript: **.js]
   [angular: **/static/**.html]

ReactJS Projects
----------------

Three new dependencies are required : ``react-intl``,
``babel-plugin-react-intl``, and ``react-intl-po``.

Update your ``package.json`` file. It should contain references to the
``json2pot`` and ``po2json`` commands.

.. code-block:: javascript

    "scripts": {
        ...
        "json2pot": "rip json2pot ./i18n/extracted-messages/**/*.json -o ./i18n/messages.pot",
        "po2json": "rip po2json -m ./i18n/extracted-messages/**/*.json"
        }

The translated PO files will converted into JSON and placed into the
``./i18n/locales`` directory.

You need to update the infra scripts as well to mark a repository as
ReactJS project for translation, for details see
:ref:`translation_scripts`.

Add Translation Server Support
------------------------------

Propose a change to the ``openstack/project-config`` repository
including the following changes:

#. Set up the project on the translation server.

   Edit file ``gerrit/projects.yaml`` and add the ``translate``
   option:

   .. code-block:: yaml

      - project: openstack/<projectname>
        description: Latest and greatest cloud stuff.
        options:
          - translate

#. Add the jobs to your pipelines.

   Edit file ``zuul.d/projects.yaml`` and add a template which
   defines translation jobs to your repository:

   .. code-block:: yaml

      - project:
          name: openstack/<projectname>
          templates:
            - translation-jobs-master-stable

   The translation team is translating stable branches only for GUI
   projects, so for horizon and its plugins.

   If the repository is a GUI project, use the
   ``translation-jobs-master-stable`` template. Otherwise use the
   ``translation-jobs-master-only`` template.

When submitting the change to ``openstack/project-config`` for
review, use the ``translation_setup`` topic so it receives the
appropriate attention:

.. code-block:: console

     $ git review -t translation_setup

With these changes merged, the strings marked for translation are sent
to the translation server after each merge to your project. Also, a
periodic job is set up that checks daily whether there are translated
strings and proposes them to your project together with translation
source files. Note that the daily job will only propose translated
files where the majority of the strings are translated.

Checking Translation Imports
----------------------------

As a minimal check that the translation files that are imported are
valid, you can add to your lint target (``pep8`` or ``linters``) a
simple ``msgfmt`` test:

.. code-block:: console

   $ bash -c "find ${MODULENAME} -type f -regex '.*\.pot?' -print0| \
            xargs -0 -n 1 --no-run-if-empty msgfmt --check-format -o /dev/null"

Note that the infra scripts run the same test, so adding it to your
project is optional.


.. _translation-setup-complex-case:

More complex cases
------------------

The infra scripts for translation setup work as follows:

* The infra scripts recognize a project type based on its repository name.
  If the repository name ends with ``-dashboard``, ``-ui``, ``horizon``
  or ``django_openstack_auth``, it is treated as a Django project.
  Otherwise it is treated as a Python project.
* If your repository declares multiple python modules in ``packages`` entry
  in ``[files]`` section in ``setup.cfg``, the infra scripts run translation
  jobs for each python module.

We strongly recommend to follow the above guideline, but in some cases
this behavior does not satisfy your project structure. For example,

* Your repository contains both Django and Python code.
* Your repository defines multiple python modules, but you just want to
  run the translation jobs for specific module(s).

In such cases you can declare how each python module should be handled
manually in ``setup.cfg``. Python modules declared in ``django_modules``
and ``python_modules`` are treated as Django project and Python project
respectively. If ``django_modules`` or ``python_modules`` entry does not
exist, it is interpreted that there are no such modules.

.. code-block:: ini

   [openstack_translations]
   django_modules = module1
   python_modules = module2 module3

You also need to setup your repository following the instruction
for Python and/or Django project above appropriately.
