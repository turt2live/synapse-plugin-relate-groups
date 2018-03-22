# synapse-plugin-relate-groups
A synapse plugin to automatically add a given group to rooms with a given alias. For help setting this up, please visit [#help:t2bot.io](https://matrix.to/#/#help:t2bot.io).

# Install

* In the same virtualenv as synapse: `pip install https://github.com/turt2live/synapse-plugin-relate-groups/tarball/master`
* Patch synapse to include [matrix-org/synapse#2870](https://github.com/matrix-org/synapse/pull/2870)

# Usage

Add this to your synapse homeserver.yaml:

```yaml
internal_api_plugins:
- module: synapse_plugin_relate_groups.RelateGroupsPlugin
  config:
    homeserver_url: 'http://localhost:8008'
    groups: 
    - group_id: '+discord:t2bot.io'
      aliases: ['#_discord.*']
      access_token: 'your_token_here' # The access token of the user to update m.room.related_groups with
```

This is well paired with the `group_id` option in your appservice's registration file:
```yaml
namespaces:
  users:
    - exclusive: true
      regex: '@_discord.*'
      group_id: '+discord:t2bot.io' # Automatically enables flair
```
