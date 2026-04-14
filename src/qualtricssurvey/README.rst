Qualtrics Survey
================

.. note::
   This XBlock is part of the `xblocks-extra <https://github.com/openedx/xblocks-extra>`_ collection.

An XBlock to ease linking to Qualtrics surveys.

The tool makes it easy for instructors to link to a Qualtrics survey
from within their course.


Installation
------------

System Administrator
~~~~~~~~~~~~~~~~~~~~

To install the XBlock on your platform, you will need to install the package collection it belongs to.
Add the following to your platform's ``requirements.txt`` file:

    xblocks-extra

You may also need to ensure this is in your ``INSTALLED_APPS``:

    qualtricssurvey


Course Staff
~~~~~~~~~~~~

To enable the XBlock in your course,
access your `Advanced Module List`:

    Settings -> Advanced Settings -> Advanced Module List

and add the following:

    qualtricssurvey


Use
---

Course Staff
~~~~~~~~~~~~

To add a Qualtrics Survey link to your course:

- go to a unit in Studio
- select "Qualtrics Survey" from the Advanced Components menu

You can now edit and preview the new component.

Using the Studio editor, you can edit the following fields:

- display name
- survey id
- university
- link text
- message
- parameter name for userid

Note: If you plan to make use of the "Param Name" field to store User ID
data, you will need to configure your Qualtrics surveys to in turn
collect that data on Qualtrics' end.


Participants
~~~~~~~~~~~~

Students click on a link within the unit and this takes them to the survey.
