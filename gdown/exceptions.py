# -*- coding: utf-8 -*-

"""
gdown.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of gdown's exceptions.

"""


class GdownError(RuntimeError):
    """There was an ambiguous exception that occurred while handling
    your request."""


class ModuleError(GdownError):
    """Module error."""


class IpBlocked(ModuleError):
    """IP blocked by hosting."""
