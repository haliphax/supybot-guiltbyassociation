"""
Automatically kickbans users who join a channel if they are joined to other
channels which are considered hostile.
"""

import supybot
import supybot.world as world

__version__ = ""
__author__ = supybot.Author('haliphax', 'haliphax', 'haliphax@nope')
__contributors__ = {}
__url__ = 'https://github.com/haliphax/supybot-guiltbyassociation'

import config
import plugin
reload(plugin)

if world.testing:
    import test

Class = plugin.Class
configure = config.configure
