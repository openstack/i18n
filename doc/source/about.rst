================
About this guide
================

This page describes the conventions and tips on writing this guide itself.

Convention
----------

The guide is written in reStructuredText (RST) markup syntax with Sphinx
extensions. Most conventions follow
`those of the openstack-manuals project
<https://docs.openstack.org/doc-contrib-guide/rst-conv.html>`__.

The following are useful links when writing documents in RST.

* `Sphinx documentation <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`__
* `Quick reStructuredText <https://docutils.sourceforge.io/docs/user/rst/quickref.html>`__

Titles
~~~~~~

The convention for heading levels is as follows::

   =========
   Heading 1
   =========

   Overline and underline with equal signs for heading 1 sections.
   This level is reserved for the title in a document.

   Heading 2
   ---------

   Underline with dashes for heading 2 sections.

   Heading 3
   ~~~~~~~~~

   Underline with tildes for heading 3 sections.

Translation
-----------

This guide itself is I18n-ed and you can translate it into your language.
To translate it, visit
`i18n <https://translate.openstack.org/project/view/i18n>`__ project in
`Zanata <https://translate.openstack.org/>`__.
Document **doc** in **i18n** project corresponds to this guide.
You can translate it in the same way as you do for other projects like
dashboard or manuals. Once the translation progress becomes higher than
the threshold (For more information on the threshold,
see :ref:`translation-jobs`),
the translated version of the guide will be published.
