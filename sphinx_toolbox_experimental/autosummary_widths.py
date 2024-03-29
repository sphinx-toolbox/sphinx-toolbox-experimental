#!/usr/bin/env python3
#
#  autosummary_widths.py
"""
Sphinx extension to allow customisation of column widths in autosummary tables with the LaTeX builder.
"""
# Based on https://github.com/sphinx-doc/sphinx/blob/3.x/sphinx/ext/autosummary/__init__.py
#
# Copyright (c) 2007-2021 by the Sphinx team.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
import re
from contextlib import suppress
from fractions import Fraction
from itertools import chain
from typing import Iterable, List, Optional, Tuple, cast

# 3rd party
import dict2css  # nodep
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from domdf_python_tools import stringlist
from domdf_python_tools.paths import PathPlus
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.ext.autosummary import autosummary_table
from sphinx.util import rst
from sphinx.util.docutils import SphinxDirective, switch_source_input
from sphinx_toolbox import latex  # nodep
from sphinx_toolbox.more_autosummary import PatchedAutosummary  # nodep

__all__ = ["AutosummaryWidths", "WidthsDirective", "configure", "setup"]


class AutosummaryWidths(PatchedAutosummary):
	"""
	Customised :rst:dir:`autosummary` directive with customisable width with the LaTeX builder.
	"""

	def get_table(self, items: List[Tuple[str, str, str, str]]) -> List[nodes.Node]:
		"""
		Generate a proper list of table nodes for autosummary:: directive.

		:param items: A list produced by :meth:`~.get_items`.
		"""

		table_spec = addnodes.tabular_col_spec()
		# table_spec['spec'] = r'\Xx{1}{3}\Xx{2}{3}'
		# table_spec['spec'] = r'\Xx{3}{8}\Xx{5}{8}'
		# table_spec['spec'] = r'\Xx{7}{16}\Xx{9}{16}'

		widths = tuple(chain.from_iterable(getattr(self.state.document, "autosummary_widths", ((1, 2), (1, 2)))))
		assert len(widths) == 4

		html_widths = getattr(self.state.document, "autosummary_html_widths", ((1, 10), (9, 10)))
		assert len(html_widths) == 2

		if "latex" in self.env.app.config.autosummary_widths_builders:
			table_spec["spec"] = r'\Xx{%d}{%d}\Xx{%d}{%d}' % widths
		else:
			table_spec["spec"] = r'\Xx{1}{2}\X{1}{2}'

		table = autosummary_table('')

		if "html" in self.env.app.config.autosummary_widths_builders:
			real_table = nodes.table('', classes=["longtable", "autosummary"])
		else:
			real_table = nodes.table('', classes=["longtable"])

		table.append(real_table)

		group = nodes.tgroup('', cols=2)
		real_table.append(group)

		if "html" in self.env.app.config.autosummary_widths_builders:
			group.append(nodes.colspec('', colwidth=html_widths[0][0] * 100 / html_widths[0][1]))
			group.append(nodes.colspec('', colwidth=html_widths[1][0] * 100 / html_widths[1][1]))
		else:
			group.append(nodes.colspec('', colwidth=10))
			group.append(nodes.colspec('', colwidth=90))

		body = nodes.tbody('')
		group.append(body)

		def append_row(*column_texts: str) -> None:
			row = nodes.row('')
			source, line = self.state_machine.get_source_and_line()

			for text in column_texts:
				node = nodes.paragraph('')
				vl = StringList()
				vl.append(text, f"{source}:{line:d}:<autosummary>")

				with switch_source_input(self.state, vl):
					self.state.nested_parse(vl, 0, node)

					with suppress(IndexError):
						if isinstance(node[0], nodes.paragraph):
							node = node[0]

					row.append(nodes.entry('', node))

			body.append(row)

		for name, sig, summary, real_name in items:
			col1 = f":obj:`{name} <{real_name}>`"

			if "nosignatures" not in self.options:
				if "html" in self.env.app.config.autosummary_widths_builders:
					col1 += f"\\ {rst.escape(sig).replace('(', '(​')}"
				else:
					col1 += f"\\ {rst.escape(sig)}"

			append_row(col1, summary)

		return [table_spec, table]


class WidthsDirective(SphinxDirective):
	"""
	Sphinx directive which configures the column widths of an :rst:dir:`autosummary` table
	for the remainder of the document, or until the next `autosummary-widths` directive.
	"""  # noqa: D400

	required_arguments = 1
	optional_arguments = 1
	option_spec = {"html": directives.unchanged_required}

	@staticmethod
	def parse_widths(raw_widths: Iterable[str]) -> List[Tuple[int, int]]:
		"""
		Parse a width string (as a vulgar fraction) into a list of 2-element ``(numerator, denominator)`` tuples.

		:param raw_widths:
		"""

		widths = [cast(Tuple[int, int], tuple(map(int, arg.split('/')))) for arg in raw_widths]

		if len(widths) == 1:
			left_width = Fraction(*widths[0])
			right_width = 1 - left_width
			widths.append((right_width.numerator, right_width.denominator))

		return widths

	def run(self) -> List:
		"""
		Process the directive's arguments.
		"""

		if "html" in self.options:
			html_widths = self.parse_widths(re.split(r"\s+", self.options["html"]))
		else:
			html_widths = [(1, 10), (9, 10)]

		self.state.document.autosummary_widths = self.parse_widths(self.arguments)  # type: ignore[attr-defined]
		self.state.document.autosummary_html_widths = html_widths  # type: ignore[attr-defined]

		return []


def configure(app: Sphinx, config: Config):
	"""
	Configure :mod:`sphinx_toolbox_experimental.autosummary_widths`.

	:param app: The Sphinx application.
	:param config:
	"""

	latex_elements = getattr(config, "latex_elements", {})

	latex_preamble = stringlist.StringList(latex_elements.get("preamble", ''))
	latex_preamble.blankline()
	latex_preamble.append(r"\makeatletter")
	latex_preamble.append(r"\newcolumntype{\Xx}[2]{>{\raggedright\arraybackslash}p{\dimexpr")
	latex_preamble.append(r"    (\linewidth-\arrayrulewidth)*#1/#2-\tw@\tabcolsep-\arrayrulewidth\relax}}")
	latex_preamble.append(r"\makeatother")
	latex_preamble.blankline()

	latex_elements["preamble"] = str(latex_preamble)
	config.latex_elements = latex_elements  # type: ignore


def copy_asset_files(app: Sphinx, exception: Optional[Exception] = None):
	"""
	Copy the custom CSS file.

	:param app: The Sphinx application.
	:param exception: Any exception which occurred and caused Sphinx to abort.
	"""

	if exception:  # pragma: no cover
		return

	if app.builder.name.lower() != "html":
		return

	css_static_dir = PathPlus(app.outdir) / "_static" / "css"
	css_static_dir.maybe_make(parents=True)

	dict2css.dump(
			{".longtable.autosummary": {"width": "100%"}},
			css_static_dir / "autosummary-widths.css",
			)


def setup(app: Sphinx):
	"""
	Setup :mod:`sphinx_toolbox_experimental.autosummary_widths`.

	:param app: The Sphinx application.
	"""

	app.add_config_value("autosummary_widths_builders", ["html", "latex"], rebuild="env", types=[list])
	app.add_directive("autosummary", AutosummaryWidths, override=True)
	app.add_directive("autosummary-widths", WidthsDirective)
	app.connect("build-finished", latex.replace_unknown_unicode)
	app.connect("build-finished", copy_asset_files)
	app.connect("config-inited", configure)
	app.add_css_file("css/autosummary-widths.css")
