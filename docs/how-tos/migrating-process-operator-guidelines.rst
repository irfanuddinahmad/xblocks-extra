Migrate your Open edX instance from Standalone XBlock Packages to xblocks-extra
===============================================================================

This guide walks operators through replacing standalone XBlock packages 
with ``xblocks-extra``.

Before following this guide, familiarise yourself with the
xblocks-extra `README <https://github.com/openedx/xblocks-extra>`_.

.. contents::
   :local:
   :depth: 2


Packaging Insights:
-------------------

Every XBlock retains the same entry point key and Python import path it had in
its standalone package. For example, ``xblock-submit-and-compare`` registered
its XBlock under the entry point key ``submit-and-compare``, importable as
``submit_and_compare.xblocks:SubmitAndCompareXBlock`` — both are unchanged in
``xblocks-extra``.

For further details on the migration process, see :doc:`migration-process-developer-guidelines`.


Before You Migrate
------------------

* **Python 3.12 is required.** ``xblocks-extra`` supports Python 3.12 only.
  The Verawood release of Open edX likewise requires Python 3.12, so no
  additional version change is needed if you are already on Verawood.
* You must **not** have both a standalone package and ``xblocks-extra``
  installed at the same time. Because both provide the same XBlock entrypoint,
  having both installed will cause runtime error (i-e- AmbiguousPluginError).
* If you only use a subset of these XBlocks, you still install the full
  ``xblocks-extra`` package. The XBlocks you do not use simply remain
  unconfigured and inactive.

Step-by-Step Migration
----------------------

1. Identify which standalone packages you have installed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check your requirements files and installed environment::

    pip show audio-xblock feedback-xblock xblock-free-text-response \
              openedx-xblock-image-modal xblock_qualtrics_survey \
              xblock-sql-grader xblock-submit-and-compare

Make a note of which packages are present so you know what to remove.

2. Remove the standalone packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove every standalone package you identified. You can remove them all at
once::

    pip uninstall -y audio-xblock feedback-xblock xblock-free-text-response \
                     openedx-xblock-image-modal xblock_qualtrics_survey \
                     xblock-sql-grader xblock-submit-and-compare

3. Install xblocks-extra
~~~~~~~~~~~~~~~~~~~~~~~~

Install the consolidated package::

    pip install xblocks-extra

4. Run your smoke tests
~~~~~~~~~~~~~~~~~~~~~~~

Restart your LMS/CMS processes and confirm that existing course content using
any of these XBlock types still renders correctly. Because the XBlock entry points
and import paths are unchanged, no course re-publish or content migration is needed.
