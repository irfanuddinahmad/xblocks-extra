SQL Grader XBlock
=================

An XBlock for grading SQL statements via a SQLite engine.

Learners write SQL queries in a code editor with syntax highlighting and
autocomplete (Ctrl+Space).  Their submission is compared against an
instructor-provided answer query; if the result sets match, the learner
receives full credit.

Built-in datasets
-----------------

The XBlock ships with two SQLite datasets ready to use:

* **rating** – ``Movie`` (mID, title, year, director), ``Reviewer`` (rID,
  name), ``Rating`` (rID, mID, stars, ratingDate)
* **social** – ``Highschooler`` (ID, name, grade), ``Friend`` (ID1, ID2),
  ``Likes`` (ID1, ID2)

Custom datasets can be added as ``.sql`` files in ``sql_grader/datasets/``.


Installation
------------

System administrator
~~~~~~~~~~~~~~~~~~~~

Add the package to your Open edX requirements::

    pip install xblocks-extra

Or install directly from the repository::

    pip install "git+https://github.com/openedx/xblocks-extra.git#egg=xblocks-extra"


Course staff
~~~~~~~~~~~~

Go to **Settings → Advanced Settings → Advanced Module List** and add::

    "sql_grader"


Codejail configuration
----------------------

The SQL grader executes learner SQL inside a codejail sandbox.  Two execution
modes are supported:

Codejail-service REST API (Tutor / production)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Starting with the Sumac release, Tutor-based deployments use the
`codejail-service <https://github.com/openedx/codejail-service>`_ container
for sandboxed execution.  When ``ENABLE_CODEJAIL_REST_SERVICE = True`` the
XBlock sends code to the service over HTTP instead of calling the local
codejail library.

For the sandbox to import ``sql_grader.problem``, the package must be
installed **inside the codejail-service sandbox venv** at image build time.
With the ``tutor-contrib-codejail`` plugin this is done via::

    tutor config save --set \
      "CODEJAIL_EXTRA_PIP_REQUIREMENTS=[\"git+https://github.com/openedx/xblocks-extra.git#egg=xblocks-extra\"]"

Then rebuild the codejail image::

    tutor images build codejail

See `openedx-platform#36639 <https://github.com/openedx/openedx-platform/issues/36639>`_
for background on the migration from local codejail to the REST service.


Local codejail sandbox (native installs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the REST service is **not** enabled, the XBlock falls back to calling
``codejail.safe_exec`` directly.  This requires a properly configured local
codejail (sandbox user, AppArmor profile, ``CODE_JAIL.python_bin`` pointing to
a real Python binary).  Refer to the
`codejail documentation <https://github.com/openedx/codejail>`_ for setup.


macOS / Docker Desktop note
~~~~~~~~~~~~~~~~~~~~~~~~~~~

AppArmor is not available on macOS.  The codejail-service runs startup safety
checks that will fail without AppArmor, causing the service to reject
requests.  For **local development only**, you can bypass this::

    docker exec -u root <codejailservice-container> \
      sed -i 's/STARTUP_SAFETY_CHECK_OK = None/STARTUP_SAFETY_CHECK_OK = True/' \
      /app/codejail_service/startup_check.py
    docker restart <codejailservice-container>

**Do not do this in production.**


Testing
-------

Studio (authoring)
~~~~~~~~~~~~~~~~~~

1. In Studio, create a new course or open an existing one.
2. Add an **Advanced** component and select **SQL Problem**.
3. In the component editor, set:

   - **Dataset**: ``rating`` (or ``social``)
   - **Answer Query**: e.g. ``SELECT title FROM Movie WHERE year > 2000``
   - **Weight**: ``1``

4. Click **Save**.

LMS (learner experience)
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Navigate to the unit containing the SQL Problem.
2. Enter a SQL query in the editor, e.g.::

       SELECT title FROM Movie WHERE year > 2000

3. Click **Submit**.  The XBlock compares your result set to the answer query:

   - **Correct**: result sets match → full score
   - **Incorrect**: result sets differ → zero score, you see your output vs.
     expected

Example test queries (rating dataset)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Answer Query (set in Studio)
     - Correct Submission
   * - ``SELECT title FROM Movie WHERE year > 2000``
     - ``SELECT title FROM Movie WHERE year > 2000``
   * - ``SELECT title, year FROM Movie ORDER BY year``
     - ``SELECT title, year FROM Movie ORDER BY year``
   * - ``SELECT name FROM Reviewer WHERE rID IN (SELECT rID FROM Rating WHERE stars = 5)``
     - ``SELECT name FROM Reviewer WHERE rID IN (SELECT rID FROM Rating WHERE stars = 5)``

To test a **wrong answer**, submit a different query — e.g. submit
``SELECT title FROM Movie WHERE year < 1990`` when the answer is
``SELECT title FROM Movie WHERE year > 2000``.

To test a **syntax error**, submit ``SELEKT title FROM Movie``.


Running unit tests
~~~~~~~~~~~~~~~~~~

From the ``xblocks-extra`` root::

    make test

Or directly::

    pytest src/sql_grader/
