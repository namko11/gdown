# -*- coding: utf-8 -*-

"""
gdown.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Gdown's exceptions.

"""


class GdownError(RuntimeError):
    """There was an ambiguous exception that occurred while handling
    your request."""


class ModuleError(GdownError):
    """Module error."""


class IpBlocked(ModuleError):
    """IP blocked by hosting."""


class AccountError(ModuleError):
    """An account error occured."""


class AccountBlocked(AccountError):
    """Account is temporary(?) blocked."""


class AccountRemoved(AccountError):
    """Account removed or invalid username/password."""
