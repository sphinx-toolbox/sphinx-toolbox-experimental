#!/usr/bin/env python3
#
#  toml.py
"""
Sphinx extension which adds the ``toml`` role for referencing sections of the TOML specification.
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
import warnings

# 3rd party
from sphinx.application import Sphinx

__all__ = ["setup"]


def setup(app: Sphinx):
	"""
	Setup :mod:`sphinx_toolbox_experimental.peps`.

	:param app: The Sphinx application.
	"""

	warnings.warn(
			"sphinx_toolbox.experimental.toml is deprecated. Please use the sphinx_packaging.toml extension instead.",
			DeprecationWarning
			)

	app.setup_extension("sphinx_packaging.toml")
