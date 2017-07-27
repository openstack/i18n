===================
Glossary Management
===================

Zanata provides suggestions for translation based on a glossary of your
language. The glossary is maintained in the i18n repository.

Glossary of your language
-------------------------

A glossary file of your language is found at
``glossary/locale/<lang>/LC_MESSAGES/glossary.po`` in the i18n repository.
The file is a usual PO file.

When you want to update a glossary of your language,
edit a corresponding glossary file using your favorite editor and
propose a change to the Gerrit review system.

Once your change is merged, the updated glossary will be uploaded
to Zanata. Note that the upload to Zanata is a **manual** process now.
Only the Zanata administrator (usually the I18n PTL and some limited folks)
can upload a glossary. If your glossary is not uploaded, contact the I18n team
or the PTL via the i18n mailing list.

.. note::

   Discuss and review glossary changes in your language team before you propose
   changes to the Gerrit review system. Reviewers in the Gerrit review system
   cannot understand your language in most cases, so they can only check syntax
   or conventions.

Master glossary
---------------

When you add a new entry to the glossary, it is highly recommended to add
the entry to the master glossary ``glossary/locale/glossary.pot``.
By doing this, all language teams can share the glossary.

The master glossary is an usual POT file.
You can edit it in your favorite editor as usual.

After you edit the master glossary, ensure to reflect the change
to all language glossary files. To do this, run the following command.

.. code-block:: console

   tox -e venv python setup.py update_catalog

Finally, propose a patch including all of the above changes to
the Gerrit review system.
