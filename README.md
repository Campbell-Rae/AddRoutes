# AddRoutes (Blender 5.x port)

A Blender add-on that lets **MIDI**, **OSC** and a remote **Android app (Blemote)** control Blender properties in real time, and lets Blender send values back out.

This repository is a fork of [slashv/AddRoutes](https://github.com/slashv/AddRoutes), updated to run on **Blender 5.3 / Python 3.13**.

## Credits

- **JPfeP** is the original author of AddRoutes (2019-2022). All of the add-on's design and functionality is his work. Project page: <http://www.jpfep.net/pages/addroutes/> and the original repository <https://github.com/JPfeP/AddRoutes>.
- **Victor Nyberg** ([slashv](https://github.com/slashv)) converted it to a Blender 4.2 extension (v0.33).
- **Campbell Rae** ported it to Blender 5.x (v0.34): replaced the MIDI library, fixed removed Blender APIs. Added the editable route name field (v0.35).

Licensed under the **GNU GPL v2 or later**, same as the original. See `LICENSE`. The original copyright notices in the source files are kept.

## What changed in this fork

### v0.35

- **Route names:** every route now keeps its numbered title ("Route #3") and has an always-visible text field directly under it for naming the route's function or intention. Handy when many controls across many MIDI devices drive things like puppeteering rigs. The name is stored with the route, saved in your .blend file, and still sent to the Blemote app. The old "Show name setting" checkbox is gone because the field is always shown.

### v0.34

- **MIDI library:** `python-rtmidi` has no prebuilt wheels for Blender 5.x's Python 3.13, so it is replaced by [rtmidi2](https://github.com/gesellkammer/rtmidi2) (MIT licence, Eduardo Moguillansky). A small wrapper, `rtmidi_compat.py`, gives the rest of the add-on the same API it used before. The MIDI backend is now loaded lazily, so the add-on still loads on a machine with no MIDI backend available.
- **Blender API:** calls that passed a context-override dict as the first argument (removed in Blender 4.0) now use `bpy.context.temp_override()`. This affected MIDI sync play/stop, the Blemote sequencer controls and the property-context lookup.
- **Envelope operator:** "Apply envelope" read `Action.groups`, which no longer exists in Blender 5.x (layered actions). It now finds the group's F-curves through the new channelbag structure, and still works with old-style actions.
- **Packaging:** the extension bundles rtmidi2 wheels for Python 3.11 and 3.13 on Linux x64, Windows x64, macOS x64 and macOS arm64. `uv.lock` and `.python-version` are updated.

## Status

- Loads in **Blender 5.3 on Ubuntu Linux**. A MIDI loopback (virtual port, note and CC out and back in) works through the new wrapper.
- **Not yet tested:** Windows, macOS, and Blender 4.2 to 5.2 (the Python 3.11 wheels are included, but unverified). The context-override and envelope changes have not been exercised with real routes.
- Bug reports are welcome. Please include the Blender version, OS, and the text from the system console.

## Install

1. Download `addroutes-0.35.0.zip` from the Releases page (or build it, see below).
2. In Blender: **Edit > Preferences > Get Extensions**, open the dropdown at the top right, choose **Install from Disk**, and pick the zip.
3. Enable **AddRoutes**.

## Building the zip from source

The zip must have `blender_manifest.toml` at its root. With Blender 4.2 or later:

```
blender --command extension build
```

Or zip the files by hand: `blender_manifest.toml`, all `*.py`, `wheels/`, `LICENSE`, `README.md`, `ChangeLog`.

## Development

Python dependencies are listed in `pyproject.toml` (`ifaddr`, `mido`, `oscpy`, `rtmidi2`) and locked with `uv`. The wheels that ship inside the extension live in `wheels/` and are referenced from `blender_manifest.toml`.

For versions of AddRoutes for older Blender releases, see the original project page linked above.
