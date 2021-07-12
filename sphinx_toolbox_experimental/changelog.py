#!/usr/bin/env python3
#
#  changelog.py
"""
Sphinx extension which generates a changelog from ``versionadded`` and ``versionchanged`` directives.
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
import itertools
import re
from collections import defaultdict
from functools import partial
from operator import itemgetter
from typing import Any, Dict, List

# 3rd party
from docutils import nodes
from docutils.nodes import Node, fully_normalize_name
from docutils.statemachine import StringList
from domdf_python_tools import stringlist
from first import first
from sphinx import addnodes  # nodep
from sphinx.application import Sphinx  # nodep
from sphinx.transforms import SphinxTransform  # nodep
from sphinx.util.docutils import SphinxDirective  # nodep
from sphinx.util.nodes import clean_astext  # nodep
from sphinx.writers.latex import LaTeXTranslator  # nodep
from sphinx_toolbox.changeset import VersionChange
from sphinx_toolbox.utils import Purger

__all__ = ["Change", "Changelog", "builder_init", "setup"]

changelog_node_purger = Purger("all_changelog_node_nodes")


class Change(VersionChange):
	"""
	Modified versions of :rst:dir:`versionadded` and :rst:dir:`versionchanged` which compile a changelog.
	"""

	def add_changelog_entry(self, change_type: str):
		"""
		Record the current directive in the changelog.

		:param change_type: The type of change (add / change).
		"""

		body: List[str]

		if len(self.arguments) == 2:
			body = [self.arguments[1]]
		else:
			body = self.content  # type: ignore

		version = self.arguments[0]

		module = self.env.ref_context.get("py:module")
		object_name = first(self.env.temp_data.get("object", ()))

		# Traverse upwards until a desc_signature node
		parent = self.state.parent

		while True:
			if parent is None:
				break

			if isinstance(parent, (addnodes.desc_signature, addnodes.desc)):
				break

			parent = parent.parent

		if parent is not None:
			object_type = parent.attributes["objtype"]
		else:
			object_type = "module"

		changelog = self.env.changelog  # type: ignore
		changelog[version][change_type].append((module, object_name, body, object_type))

	def run(self) -> List[Node]:
		"""
		Process the content of the directive.
		"""

		ret = super().run()

		if self.name == "versionadded":
			self.add_changelog_entry("add")
		elif self.name == "versionchanged":
			self.add_changelog_entry("change")

		changelog_node_purger.add_node(self.env, ret[0], ret[0], self.lineno)

		return ret


class Changelog(SphinxDirective):
	"""
	Directive which adds a changelog for the given version.

	The changelog is compiled from :rst:dir:`versionadded` and :rst:dir:`versionchanged` directives.
	"""

	required_arguments = 1

	def run(self):

		ret = []

		version = self.arguments[0]
		changelog = self.env.changelog  # type: ignore
		changes = changelog[version]

		for module, object_name, body, obj_type in changes["change"]:
			obj_type_role = self.env.get_domain("py").object_types[obj_type].roles[0]

			if object_name:
				full_module_name = f":py:{obj_type_role or 'obj'}:`{module}.{object_name}`"
				sub_section_text = f"{module}.{object_name}"
			else:
				full_module_name = f":py:{obj_type_role or 'mod'}:`{module}`"
				sub_section_text = module

			sub_section_node = nodes.section()
			sub_section_node += nodes.title()
			ret.append(sub_section_node)
			changelog_node_purger.add_node(self.env, sub_section_node, sub_section_node, self.lineno)

			module_name_node = nodes.paragraph(full_module_name, full_module_name)
			self.state.nested_parse(StringList([full_module_name]), self.content_offset, module_name_node)
			sub_section_node.children[0] += module_name_node.children[1].children[0]  # type: ignore

			name = fully_normalize_name(sub_section_text)
			sub_section_node["names"].append(name)
			self.state.document.note_implicit_target(sub_section_node, sub_section_node)

			content_node = nodes.paragraph()
			self.state.nested_parse(StringList(body), self.content_offset, content_node)
			sub_section_node += content_node

		if "add" in changes:
			sub_section_text = "Additions"
			sub_section_node = nodes.section()
			sub_section_node += nodes.title(sub_section_text, sub_section_text)
			ret.append(sub_section_node)
			name = fully_normalize_name(sub_section_text)
			sub_section_node["names"].append(name)
			self.state.document.note_implicit_target(sub_section_node, sub_section_node)
			changelog_node_purger.add_node(self.env, sub_section_node, sub_section_node, self.lineno)

			content = stringlist.StringList()
			content_node = nodes.paragraph()

			additions = {k: list(v) for k, v in itertools.groupby(changes["add"], key=itemgetter(3))}

			for group in sorted(additions):
				group_name = group.capitalize()
				if group_name == "class":
					group_name = "classe"

				content.append(f":bold-title:`{group_name}s`")
				content.blankline()

				for module, object_name, body, obj_type in additions[group]:
					obj_type_role = self.env.get_domain("py").object_types[obj_type].roles[0]

					if object_name:
						content.append(f"* :py:{obj_type_role or 'obj'}:`{module}.{object_name}`")
					else:
						content.append(f"* :py:{obj_type_role or 'mod'}:`{module}`")

				content.blankline()

			self.state.nested_parse(StringList(content), self.content_offset, content_node)
			sub_section_node += content_node

		return ret


def visit_title(translator: LaTeXTranslator, node: nodes.title) -> None:
	parent = node.parent

	if getattr(translator.config, "changelog_sections_numbered", True):
		return LaTeXTranslator.visit_title(translator, node)

	if "changelog" not in parent.attributes["classes"]:
		return LaTeXTranslator.visit_title(translator, node)

	if isinstance(parent, addnodes.seealso):
		# the environment already handles this
		raise nodes.SkipNode
	elif isinstance(parent, nodes.section):
		if translator.this_is_the_title:
			return LaTeXTranslator.visit_title(translator, node)
		else:
			short = ''
			if node.traverse(nodes.image):
				short = f'[{translator.escape(" ".join(clean_astext(node).split()))}]'

			sectionlevel = translator.sectionnames[translator.sectionlevel]
			translator.body.append(r"\phantomsection\stepcounter{section}")
			translator.body.append(
					fr"\addcontentsline{{toc}}{{{sectionlevel}}}{{\protect\numberline{{\the{sectionlevel}}}{{{node.astext()}}}}}"
					)
			translator.body.append(fr'\{sectionlevel}{short}*{{')
			translator.context.append('}\n' + translator.hypertarget_to(node.parent))
	else:
		return LaTeXTranslator.visit_title(translator, node)

	translator.in_title = 1
	return None


_make_id = nodes.make_id


def make_id(string):
	if re.match(r"\d.\d.\d", string):
		return string  # .replace(".", "-")
	else:
		return _make_id(string)


nodes.make_id = make_id


class ChangelogSectionTransform(SphinxTransform):
	default_priority = 500

	def apply(self, **kwargs) -> None:

		if self.env.docname != "changelog":
			return

		for node in self.document.traverse(nodes.section):
			if re.match(r"\d.\d.\d", node.children[0].astext()):
				node.attributes["classes"].append("changelog")

				for child_node in node.traverse(nodes.section):
					child_node.attributes["classes"].append("changelog")


# class Changelog(SphinxDirective):
#
# 	def run(self):
#
# 		ret = []
#
# 		for version, changes in self.env.changelog.items():
# 			section_text = f"v{version}"
# 			section_node = nodes.section()
# 			section_node += nodes.title(section_text, section_text)
# 			name = fully_normalize_name(section_text)
# 			section_node['names'].append(name)
# 			self.state.document.note_implicit_target(section_node, section_node)
#
# 			ret.append(section_node)
##
# 			for module, object_name, body in changes["change"]:
# 				if object_name:
# 					full_module_name = f":py:obj:`{module}.{object_name}`"
# 					sub_section_text = f"{module}.{object_name}"
# 				else:
# 					full_module_name = f":py:mod:`{module}`"
# 					sub_section_text = module
#
# 				sub_section_node = nodes.section()
# 				sub_section_node += nodes.title()
# 				section_node += sub_section_node
#
# 				module_name_node = nodes.paragraph(full_module_name, full_module_name)
# 				self.state.nested_parse(StringList([full_module_name]), self.content_offset, module_name_node)
# 				sub_section_node.children[0] += module_name_node.children[1].children[0]
#
# 				name = fully_normalize_name(sub_section_text)
# 				sub_section_node['names'].append(name)
# 				self.state.document.note_implicit_target(sub_section_node, sub_section_node)
#
# 				content_node = nodes.paragraph()
# 				self.state.nested_parse(StringList(body), self.content_offset, content_node)
# 				sub_section_node += content_node
#
# 			changelog_node_purger.add_node(self.env, section_node, section_node, self.lineno)
#
# 		return ret


def builder_init(app: Sphinx) -> None:
	"""
	Initialize the changelog dictionary.

	``env.changelog`` is a dictionary mapping version numbers to a mapping
	of change types (add, change) to a list of changes.

	Each change is a tuple of ``(module, object_name, directive_body, object_type)``

	:param app: The Sphinx application.
	"""

	changelog = defaultdict(partial(defaultdict, list))
	app.env.changelog = changelog  # type: ignore


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup Sphinx Extension.

	:param app: The Sphinx application.
	"""

	app.connect("builder-inited", builder_init)
	app.connect("env-get-outdated", changelog_node_purger.get_outdated_docnames)

	app.add_directive("versionadded", Change, override=True)
	app.add_directive("versionchanged", Change, override=True)
	app.add_directive("changelog", Changelog)

	app.add_node(nodes.title, latex=(visit_title, LaTeXTranslator.depart_title))
	app.add_config_value("changelog_sections_numbered", True, "env", [bool])

	return {"parallel_read_safe": True}
