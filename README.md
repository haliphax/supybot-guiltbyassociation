# supybot GuiltByAssociation plugin

This plugin will automatically kickban users who join a channel if they are
joined to other channels which are considered hostile.

## settings

- `supybot.plugins.GuiltByAssociation.enable` _(Boolean)_: Whether or not the
  plugin is active on the selected channel
- `supybot.plugins.GuiltByAssociation.expire` _(Integer_): How long (in seconds)
  to wait before lifting the ban (`0` to disable, disabled by default)
- `supybot.plugins.GuiltByAssociation.chans` _(String)_: A comma-separated list
  of channels which are considered hostile

To set these, use the `config channel` command.
