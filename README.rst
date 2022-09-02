==============================
sphinx_toolbox_experimental
==============================

.. start short_desc

**Experimental Sphinx Extensions.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/workflows/Linux/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/workflows/Windows/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/workflows/macOS/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/workflows/Flake8/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/workflows/mypy/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/sphinx-toolbox/sphinx-toolbox-experimental/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/sphinx-toolbox/sphinx-toolbox-experimental/
	:alt: Requirements Status

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/sphinx-toolbox/sphinx-toolbox-experimental?logo=codefactor
	:target: https://www.codefactor.io/repository/github/sphinx-toolbox/sphinx-toolbox-experimental
	:alt: CodeFactor Grade

.. |license| image:: https://img.shields.io/github/license/sphinx-toolbox/sphinx-toolbox-experimental
	:target: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/sphinx-toolbox/sphinx-toolbox-experimental
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/sphinx-toolbox/sphinx-toolbox-experimental/v0.0.0
	:target: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/sphinx-toolbox/sphinx-toolbox-experimental
	:target: https://github.com/sphinx-toolbox/sphinx-toolbox-experimental/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022
	:alt: Maintenance

.. end shields


Installation
--------------

.. start installation

``sphinx-toolbox-experimental`` can be installed from GitHub.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install git+https://github.com/sphinx-toolbox/sphinx-toolbox-experimental

.. end installation


sphinx_toolbox_experimental.autosummary_widths
-------------------------------------------------

Sphinx extension to allow customisation of column widths in autosummary tables with the LaTeX builder.


sphinx_toolbox_experimental.changelog
-------------------------------------------------

Sphinx extension which generates a changelog from ``versionadded`` and ``versionchanged`` directives.

The changelog can be added with the ``changelog`` directive. The directive takes a single argument, the version number to display the changelog for.


sphinx_toolbox_experimental.html_section
-----------------------------------------

Sphinx extension to hide section headers with non-HTML builders.

Usage
^^^^^^^

.. code-block:: rest

	Contents
	-----------

	.. html-section::

The section label ``Contents`` will only be shown with the HTML builder.
However, the section content will still be visible.
Consider using Sphinx's ``.. only:: html`` directive for that.


sphinx_toolbox_experimental.missing_xref
-------------------------------------------------

Sphinx extension which ignores warnings about certain XRefs being unresolved.
The warnings to ignore are determined by a list of patterns (for ``re.match``) defined in the ``ignore_missing_xrefs`` option in ``conf.py``.


sphinx_toolbox_experimental.needspace
-------------------------------------------------

Sphinx extension which configures the LaTeX ``needspace`` package.
The default is to add ``\needspace{5\baselineskip}`` before each ``addnodes.desc`` node (i.e. a function or class description).
The space can be adjusted with the ``needspace_amount`` option in ``conf.py``.


sphinx_toolbox_experimental.peps
-------------------------------------------------

Sphinx extension which modifies the ``pep`` role to use normal (i.e. not bold) text for custom titles.

Also adds the ``pep621`` role for referencing sections within PEP 621,
and the ``core-meta`` role for referencing sections in Python's core metadata`.


sphinx_toolbox_experimental.rst_field
-------------------------------------------------

Sphinx extension to add a ``field`` directive to the ``rst`` domain for documenting a reST directive field..


sphinx_toolbox_experimental.succinct_seealso
-------------------------------------------------

Sphinx extension which customises ``seealso`` directives to be on one line with the LaTeX builder.

sphinx_toolbox_experimental.toml
-------------------------------------------------

Sphinx extension which adds the ``toml`` role for referencing sections of the TOML specification.

The TOML version can be set with the ``toml_spec_version`` option in ``conf.py``.
