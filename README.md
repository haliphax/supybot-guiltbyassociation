# supybot GuiltByAssociation plugin

This plugin will automatically kickban users who join a channel if they are
joined to other channels which are considered hostile.

## settings

- `supybot.plugins.GuiltByAssociation.enable` (Boolean): Whether or not the
  plugin is active on the selected channel
- `supybot.plugins.GuiltByAssociation.chans` (String): A comma-separated list
  of channels which are considered hostile

To set these, use the `config channel` command.
