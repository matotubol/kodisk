# Stream Cinema

This plugin includes optional remote-control features. Remote commands can be sent using the `cmd://` URL scheme or over the WebSocket service.

Only a small set of Kodi built-in commands is allowed. When a `cmd://` link is processed the command is validated and anything outside the whitelist is ignored and logged. Allowed command prefixes are:

- `Action(`
- `PlayMedia(`
- `RunPlugin(`
- `Container.Update`
- `Container.Refresh`
- `ActivateWindow(`
- `Addon.OpenSettings(`
- `SetFocus(`
- `UpdateAddonRepos`
- `UpdateLocalAddons`

Any other command will be skipped for safety.
