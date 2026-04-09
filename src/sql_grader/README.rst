SQL Grader XBlock
=================

XBlock to grade SQL statements
via a SQLite engine.


This package provides an XBlock for use with the Open EdX Platform.
Participants can be graded on SQL scripts, written in code editor
supporting:

- syntax highlighting
- autocomplete (with Ctrl+Space)



Installation
------------


System Administrator
~~~~~~~~~~~~~~~~~~~~

To install the XBlock on your platform,
add the following to your `requirements.txt` file:

    xblocks-extra



Course Staff
~~~~~~~~~~~~

To install the XBlock in your course,
access your `Advanced Module List`:

    Settings -> Advanced Settings -> Advanced Module List

and add the following:

    sql_grader
