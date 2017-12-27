import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
import supybot.schedule as schedule


class GuiltByAssociation(callbacks.Plugin):

    """
    This plugin automatically kickbans users who join the channel if they are
    joined to other channels which are considered hostile. In order to use this
    plugin, supybot.plugins.GuiltByAssociation.enable must be True.
    supybot.plugins.GuiltByAssociation.chans is a comma-separated list of
    channels to consider hostile.
    """

    _whois = {}
    _chans = []

    def __init__(self, irc):
        self.__parent = super(GuiltByAssociation, self)
        self.__parent.__init__(irc)

    def doJoin(self, irc, msg):
        channel = msg.args[0]

        if not self.registryValue('enable', channel):
            return

        self._chans = [chan.lower() for chan in
                       self.registryValue('chans', channel).split(',')]

        if not ircutils.strEqual(msg.nick, irc.nick):
            nick = ircutils.toLower(msg.nick)
            irc_ = callbacks.SimpleProxy(irc, msg)
            irc_.queueMsg(ircmsgs.whois(nick, nick))
            self._whois[(irc, nick)] = (irc, msg, {})

    # shamelessly lifted from the Network plugin
    def do311(self, irc, msg):
        nick = ircutils.toLower(msg.args[1])

        if (irc, nick) not in self._whois:
            return
        else:
            self._whois[(irc, nick)][-1][msg.command] = msg

    # These are all sent by a WHOIS response.
    do301 = do311
    do312 = do311
    do317 = do311
    do319 = do311
    do320 = do311

    def do318(self, irc, msg):
        nick = msg.args[1]
        loweredNick = ircutils.toLower(nick)

        if (irc, loweredNick) not in self._whois:
            return

        (replyIrc, replyMsg, d) = self._whois[(irc, loweredNick)]
        sourcechan = replyMsg.args[0]
        hostmask = '@'.join(d['311'].args[2:4])
        user = d['311'].args[-1]

        if '319' in d:
            channels = d['319'].args[-1].split()

            for channel in channels:
                stripped_chan = channel.lstrip('@%+~!')
                # UnrealIRCd uses & for user modes and disallows it as a
                # channel-prefix, flying in the face of the RFC.  Have to
                # handle this specially when processing WHOIS response.
                testchan = stripped_chan.lstrip('&')

                if testchan != stripped_chan and irc.isChannel(testchan):
                    stripped_chan = testchan

                stripped_chan = stripped_chan.lower()

                if stripped_chan in self._chans:
                    # user is in a hostile channel; kick ban
                    irc_ = callbacks.SimpleProxy(irc, msg)
                    irc_.queueMsg(
                        ircmsgs.ban(sourcechan,
                                    '*!{hostmask}'.format(hostmask=hostmask)))
                    irc_.queueMsg(ircmsgs.kick(sourcechan, nick))

        del self._whois[(irc, loweredNick)]

Class = GuiltByAssociation
