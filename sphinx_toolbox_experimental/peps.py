#!/usr/bin/env python3
#
#  pep_section.py
"""
Sphinx extension which modifies the :rst:role:`pep` role to use normal (i.e. not bold) text for custom titles.

Also adds the ``pep621`` role for referencing sections within :pep:`621`.
"""
# Based on https://github.com/sphinx-doc/sphinx/blob/3.x/sphinx/roles.py
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
from typing import Dict, List, Optional, Tuple

# 3rd party
from docutils import nodes
from docutils.nodes import Node, system_message, unescape
from docutils.parsers.rst.states import Inliner
from sphinx import addnodes  # nodep
from sphinx.application import Sphinx  # nodep
from sphinx.locale import _  # nodep
from sphinx.util.docutils import ReferenceRole, SphinxRole  # nodep

__all__ = ["PEP", "PEP621Section", "setup"]


class PEP(ReferenceRole):
	"""
	Sphinx role for referencing a PEP or a section thereof.
	"""

	title: Optional[str]
	target: Optional[str]
	has_explicit_title: Optional[bool]

	def run(self) -> Tuple[List[Node], List[system_message]]:
		target_id = "index-%s" % self.env.new_serialno("index")
		entries = [("single", _("Python Enhancement Proposals; PEP %s") % self.target, target_id, '', None)]

		assert self.title is not None
		assert self.target is not None
		assert self.inliner is not None

		index = addnodes.index(entries=entries)
		target = nodes.target('', '', ids=[target_id])
		self.inliner.document.note_explicit_target(target)

		try:
			refuri = self.build_uri()
			reference = nodes.reference('', '', internal=False, refuri=refuri, classes=["pep"])
			if self.has_explicit_title:
				reference += nodes.inline(self.title, self.title)
			else:
				title = f"PEP {self.title}"
				reference += nodes.strong(title, title)
		except ValueError:
			msg = self.inliner.reporter.error(f"invalid PEP number {self.target}", line=self.lineno)
			prb = self.inliner.problematic(self.rawtext, self.rawtext, msg)  # type: ignore
			return [prb], [msg]

		return [index, target, reference], []

	def build_uri(self) -> str:
		assert self.target is not None
		assert self.inliner is not None

		base_url = self.inliner.document.settings.pep_base_url
		ret = self.target.split('#', 1)

		if len(ret) == 2:
			return base_url + f"pep-{int(ret[0]):04d}#{ret[1]}"
		else:
			return base_url + f"pep-{int(ret[0]):04d}"


class PEP621Section(PEP):
	"""
	Sphinx role for referencing a section within :pep:`621`.
	"""

	def __call__(
			self,
			name: str,
			rawtext: str,
			text: str,
			lineno: int,
			inliner: Inliner,
			options: Dict = {},
			content: List[str] = []
			) -> Tuple[List[Node], List[system_message]]:
		# if the first character is a bang, don't cross-reference at all
		self.disabled = text.startswith('!')

		matched = self.explicit_title_re.match(text)
		if matched:
			self.has_explicit_title = True
			self.title = unescape(matched.group(1))
			self.target = f"621#{unescape(matched.group(2))}"
		else:
			self.has_explicit_title = True
			self.title = unescape(text)
			self.target = f"621#{unescape(text)}"

		return SphinxRole.__call__(self, name, rawtext, text, lineno, inliner, options, content)


def setup(app: Sphinx):
	"""
	Setup :mod:`sphinx_toolbox_experimental.peps`.

	:param app: The Sphinx application.
	"""

	# 3rd party
	from docutils.parsers.rst import roles

	roles.register_local_role("pep", PEP())
	roles.register_local_role("pep621", PEP621Section())
