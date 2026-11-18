# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 Campbell Rae
# Part of the Blender 5.x port of AddRoutes by JPfeP.
"""
Small python-rtmidi style wrapper around rtmidi2.

AddRoutes was written against python-rtmidi, which has no prebuilt wheels for
the Python used by Blender 5.x (3.13). rtmidi2 does, so this module gives the
rest of the add-on the API it already expects:

    MidiIn.get_ports() / open_port() / is_port_open() / close_port() / delete()
    MidiIn.get_message()  -> (message, deltatime) or None
    MidiOut.send_message(list_of_bytes)
    open_midiinput() / open_midioutput()

The underlying rtmidi2 client is created lazily, so a machine without a MIDI
backend (for example no ALSA sequencer) can still load the add-on.
"""

import rtmidi2


class _Base:
    _cls = None
    _default_name = "Blender"

    def __init__(self, name=None):
        self._name = name or self._default_name
        self._dev = None
        self._open = False

    def _device(self):
        if self._dev is None:
            self._dev = self._cls(self._name)
        return self._dev

    def get_ports(self):
        try:
            return list(self._device().ports)
        except Exception:
            return []

    def open_port(self, port=0):
        """Open a port by index or by exact name."""
        ports = self.get_ports()
        if isinstance(port, str):
            if port not in ports:
                raise ValueError("MIDI port not found: %r" % port)
            port = ports.index(port)
        self._device().open_port(port)
        self._open = True

    def open_virtual_port(self, name=None):
        self._device().open_virtual_port(name or self._name)
        self._open = True

    def is_port_open(self):
        return self._open

    def close_port(self):
        if self._dev is not None and self._open:
            try:
                self._dev.close_port()
            except Exception:
                pass
        self._open = False

    def delete(self):
        self.close_port()
        self._dev = None


class MidiIn(_Base):
    _cls = rtmidi2.MidiIn
    _default_name = "Blender In"

    def get_message(self):
        if self._dev is None or not self._open:
            return None
        msg = self._dev.get_message()
        if msg is None:
            return None
        return list(msg), 0.0


class MidiOut(_Base):
    _cls = rtmidi2.MidiOut
    _default_name = "Blender Out"

    def send_message(self, msg):
        if self._dev is None or not self._open:
            return
        self._dev.send_raw(*msg)


def _open(cls, port, use_virtual, client_name, virtual_name):
    dev = cls(client_name)
    if use_virtual:
        dev.open_virtual_port(virtual_name)
        return dev, virtual_name
    dev.open_port(port)
    return dev, port


def open_midiinput(port=None, use_virtual=False, interactive=False, client_name="Blender In",
                   port_name="Blender Virtual In"):
    return _open(MidiIn, port, use_virtual, client_name, port_name)


def open_midioutput(port=None, use_virtual=False, interactive=False, client_name="Blender Out",
                    port_name="Blender Virtual Out"):
    return _open(MidiOut, port, use_virtual, client_name, port_name)
