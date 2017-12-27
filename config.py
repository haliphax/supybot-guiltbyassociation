import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    conf.registerPlugin('GuiltByAssociation', True)


GuiltByAssociation = conf.registerPlugin('GuiltByAssociation')
conf.registerChannelValue(GuiltByAssociation, 'enable',
    registry.Boolean(False, """Determines whether or not the bot will
    automatically kickban guilty users when they join the channel."""))
conf.registerChannelValue(GuiltByAssociation, 'chans',
    registry.String('', """The list of channels (separated by comma) which will
    result in an automatic kickban if found in a user's /whois output."""))
