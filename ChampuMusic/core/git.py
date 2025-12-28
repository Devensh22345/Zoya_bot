"""
Git features are DISABLED on Heroku.
Heroku dynos do not support system git operations.
"""

from ..logging import LOGGER


def git():
    LOGGER(__name__).warning(
        "Git update feature is disabled on Heroku deployment."
    )
