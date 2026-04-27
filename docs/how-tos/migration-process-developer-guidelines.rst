Move XBlock package to xblocks-extra : Developers Guide
========================================================

This guide explains how to migrate an existing XBlock into this repository while
preserving its original package path for drop-in replacement.

Key Principle: Package Path Preservation
----------------------------------------

This repository maintains each xblock's **original package path** using a ``src/``
layout. Packages live in ``src/`` but are installed without the ``src`` prefix.

For example, if you're migrating ``foo_xblock``:

- Place the package at ``src/foo_xblock/``
- It becomes importable as ``foo_xblock`` (not ``src.foo_xblock``)

This allows migrated xblocks to serve as drop-in replacements for the original
packages without requiring changes to imports or entry points.

Migration Checklist
-------------------

1. **Copy the XBlock Package**

   Copy the xblock package directory to the ``src/`` directory::

       cp -r /path/to/original/foo_xblock ./src/foo_xblock

2. **Update pyproject.toml**

   Add the entry point::

       [project.entry-points."xblock.v1"]
       foo = "foo_xblock:FooXBlock"

   Add to known first-party packages for Ruff::

       [tool.ruff.lint.isort]
       known-first-party = ["foo_xblock"]

   Add to coverage sources::

       [tool.coverage.run]
       source = ["src/foo_xblock"]

3. **Add Dependencies**

   If the xblock has additional dependencies beyond XBlock and Django, add them
   to the main ``dependencies`` list::

       dependencies = [
           "XBlock",
           "Django>=4.2",
           "some-new-dependency",
       ]

4. **Migrate Tests**

   Tests can live with the xblock or in the top-level ``tests/`` directory::

       src/foo_xblock/tests/test_foo.py  # preferred: tests with the xblock
       # or
       tests/test_foo_xblock.py  # for integration tests

5. **Update Imports (if needed)**

   If the original xblock had imports like::

       from foo_xblock.foo import FooXBlock

   These should continue to work unchanged. If the original used relative imports,
   ensure they still work in the new location.

6. **Run Tests and Linting**

   Verify everything works::

       make lint
       make test

7. **Create a Pull Request**

   Submit a PR with:

   - The xblock package in ``src/``
   - Updated ``pyproject.toml``
   - Any new tests

Example: Adding ``example_xblock``
----------------------------------

Here's a complete example of adding an xblock called ``example_xblock``:

1. Copy the package to ``src/``::

       src/example_xblock/
       ├── __init__.py
       ├── example.py
       └── tests/
           └── test_example.py

2. Update ``pyproject.toml``:

   .. code-block:: toml

       [project.entry-points."xblock.v1"]
       example = "example_xblock:ExampleXBlock"

       [tool.ruff.lint.isort]
       known-first-party = ["example_xblock"]

       [tool.coverage.run]
       source = ["src/example_xblock"]

3. Run verification::

       pip install -e ".[dev,test]"
       make lint
       make test

Handling Multiple XBlocks
-------------------------

When multiple xblocks are in the repository, each lives in its own directory
under ``src/``. The ``pyproject.toml`` configuration accumulates::

    src/
    ├── foo_xblock/
    ├── bar_xblock/
    └── baz_xblock/

    [project.entry-points."xblock.v1"]
    foo = "foo_xblock:FooXBlock"
    bar = "bar_xblock:BarXBlock"
    baz = "baz_xblock:BazXBlock"

    [tool.ruff.lint.isort]
    known-first-party = ["foo_xblock", "bar_xblock", "baz_xblock"]

    [tool.coverage.run]
    source = ["src/foo_xblock", "src/bar_xblock", "src/baz_xblock"]
