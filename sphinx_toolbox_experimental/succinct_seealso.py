#!/usr/bin/env python3
#
#  succinct_seealso.py
"""
Sphinx extension which customises :rst:dir:`seealso` directives to be on one line with the LaTeX builder.
"""
#
# Copyright (c) 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

# 3rd party
from sphinx import addnodes  # nodep
from sphinx.application import Sphinx  # nodep
from sphinx.locale import admonitionlabels  # nodep
from sphinx.writers.latex import LaTeXTranslator  # nodep

__all__ = ["depart_seealso", "setup", "visit_seealso"]


def visit_seealso(translator: LaTeXTranslator, node: addnodes.seealso) -> None:
	"""
	Visit an :class:`addnodes.seealso`` node.

	:param translator:
	:param node:
	"""

	# translator.body.append('\n\n\\begin{description}\\item[{%s:}] \\leavevmode' % admonitionlabels['seealso'])
	# translator.body.append('\n\n\\sphinxstrong{%s:} ' % admonitionlabels["seealso"])
	if len(node) > 1:
		LaTeXTranslator.visit_seealso(translator, node)
	else:
		translator.body.append('\n\n\\sphinxstrong{%s:} ' % admonitionlabels["seealso"])


def depart_seealso(translator: LaTeXTranslator, node: addnodes.seealso) -> None:
	"""
	Depart an :class:`addnodes.seealso`` node.

	:param translator:
	:param node:
	"""

	# translator.body.append("\\end{description}\n\n")
	translator.body.append("\n\n")


def setup(app: Sphinx):
	"""
	Setup :mod:`sphinx_toolbox_experimental.succinct_seealso`.

	:param app: The Sphinx application.
	"""

	app.add_node(addnodes.seealso, latex=(visit_seealso, depart_seealso), override=True)
