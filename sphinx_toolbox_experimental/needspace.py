#!/usr/bin/env python3
#
#  needspace.py
"""
Sphinx extension which configures the LaTeX ``needspace`` package.
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
from sphinx.application import Sphinx
from sphinx.config import Config

__all__ = ["configure", "setup"]


def configure(app: Sphinx, config: Config):
	"""
	Configure Sphinx Extension.

	:param app: The Sphinx application.
	:param config:
	"""

	needspace_amount = getattr(config, "needspace_amount", "5\baselineskip")
	config.needspace_amount = needspace_amount  # type: ignore


def setup(app: Sphinx):
	"""
	Setup Sphinx Extension.

	:param app: The Sphinx application.
	"""

	app.setup_extension("sphinx_toolbox.latex")
	app.connect("config-inited", configure)

	return {"parallel_read_safe": True}
