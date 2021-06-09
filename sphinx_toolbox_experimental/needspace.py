#!/usr/bin/env python3
#
#  needspace.py
"""
Sphinx extension which configues the LaTeX ``needspace`` package.
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
from domdf_python_tools.stringlist import StringList
from sphinx import addnodes  # nodep
from sphinx.application import Sphinx  # nodep
from sphinx.config import Config  # nodep
from sphinx.writers.latex import LaTeXTranslator  # nodep

__all__ = ["configure", "setup", "visit_desc"]


def visit_desc(translator: LaTeXTranslator, node: addnodes.desc) -> None:
	"""
	Visit an :class:`addnodes.desc` node and add a custom table of contents label for the item, if required.

	:param translator:
	:param node:
	"""

	needspace_amount = getattr(translator.config, "needspace_amount", r"5\baselineskip")
	translator.body.append(fr"\needspace{{{needspace_amount}}}")

	if "sphinxcontrib.toctree_plus" in translator.config.extensions:
		# 3rd party
		from sphinxcontrib import toctree_plus  # nodep

		toctree_plus.visit_desc(translator, node)
	else:
		LaTeXTranslator.visit_desc(translator, node)


def configure(app: Sphinx, config: Config):
	"""
	Configure Sphinx Extension.

	:param app: The Sphinx application.
	:param config:
	"""

	latex_elements = getattr(config, "latex_elements", {})

	latex_extrapackages = StringList(latex_elements.get("extrapackages", ''))
	latex_extrapackages.append(r"\usepackage{needspace}")
	latex_elements["extrapackages"] = str(latex_extrapackages)

	config.latex_elements = latex_elements  # type: ignore


def setup(app: Sphinx):
	"""
	Setup Sphinx Extension.

	:param app: The Sphinx application.
	"""

	app.connect("config-inited", configure)
	app.add_node(addnodes.desc, latex=(visit_desc, LaTeXTranslator.depart_desc), override=True)
	app.add_config_value("needspace_amount", default=r"5\baselineskip", rebuild="latex", types=["str"])

	return {"parallel_read_safe": True}
