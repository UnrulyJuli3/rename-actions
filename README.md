# Talkshow `actions` rename tool

Rename action package files to their internal names for readability. e.g. `12345.swf` -> `Scoreboard.swf`

## To target a game:

Edit the `paths` array in the Python script.

You may also change the `create_backup` parameter. `True` means it will back up your current `actions` folder to a folder named `actions-backup` if it does not already exist. `False` will disable this functionality.

## To make the game recognize the renamed files:

- Open the game's main SWF file (e.g. games/TriviaDeath/TriviaDeath.swf) in a decompiler
- Navigate to jackboxgames.talkshow.actions.ActionPackageRef
- There will be a line that contains this snippet somewhere:
```js
this._url != null ? this._url : this.getExport().configInfo.getValue(ConfigInfo.ACTION_PATH) + this._id + ".swf"
```
- In that line, the call to `this._id` (near the end) must be changed to `this._name`