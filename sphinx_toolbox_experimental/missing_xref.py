#!/usr/bin/env python3
#
#  missing_xref.py
"""
Sphinx extension which ignores warnings about certain XRefs being unresolved.
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

# stdlib
import re

# 3rd party
from docutils import nodes
from sphinx.application import Sphinx  # nodep
from sphinx.environment import BuildEnvironment  # nodep
from sphinx.errors import NoUri  # nodep

__all__ = ["handle_missing_xref", "setup"]


def handle_missing_xref(
		app: Sphinx,
		env: BuildEnvironment,
		node: nodes.Node,
		contnode: nodes.Node,
		) -> None:

	if not isinstance(node, nodes.Element):
		return

	for pattern in getattr(env.config, "ignore_missing_xrefs", []):
		if re.match(pattern, node.get("reftarget", '')):
			raise NoUri


def setup(app: Sphinx):
	"""
	Setup Sphinx Extension.

	:param app: The Sphinx application.
	"""

	app.add_config_value(
			"ignore_missing_xrefs",
			default=[],
			rebuild="env",
			types=[list],  # list of strings
			)
	app.connect("missing-reference", handle_missing_xref, priority=950)
