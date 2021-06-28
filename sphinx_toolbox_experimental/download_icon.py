#!/usr/bin/env python3
#
#  download_icon.py
"""
Sphinx extension to add an icon to the left of ``download`` roles.
"""
#
# Copyright (c) 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from typing import Any, Dict

# 3rd party
from domdf_python_tools.compat import importlib_resources
from domdf_python_tools.paths import PathPlus
from sphinx.application import Sphinx

__all__ = ["copy_asset_files", "setup"]


def copy_asset_files(app: Sphinx, exception: Exception = None):
	"""
	Copy additional stylesheets into the HTML build directory.

	:param app: The Sphinx application.
	:param exception: Any exception which occurred and caused Sphinx to abort.
	"""

	if exception:  # pragma: no cover
		return

	if app.builder.format.lower() != "html":
		return

	css_static_dir = PathPlus(app.outdir) / "_static" / "css"
	css_static_dir.maybe_make(parents=True)
	(css_static_dir / "sphinx-toolbox.css").write_text(
			"""
/*  Font Awesome 4.7.0 by @davegandy - https://fontawesome.io - @fontawesome
 *  License - https://fontawesome.io/license (Font: SIL OFL 1.1, CSS: MIT License)
 */
@font-face {
    font-family: 'FontAwesome';
    src: url("../fonts/fontawesome-webfont.woff2?v=4.7.0") format("woff2"),
         url("../fonts/fontawesome-webfont.woff?v=4.7.0") format("woff"),
         url("../fonts/fontawesome-webfont.ttf?v=4.7.0") format("truetype");
    font-weight: normal;
    font-style: normal
}

.download code.download span:first-child:before {
    content: "";
    display: inline-block;
    font: normal normal normal 14px/1 FontAwesome;
    margin-right: .3em;
    margin-left: .3em;
    text-decoration: inherit;
}
"""
			)

	fonts_dir = PathPlus(app.outdir) / "_static" / "fonts"
	fonts_dir.maybe_make()

	for filename in []:
		(fonts_dir / filename).write_binary(
				importlib_resources.read_binary(
						"sphinx_toolbox_experimental.fonts",
						filename,
						)
				)


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup Sphinx Extension.

	:param app: The Sphinx app.
	"""

	app.add_css_file("css/download-icon.css")
	app.connect("build-finished", copy_asset_files)

	return {"parallel_read_safe": True}
