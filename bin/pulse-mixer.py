#!/usr/bin/env python3
'''Usage of pulsemixer:
  -h, --help            show this help message and exit
  -v, --version         print version
  -l, --list            list everything
  --list-sources        list sources
  --list-sinks          list sinks
  --id ID               specify ID. If no ID specified - default sink is used
  --set-volume n        set volume for ID
  --set-volume-all n:n  set volume for ID (for every channel)
  --change-volume +-n   change volume for ID
  --get-mute            get mute for ID
  --toggle-mute         toggle mute for ID
  --get-volume          get volume for ID
  --mute                mute ID
  --unmute              unmute ID
  --server              choose the server to connect to
  --color n             0 no color, 1 color currently selected, 2 full-color (default)
  --no-mouse            disable mouse support'''

VERSION = '1.4.0'

from ctypes import *
from time import sleep
import operator, functools
import sys
import curses
import re
import getopt
import signal
import traceback
from os import environ, getenv
from pprint import pprint

#########################################################################################
# v bindings

try:
    p = CDLL("libpulse.so.0")
except Exception as err:
    sys.exit(err)

PA_VOLUME_NORM = 65536
PA_CHANNELS_MAX = 32
PA_USEC_T = c_uint64

bar_style = getenv('PULSEMIXER_BAR_STYLE', '┌╶┐╴└┘▮- ──').ljust(11, '?')
BAR_TOP_LEFT       = bar_style[0]
BAR_LEFT_MONO      = bar_style[1]
BAR_TOP_RIGHT      = bar_style[2]
BAR_RIGHT_MONO     = bar_style[3]
BAR_BOTTOM_LEFT    = bar_style[4]
BAR_BOTTOM_RIGHT   = bar_style[5]
BAR_ON             = bar_style[6]
BAR_OFF            = bar_style[7]
ARROW              = bar_style[8]
ARROW_FOCUSED      = bar_style[9]
ARROW_LOCKED       = bar_style[10]


class PA_MAINLOOP(Structure):
    pass


class PA_MAINLOOP_API(Structure):
    pass


class PA_CONTEXT(Structure):
    pass


class PA_OPERATION(Structure):
    pass


class PA_PROPLIST(Structure):
    pass


class PA_SAMPLE_SPEC(Structure):
    _fields_ = [
        ("format", c_int),
        ("rate", c_uint32),
        ("channels", c_uint32)
    ]


class PA_CHANNEL_MAP(Structure):
    _fields_ = [
        ("channels", c_uint8),
        ("map", c_int * PA_CHANNELS_MAX)
    ]


class PA_CVOLUME(Structure):
    _fields_ = [
        ("channels", c_uint8),
        ("values", c_uint32 * PA_CHANNELS_MAX)
    ]


class PA_PORT_INFO(Structure):
    _fields_ = [
        ('name', c_char_p),
        ('description', c_char_p),
        ('priority', c_uint32),
    ]


class PA_SINK_INPUT_INFO(Structure):
    _fields_ = [
        ("index",           c_uint32),
        ("name",            c_char_p),
        ("owner_module",    c_uint32),
        ("client",          c_uint32),
        ("sink",            c_uint32),
        ("sample_spec",     PA_SAMPLE_SPEC),
        ("channel_map",     PA_CHANNEL_MAP),
        ("volume",          PA_CVOLUME),
        ("buffer_usec",     PA_USEC_T),
        ("sink_usec",       PA_USEC_T),
        ("resample_method", c_char_p),
        ("driver",          c_char_p),
        ("mute",            c_int),
        ("proplist", POINTER(PA_PROPLIST))
    ]


class PA_SINK_INFO(Structure):
    _fields_ = [
        ("name",                c_char_p),
        ("index",               c_uint32),
        ("description",         c_char_p),
        ("sample_spec",         PA_SAMPLE_SPEC),
        ("channel_map",         PA_CHANNEL_MAP),
        ("owner_module",        c_uint32),
        ("volume",              PA_CVOLUME),
        ("mute",                c_int),
        ("monitor_source",      c_uint32),
        ("monitor_source_name", c_char_p),
        ("latency",             PA_USEC_T),
        ("driver",              c_char_p),
        ("flags",               c_int),
        ("proplist",            POINTER(PA_PROPLIST)),
        ("configured_latency",  PA_USEC_T),
        ('base_volume',         c_int),
        ('state',               c_int),
        ('n_volume_steps',      c_int),
        ('card',                c_uint32),
        ('n_ports',             c_uint32),
        ('ports',               POINTER(POINTER(PA_PORT_INFO))),
        ('active_port',         POINTER(PA_PORT_INFO))
    ]


class PA_SOURCE_OUTPUT_INFO(Structure):
    _fields_ = [
        ("index",           c_uint32),
        ("name",            c_char_p),
        ("owner_module",    c_uint32),
        ("client",          c_uint32),
        ("source",          c_uint32),
        ("sample_spec",     PA_SAMPLE_SPEC),
        ("channel_map",     PA_CHANNEL_MAP),
        ("buffer_usec",     PA_USEC_T),
        ("source_usec",     PA_USEC_T),
        ("resample_method", c_char_p),
        ("driver",          c_char_p),
        ("proplist",        POINTER(PA_PROPLIST)),
        ("corked",          c_int),
        ("volume",          PA_CVOLUME),
        ("mute",            c_int),
    ]


class PA_SOURCE_INFO(Structure):
    _fields_ = [
        ("name",                 c_char_p),
        ("index",                c_uint32),
        ("description",          c_char_p),
        ("sample_spec",          PA_SAMPLE_SPEC),
        ("channel_map",          PA_CHANNEL_MAP),
        ("owner_module",         c_uint32),
        ("volume",               PA_CVOLUME),
        ("mute",                 c_int),
        ("monitor_of_sink",      c_uint32),
        ("monitor_of_sink_name", c_char_p),
        ("latency",              PA_USEC_T),
        ("driver",               c_char_p),
        ("flags",                c_int),
        ("proplist",             POINTER(PA_PROPLIST)),
        ("configured_latency",   PA_USEC_T),
        ('base_volume',          c_int),
        ('state',                c_int),
        ('n_volume_steps',       c_int),
        ('card',                 c_uint32),
        ('n_ports',              c_uint32),
        ('ports',                POINTER(POINTER(PA_PORT_INFO))),
        ('active_port',          POINTER(PA_PORT_INFO))
    ]


class PA_CLIENT_INFO(Structure):
    _fields_ = [
        ("index",        c_uint32),
        ("name",         c_char_p),
        ("owner_module", c_uint32),
        ("driver",       c_char_p)
    ]


class PA_CARD_PROFILE_INFO(Structure):
    _fields_ = [
        ('name', c_char_p),
        ('description', c_char_p),
        ('n_sinks', c_uint32),
        ('n_sources', c_uint32),
        ('priority', c_uint32),
    ]


class PA_CARD_INFO(Structure):
    _fields_ = [
        ('index', c_uint32),
        ('name', c_char_p),
        ('owner_module', c_uint32),
        ('driver', c_char_p),
        ('n_profiles', c_uint32),
        ('profiles', POINTER(PA_CARD_PROFILE_INFO)),
        ('active_profile', POINTER(PA_CARD_PROFILE_INFO)),
        ('proplist', POINTER(PA_PROPLIST)),
    ]


class PA_SERVER_INFO(Structure):
    _fields_ = [
        ('user_name', c_char_p),
        ('host_name', c_char_p),
        ('server_version', c_char_p),
        ('server_name', c_char_p),
        ('sample_spec', PA_SAMPLE_SPEC),
        ('default_sink_name', c_char_p),
        ('default_source_name', c_char_p),
    ]

PA_STATE_CB_T = CFUNCTYPE(c_int, POINTER(PA_CONTEXT), c_void_p)

PA_SIGNAL_CB_T = CFUNCTYPE(c_void_p,
                           POINTER(PA_MAINLOOP_API),
                           POINTER(c_int),
                           c_int,
                           c_void_p)

PA_CLIENT_INFO_CB_T = CFUNCTYPE(c_void_p,
                                POINTER(PA_CONTEXT),
                                POINTER(PA_CLIENT_INFO),
                                c_int,
                                c_void_p)

PA_SINK_INPUT_INFO_CB_T = CFUNCTYPE(c_int,
                                    POINTER(PA_CONTEXT),
                                    POINTER(PA_SINK_INPUT_INFO),
                                    c_int,
                                    c_void_p)

PA_SINK_INFO_CB_T = CFUNCTYPE(c_int,
                              POINTER(PA_CONTEXT),
                              POINTER(PA_SINK_INFO),
                              c_int,
                              c_void_p)

PA_SOURCE_OUTPUT_INFO_CB_T = CFUNCTYPE(c_int,
                                       POINTER(PA_CONTEXT),
                                       POINTER(PA_SOURCE_OUTPUT_INFO),
                                       c_int,
                                       c_void_p)

PA_SOURCE_INFO_CB_T = CFUNCTYPE(c_int,
                                POINTER(PA_CONTEXT),
                                POINTER(PA_SOURCE_INFO),
                                c_int,
                                c_void_p)

PA_CONTEXT_SUCCESS_CB_T = CFUNCTYPE(c_void_p,
                                    POINTER(PA_CONTEXT),
                                    c_int,
                                    c_void_p)

PA_CARD_INFO_CB_T = CFUNCTYPE(None,
                              POINTER(PA_CONTEXT),
                              POINTER(PA_CARD_INFO),
                              c_int,
                              c_void_p)

PA_SERVER_INFO_CB_T = CFUNCTYPE(None,
                                POINTER(PA_CONTEXT),
                                POINTER(PA_SERVER_INFO),
                                c_void_p)
PA_CONTEXT_READY = 4
PA_CONTEXT_FAILED = 5
PA_CONTEXT_TERMINATED = 6

pa_mainloop_new = p.pa_mainloop_new
pa_mainloop_new.restype = POINTER(PA_MAINLOOP)
pa_mainloop_new.argtypes = []

pa_mainloop_get_api = p.pa_mainloop_get_api
pa_mainloop_get_api.restype = POINTER(PA_MAINLOOP_API)
pa_mainloop_get_api.argtypes = [POINTER(PA_MAINLOOP)]

pa_mainloop_run = p.pa_mainloop_run
pa_mainloop_run.restype = c_int
pa_mainloop_run.argtypes = [POINTER(PA_MAINLOOP), POINTER(c_int)]

pa_mainloop_iterate = p.pa_mainloop_iterate
pa_mainloop_iterate.restype = c_int
pa_mainloop_iterate.argtypes = [POINTER(PA_MAINLOOP), c_int, POINTER(c_int)]

pa_mainloop_free = p.pa_mainloop_free
pa_mainloop_free.restype = c_int
pa_mainloop_free.argtypes = [POINTER(PA_MAINLOOP)]

pa_signal_init = p.pa_signal_init
pa_signal_init.restype = c_int
pa_signal_init.argtypes = [POINTER(PA_MAINLOOP_API)]

pa_signal_new = p.pa_signal_new
pa_signal_new.restype = None
pa_signal_new.argtypes = [c_int, PA_SIGNAL_CB_T, POINTER(c_int)]

pa_context_errno = p.pa_context_errno
pa_context_errno.restype = c_int
pa_context_errno.argtypes = [POINTER(PA_CONTEXT)]

pa_context_new = p.pa_context_new
pa_context_new.restype = POINTER(PA_CONTEXT)
pa_context_new.argtypes = [POINTER(PA_MAINLOOP_API), c_char_p]

pa_context_unref = p.pa_context_unref
pa_context_unref.restype = None
pa_context_unref.argtypes = [POINTER(PA_CONTEXT)]

pa_context_set_state_callback = p.pa_context_set_state_callback
pa_context_set_state_callback.restype = None
pa_context_set_state_callback.argtypes = [
    POINTER(PA_CONTEXT),
    PA_STATE_CB_T,
    c_void_p
]

pa_context_connect = p.pa_context_connect
pa_context_connect.restype = c_int
pa_context_connect.argtypes = [
    POINTER(PA_CONTEXT),
    c_char_p,
    c_int,
    POINTER(c_int)
]

pa_context_get_state = p.pa_context_get_state
pa_context_get_state.restype = c_int
pa_context_get_state.argtypes = [POINTER(PA_CONTEXT)]

pa_context_disconnect = p.pa_context_disconnect
pa_context_disconnect.restype = c_int
pa_context_disconnect.argtypes = [POINTER(PA_CONTEXT)]

pa_proplist_gets = p.pa_proplist_gets
pa_proplist_gets.restype = c_char_p
pa_proplist_gets.argtypes = [POINTER(PA_PROPLIST), c_char_p]

pa_context_get_sink_input_info_list = p.pa_context_get_sink_input_info_list
pa_context_get_sink_input_info_list.restype = POINTER(c_int)
pa_context_get_sink_input_info_list.argtypes = [
    POINTER(PA_CONTEXT),
    PA_SINK_INPUT_INFO_CB_T,
    c_void_p
]

pa_context_get_sink_info_list = p.pa_context_get_sink_info_list
pa_context_get_sink_info_list.restype = POINTER(c_int)
pa_context_get_sink_info_list.argtypes = [
    POINTER(PA_CONTEXT),
    PA_SINK_INFO_CB_T,
    c_void_p
]

pa_context_set_sink_mute_by_index = p.pa_context_set_sink_mute_by_index
pa_context_set_sink_mute_by_index.restype = POINTER(c_int)
pa_context_set_sink_mute_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_int,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_suspend_sink_by_index = p.pa_context_suspend_sink_by_index
pa_context_suspend_sink_by_index.restype = POINTER(c_int)
pa_context_suspend_sink_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_int,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_set_sink_port_by_index = p.pa_context_set_sink_port_by_index
pa_context_set_sink_port_by_index.restype = POINTER(c_int)
pa_context_set_sink_port_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_char_p,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_set_sink_input_mute = p.pa_context_set_sink_input_mute
pa_context_set_sink_input_mute.restype = POINTER(c_int)
pa_context_set_sink_input_mute.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_int,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_set_sink_volume_by_index = p.pa_context_set_sink_volume_by_index
pa_context_set_sink_volume_by_index.restype = POINTER(c_int)
pa_context_set_sink_volume_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    POINTER(PA_CVOLUME),
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_set_sink_input_volume = p.pa_context_set_sink_input_volume
pa_context_set_sink_input_volume.restype = POINTER(c_int)
pa_context_set_sink_input_volume.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    POINTER(PA_CVOLUME),
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_move_sink_input_by_index = p.pa_context_move_sink_input_by_index
pa_context_move_sink_input_by_index.restype = POINTER(c_int)
pa_context_move_sink_input_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_uint32,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_set_default_sink = p.pa_context_set_default_sink
pa_context_set_default_sink.restype = POINTER(PA_OPERATION)
pa_context_set_default_sink.argtypes = [
    POINTER(PA_CONTEXT),
    c_char_p,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_kill_sink_input = p.pa_context_kill_sink_input
pa_context_kill_sink_input.restype = POINTER(PA_OPERATION)
pa_context_kill_sink_input.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_kill_client = p.pa_context_kill_client
pa_context_kill_client.restype = POINTER(PA_OPERATION)
pa_context_kill_client.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_get_source_output_info = p.pa_context_get_source_output_info
pa_context_get_source_output_info.restype = POINTER(c_int)
pa_context_get_source_output_info.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    PA_SOURCE_OUTPUT_INFO_CB_T,
    c_void_p
]

pa_context_get_source_output_info_list = p.pa_context_get_source_output_info_list
pa_context_get_source_output_info_list.restype = POINTER(c_int)
pa_context_get_source_output_info_list.argtypes = [
    POINTER(PA_CONTEXT),
    PA_SOURCE_OUTPUT_INFO_CB_T,
    c_void_p
]

pa_context_move_source_output_by_index = p.pa_context_move_source_output_by_index
pa_context_move_source_output_by_index.restype = POINTER(c_int)
pa_context_move_source_output_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_uint32,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_set_source_output_volume = p.pa_context_set_source_output_volume
pa_context_set_source_output_volume.restype = POINTER(c_int)
pa_context_set_source_output_volume.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    POINTER(PA_CVOLUME),
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_set_source_output_mute = p.pa_context_set_source_output_mute
pa_context_set_source_output_mute.restype = POINTER(c_int)
pa_context_set_source_output_mute.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_int,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_get_source_info_by_index = p.pa_context_get_source_info_by_index
pa_context_get_source_info_by_index.restype = POINTER(c_int)
pa_context_get_source_info_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    PA_SOURCE_INFO_CB_T,
    c_void_p
]

pa_context_get_source_info_list = p.pa_context_get_source_info_list
pa_context_get_source_info_list.restype = POINTER(c_int)
pa_context_get_source_info_list.argtypes = [
    POINTER(PA_CONTEXT),
    PA_SOURCE_INFO_CB_T,
    c_void_p
]

pa_context_set_source_volume_by_index = p.pa_context_set_source_volume_by_index
pa_context_set_source_volume_by_index.restype = POINTER(c_int)
pa_context_set_source_volume_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    POINTER(PA_CVOLUME),
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_set_source_volume_by_index = p.pa_context_set_source_volume_by_index
pa_context_set_source_volume_by_index.restype = POINTER(c_int)
pa_context_set_source_volume_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    POINTER(PA_CVOLUME),
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_set_source_mute_by_index = p.pa_context_set_source_mute_by_index
pa_context_set_source_mute_by_index.restype = POINTER(c_int)
pa_context_set_source_mute_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_int,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_suspend_source_by_index = p.pa_context_suspend_source_by_index
pa_context_suspend_source_by_index.restype = POINTER(c_int)
pa_context_suspend_source_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_int,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_set_source_port_by_index = p.pa_context_set_source_port_by_index
pa_context_set_source_port_by_index.restype = POINTER(c_int)
pa_context_set_source_port_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_char_p,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_set_default_source = p.pa_context_set_default_source
pa_context_set_default_source.restype = POINTER(PA_OPERATION)
pa_context_set_default_source.argtypes = [
    POINTER(PA_CONTEXT),
    c_char_p,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_kill_source_output = p.pa_context_kill_source_output
pa_context_kill_source_output.restype = POINTER(PA_OPERATION)
pa_context_kill_source_output.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_get_client_info_list = p.pa_context_get_client_info_list
pa_context_get_client_info_list.restype = POINTER(c_int)
pa_context_get_client_info_list.argtypes = [
    POINTER(PA_CONTEXT),
    PA_CLIENT_INFO_CB_T,
    c_void_p
]

pa_context_get_card_info_by_index = p.pa_context_get_card_info_by_index
pa_context_get_card_info_by_index.restype = POINTER(PA_OPERATION)
pa_context_get_card_info_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    PA_CARD_INFO_CB_T,
    c_void_p
]

pa_context_get_card_info_list = p.pa_context_get_card_info_list
pa_context_get_card_info_list.restype = POINTER(PA_OPERATION)
pa_context_get_card_info_list.argtypes = [
    POINTER(PA_CONTEXT),
    PA_CARD_INFO_CB_T,
    c_void_p
]

pa_context_set_card_profile_by_index = p.pa_context_set_card_profile_by_index
pa_context_set_card_profile_by_index.restype = POINTER(c_int)
pa_context_set_card_profile_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_char_p,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]

pa_context_get_server_info = p.pa_context_get_server_info
pa_context_get_server_info.restype = POINTER(PA_OPERATION)
pa_context_get_server_info.argtypes = [
    POINTER(PA_CONTEXT),
    PA_SERVER_INFO_CB_T,
    c_void_p
]

# ^ bindings
#########################################################################################
# v lib


class PulsePort():

    def __init__(self, pa_port):
        self.name = pa_port.name
        self.description = pa_port.description
        self.priority = pa_port.priority

    def debug(self):
        pprint(vars(self))


class PulseServer():

    def __init__(self, pa_server):
        self.default_sink_name = pa_server.default_sink_name
        self.default_source_name = pa_server.default_source_name
        self.server_version = pa_server.server_version

    def debug(self):
        pprint(vars(self))


class PulseCardProfile():

    def __init__(self, pa_profile):
        self.name = pa_profile.name
        self.description = pa_profile.description

    def debug(self):
        pprint(vars(self))


class PulseCard():

    def __init__(self, pa_card):
        self.name = pa_card.name
        self.description = pa_proplist_gets(pa_card.proplist, b'device.description')
        self.index = pa_card.index
        self.driver = pa_card.driver
        self.owner_module = pa_card.owner_module
        self.n_profiles = pa_card.n_profiles
        self.profiles = [PulseCardProfile(pa_card.profiles[n]) for n in range(self.n_profiles)]
        self.active_profile = PulseCardProfile(pa_card.active_profile[0])
        self.volume = type('volume', (object,), {'channels': 1, 'values': [0, 0]})

    def debug(self):
        pprint(vars(self))

    def __str__(self):
        return "Card-ID: {}, Name: {}".format(self.index, self.name.decode())


class PulseClient():

    def __init__(self, pa_client):
        self.index = getattr(pa_client, "index", 0)
        self.name = getattr(pa_client, "name", pa_client)
        self.driver = getattr(pa_client, "driver", "default driver")
        self.owner_module = getattr(pa_client, "owner_module", -1)

    def debug(self):
        pprint(vars(self))

    def __str__(self):
        return "Client-name: {}".format(self.name.decode())


class Pulse():

    def __init__(self, client_name='libpulse', server_name=None):

        self.ret = None
        self.error = None
        self.operation = None
        self.connected = True
        self.action_done = False
        self.data = []
        self.client_name = client_name.encode()
        self.server_name = server_name

        self.pa_signal_cb = PA_SIGNAL_CB_T(self.signal_cb)
        self.pa_state_cb = PA_STATE_CB_T(self.state_cb)

        self.mainloop = pa_mainloop_new()
        self.mainloop_api = pa_mainloop_get_api(self.mainloop)

        assert pa_signal_init(self.mainloop_api) == 0, "pa_signal_init failed"

        pa_signal_new(2, self.pa_signal_cb, None)
        pa_signal_new(15, self.pa_signal_cb, None)

        self.context = pa_context_new(self.mainloop_api, self.client_name)
        pa_context_set_state_callback(self.context, self.pa_state_cb, None)

        if pa_context_connect(self.context, self.server_name, 0, None) < 0:
            self.disconnect()
            sys.exit("Failed to connect to pulseaudio daemon: Connection refused")
        self.iterate()

    def reconnect(self):
        self.connected = False
        while not self.connected:
            self.error = None
            self.disconnect()

            self.mainloop = pa_mainloop_new()
            self.mainloop_api = pa_mainloop_get_api(self.mainloop)

            self.context = pa_context_new(self.mainloop_api, self.client_name)
            pa_context_set_state_callback(self.context, self.pa_state_cb, None)

            try:
                if pa_context_connect(self.context, self.server_name, 0, None) >= 0:
                    self.iterate()
                    self.connected = True
            except:
                pass
            sleep(0.5)

    def unmute_stream(self, obj):
        if type(obj) is PulseSinkInfo:
            self.sink_mute(obj.index, 0)
        elif type(obj) is PulseSinkInputInfo:
            self.sink_input_mute(obj.index, 0)
        elif type(obj) is PulseSourceInfo:
            self.source_mute(obj.index, 0)
        elif type(obj) is PulseSourceOutputInfo:
            self.source_output_mute(obj.index, 0)
        obj.mute = 0

    def mute_stream(self, obj):
        if type(obj) is PulseSinkInfo:
            self.sink_mute(obj.index, 1)
        elif type(obj) is PulseSinkInputInfo:
            self.sink_input_mute(obj.index, 1)
        elif type(obj) is PulseSourceInfo:
            self.source_mute(obj.index, 1)
        elif type(obj) is PulseSourceOutputInfo:
            self.source_output_mute(obj.index, 1)
        obj.mute = 1

    def set_volume(self, obj, volume):
        if type(obj) is PulseSinkInfo:
            self.set_sink_volume(obj.index, volume)
        elif type(obj) is PulseSinkInputInfo:
            self.set_sink_input_volume(obj.index, volume)
        elif type(obj) is PulseSourceInfo:
            self.set_source_volume(obj.index, volume)
        elif type(obj) is PulseSourceOutputInfo:
            self.set_source_output_volume(obj.index, volume)
        obj.volume = volume

    def change_volume_mono(self, obj, inc):
        obj.volume.values = [v + inc for v in obj.volume.values]
        self.set_volume(obj, obj.volume)

    def get_volume_mono(self, obj):
        return int(sum(obj.volume.values) / len(obj.volume.values))

    def fill_clients(self):
        if not self.data:
            return
        data, self.data = self.data, []
        clist = self.client_list()
        for d in data:
            for c in clist:
                if c.index == d.client_id:
                    d.client = c
                    break
        return data

    def signal_cb(self, api, e, sig, userdata):
        if sig == 2 or sig == 15:
            self.disconnect()
        return 0

    def state_cb(self, c, b):
        state = pa_context_get_state(c)
        if state == PA_CONTEXT_READY:
            self.complete_action()
        elif state in (PA_CONTEXT_FAILED, PA_CONTEXT_TERMINATED):
            self.error = RuntimeError("Failed to complete action: {}, {}".format(state, pa_context_errno(c)))
            self.complete_action()
        return 0

    def _action_cb(func):
        def wrapper(self, c, info, eof, userdata):
            if eof:
                self.complete_action()
                return 0
            func(self, c, info, eof, userdata)
            return 0
        return wrapper

    @_action_cb
    def card_cb(self, c, card_info, eof, userdata):
        self.data.append(PulseCard(card_info[0]))

    @_action_cb
    def client_cb(self, c, client_info, eof, userdata):
        self.data.append(PulseClient(client_info[0]))

    @_action_cb
    def sink_input_cb(self, c, sink_input_info, eof, userdata):
        self.data.append(PulseSinkInputInfo(sink_input_info[0]))

    @_action_cb
    def sink_cb(self, c, sink_info, eof, userdata):
        self.data.append(PulseSinkInfo(sink_info[0]))

    @_action_cb
    def source_output_cb(self, c, source_output_info, eof, userdata):
        self.data.append(PulseSourceOutputInfo(source_output_info[0]))

    @_action_cb
    def source_cb(self, c, source_info, eof, userdata):
        self.data.append(PulseSourceInfo(source_info[0]))

    def server_cb(self, c, server_info, eof):
        self.data.append(PulseServer(server_info[0]))
        self.complete_action()

    def context_success(self, c, success, userdata):
        self.complete_action()
        return 0

    def complete_action(self):
        self.action_done = True

    def start_action(self):
        self.action_done = False

    def disconnect(self):
        pa_context_disconnect(self.context)
        pa_context_unref(self.context)
        pa_mainloop_free(self.mainloop)

    def sink_input_list(self):
        CB = PA_SINK_INPUT_INFO_CB_T(self.sink_input_cb)
        self.operation = pa_context_get_sink_input_info_list(self.context, CB, None)
        self.iterate()
        data, self.data = self.fill_clients(), []
        return data or []

    def sink_list(self):
        CB = PA_SINK_INFO_CB_T(self.sink_cb)
        self.operation = pa_context_get_sink_info_list(self.context, CB, None)
        self.iterate()
        data, self.data = self.data, []
        return data or []

    def source_output_list(self):
        CB = PA_SOURCE_OUTPUT_INFO_CB_T(self.source_output_cb)
        self.operation = pa_context_get_source_output_info_list(self.context, CB, None)
        self.iterate()
        data, self.data = self.fill_clients(), []
        return data or []

    def source_list(self):
        CB = PA_SOURCE_INFO_CB_T(self.source_cb)
        self.operation = pa_context_get_source_info_list(self.context, CB, None)
        self.iterate()
        data, self.data = self.data, []
        return data or []

    def get_server_info(self):
        CB = PA_SERVER_INFO_CB_T(self.server_cb)
        self.operation = pa_context_get_server_info(self.context, CB, None)
        self.iterate()
        data, self.data = self.data, []
        return data[0] or None

    def card_list(self):
        CB = PA_CARD_INFO_CB_T(self.card_cb)
        self.operation = pa_context_get_card_info_list(self.context, CB, None)
        self.iterate()
        data, self.data = self.data, []
        return data or []

    def client_list(self):
        CB = PA_CLIENT_INFO_CB_T(self.client_cb)
        self.operation = pa_context_get_client_info_list(self.context, CB, None)
        self.iterate()
        data, self.data = self.data, []
        return data or []

    def sink_input_mute(self, index, mute):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_sink_input_mute(self.context, index, mute, CONTEXT, None)
        self.iterate()

    def sink_input_move(self, index, s_index):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_move_sink_input_by_index(self.context, index, s_index, CONTEXT, None)
        self.iterate()

    def sink_mute(self, index, mute):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_sink_mute_by_index(self.context, index, mute, CONTEXT, None)
        self.iterate()

    def set_sink_input_volume(self, index, vol):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_sink_input_volume(self.context, index, vol.to_c(), CONTEXT, None)
        self.iterate()

    def set_sink_volume(self, index, vol):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_sink_volume_by_index(self.context, index, vol.to_c(), CONTEXT, None)
        self.iterate()

    def sink_suspend(self, index, suspend):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_suspend_sink_by_index(self.context, index, suspend, CONTEXT, None)
        self.iterate()

    def set_default_sink(self, name):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_default_sink(self.context, name, CONTEXT, None)
        self.iterate()

    def kill_sink(self, index):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_kill_sink_input(self.context, index, CONTEXT, None)
        self.iterate()

    def kill_client(self, index):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_kill_client(self.context, index, CONTEXT, None)
        self.iterate()

    def set_sink_port(self, index, port):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_sink_port_by_index(self.context, index, port, CONTEXT, None)
        self.iterate()

    def set_source_output_volume(self, index, vol):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_source_output_volume(self.context, index, vol.to_c(), CONTEXT, None)
        self.iterate()

    def set_source_volume(self, index, vol):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_source_volume_by_index(self.context, index, vol.to_c(), CONTEXT, None)
        self.iterate()

    def source_suspend(self, index, suspend):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_suspend_source_by_index(self.context, index, suspend, CONTEXT, None)
        self.iterate()

    def set_default_source(self, name):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_default_source(self.context, name, CONTEXT, None)
        self.iterate()

    def kill_source(self, index):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_kill_source_output(self.context, index, CONTEXT, None)
        self.iterate()

    def set_source_port(self, index, port):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_source_port_by_index(self.context, index, port, CONTEXT, None)
        self.iterate()

    def source_output_mute(self, index, mute):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_source_output_mute(self.context, index, mute, CONTEXT, None)
        self.iterate()

    def source_mute(self, index, mute):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_source_mute_by_index(self.context, index, mute, CONTEXT, None)
        self.iterate()

    def source_output_move(self, index, s_index):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_move_source_output_by_index(self.context, index, s_index, CONTEXT, None)
        self.iterate()

    def set_card_profile(self, index, p_index):
        CONTEXT = PA_CONTEXT_SUCCESS_CB_T(self.context_success)
        self.operation = pa_context_set_card_profile_by_index(self.context, index, p_index, CONTEXT, None)
        self.iterate()

    def run(self):
        self.ret = pointer(c_int(0))
        pa_mainloop_run(self.mainloop, self.ret)

    def iterate(self, times=1, start=True):
        if self.error:
            raise self.error
        start and self.start_action()
        self.ret = pointer(c_int())
        pa_mainloop_iterate(self.mainloop, times, self.ret)
        while not self.action_done:
            pa_mainloop_iterate(self.mainloop, times, self.ret)


class PulseSink():

    def __init__(self, sink_info):
        self.index = sink_info.index
        self.name = sink_info.name
        self.mute = sink_info.mute
        self.volume = PulseVolume(sink_info.volume)

    def debug(self):
        pprint(vars(self))


class PulseSinkInfo(PulseSink):

    def __init__(self, pa_sink_info):
        PulseSink.__init__(self, pa_sink_info)
        self.description = pa_sink_info.description
        self.owner_module = pa_sink_info.owner_module
        self.driver = pa_sink_info.driver
        self.monitor_source = pa_sink_info.monitor_source
        self.monitor_source_name = pa_sink_info.monitor_source_name
        self.n_ports = pa_sink_info.n_ports
        self.ports = [PulsePort(pa_sink_info.ports[i].contents) for i in range(self.n_ports)]
        self.active_port = None
        if self.n_ports:
            self.active_port = PulsePort(pa_sink_info.active_port.contents)

    def __str__(self):
        return "ID: {}, Name: {}, Mute: {}, {}".format(
            self.index, self.description.decode(), self.mute, self.volume)


class PulseSinkInputInfo(PulseSink):

    def __init__(self, pa_sink_input_info):
        PulseSink.__init__(self, pa_sink_input_info)
        self.owner_module = pa_sink_input_info.owner_module
        self.client = PulseClient(pa_sink_input_info.name)
        self.client_id = pa_sink_input_info.client
        self.sink = self.owner = pa_sink_input_info.sink
        self.driver = pa_sink_input_info.driver
        self.media_name = pa_proplist_gets(pa_sink_input_info.proplist, b'media.name')

    def __str__(self):
        if self.client:
            return "ID: {}, Name: {}, Mute: {}, {}".format(
                self.index, self.client.name.decode(), self.mute, self.volume)
        return "ID: {}, Name: {}, Mute: {}".format(self.index, self.name.decode(), self.mute)


class PulseSource():

    def __init__(self, source_info):
        self.index = source_info.index
        self.name = source_info.name
        self.mute = source_info.mute
        self.volume = PulseVolume(source_info.volume)

    def debug(self):
        pprint(vars(self))


class PulseSourceInfo(PulseSource):

    def __init__(self, pa_source_info):
        PulseSource.__init__(self, pa_source_info)
        self.description = pa_source_info.description
        self.owner_module = pa_source_info.owner_module
        self.monitor_of_sink = pa_source_info.monitor_of_sink
        self.monitor_of_sink_name = pa_source_info.monitor_of_sink_name
        self.driver = pa_source_info.driver
        self.n_ports = pa_source_info.n_ports
        self.ports = [PulsePort(pa_source_info.ports[i].contents) for i in range(self.n_ports)]
        self.active_port = None
        if self.n_ports:
            self.active_port = PulsePort(pa_source_info.active_port.contents)

    def __str__(self):
        return "ID: {}, Name: {}, Mute: {}, {}".format(
            self.index, self.description.decode(), self.mute, self.volume)


class PulseSourceOutputInfo(PulseSource):

    def __init__(self, pa_source_output_info):
        PulseSource.__init__(self, pa_source_output_info)
        self.owner_module = pa_source_output_info.owner_module
        self.client = PulseClient(pa_source_output_info.name)
        self.client_id = pa_source_output_info.client
        self.source = self.owner = pa_source_output_info.source
        self.driver = pa_source_output_info.driver

    def __str__(self):
        if self.client:
            return "ID: {}, Name: {}, Mute: {}, {}".format(
                self.index, self.client.name.decode(), self.mute, self.volume)
        return "ID: {}, Name: {}, Mute: {}".format(self.index, self.name.decode(), self.mute)


class PulseVolume():

    def __init__(self, cvolume):
        self.channels = cvolume.channels
        self.values = [(round(x * 100 / PA_VOLUME_NORM)) for x in cvolume.values[:self.channels]]

    def to_c(self):
        self.values = list(map(lambda x: max(min(x, 150), 0), self.values))
        cvolume = PA_CVOLUME()
        cvolume.channels = self.channels
        for x in range(self.channels):
            cvolume.values[x] = round((self.values[x] * PA_VOLUME_NORM) / 100)
        return cvolume

    def debug(self):
        pprint(vars(self))

    def __str__(self):
        return "Channels: {}, Volumes: {}".format(self.channels, [str(x) + "%" for x in self.values])

# ^ lib
#########################################################################################
# v main


class Bar():
    # should be in correct order
    LEFT, RIGHT, RLEFT, RRIGHT, CENTER, SUB, SLEFT, SRIGHT, NONE = range(9)

    def __init__(self, pa):
        if type(pa) is str:
            self.name = pa
            return
        if type(pa) in (PulseSinkInfo, PulseSourceInfo, PulseCard):
            self.fullname = pa.description.decode()
        else:
            self.fullname = pa.client.name.decode()
        self.name = re.sub('^ALSA plug-in \[|\]$', '', self.fullname.replace('|', ' '))
        self.index = pa.index
        self.owner = -1
        self.stream_index = -1
        self.poll_data(pa, 0, 0)
        self.maxsize = 150
        self.locked = True

    def poll_data(self, pa, owned, stream_index):
        self.channels = pa.volume.channels
        self.muted = getattr(pa, 'mute', False)
        self.owned = owned
        self.stream_index = stream_index
        self.volume = pa.volume.values
        try:
            self.media_name = ': {}'.format(pa.media_name.decode().replace('|', ' '))
        except:
            self.media_name = ''
        if type(pa) in (PulseSinkInputInfo, PulseSourceOutputInfo):
            self.owner = pa.owner
        self.pa = pa

    def mute_toggle(self):
        pulse.unmute_stream(self.pa) if self.muted else pulse.mute_stream(self.pa)

    def lock_toggle(self):
        self.locked = not self.locked

    def set(self, n, side):
        vol = self.pa.volume
        if self.locked:
            for i, _ in enumerate(vol.values):
                vol.values[i] = n
        else:
            vol.values[side] = n
        pulse.set_volume(self.pa, vol)

    def move(self, n, side):
        vol = self.pa.volume
        if self.locked:
            for i, _ in enumerate(vol.values):
                vol.values[i] += n
        else:
            vol.values[side] += n
        pulse.set_volume(self.pa, vol)


class Screen():
    DOWN = 1
    UP = -1
    SCROLL_UP = [getattr(curses, i, 0) for i in ['BUTTON4_PRESSED', 'BUTTON3_TRIPLE_CLICKED']]
    SCROLL_DOWN = [getattr(curses, i, 0) for i in ['BUTTON5_PRESSED', 'A_LOW', 'A_BOLD', 'BUTTON4_DOUBLE_CLICKED']]
    KEY_MOUSE = getattr(curses, 'KEY_MOUSE', 0)
    SPACE_KEY = 32
    ESC_KEY = 27
    MODE = {0: 1, 1: 0, 2: 0}
    DIGITS = list(map(ord, map(str, range(10))))
    SIDES = {Bar.LEFT: 'Left', Bar.RIGHT: 'Right', Bar.RLEFT: 'Rear Left',
             Bar.RRIGHT: 'Rear Right', Bar.CENTER: 'Center', Bar.SUB: 'Subwoofer',
             Bar.SLEFT: 'Side left', Bar.SRIGHT: 'Side right'}
    SEQ_TO_KEY = {
        (91, 49, 59, 50, 67): curses.KEY_SRIGHT,
        (91, 49, 59, 50, 68): curses.KEY_SLEFT,
        (79, 80, -1, -1, -1): curses.KEY_F1,
        (79, 81, -1, -1, -1): curses.KEY_F2,
        (79, 82, -1, -1, -1): curses.KEY_F3,
    }

    def __init__(self, color=3, mouse=True):
        environ['ESCDELAY'] = '25'
        self.screen = curses.initscr()
        self.screen.timeout(900)
        self.screen.scrollok(1)
        if mouse:
            try:
                curses.mousemask(curses.ALL_MOUSE_EVENTS |
                                 curses.BUTTON1_CLICKED |
                                 self.KEY_MOUSE |
                                 functools.reduce(operator.or_, list(self.SCROLL_UP)) |
                                 functools.reduce(operator.or_, list(self.SCROLL_DOWN)))
            except:
                self.KEY_MOUSE = 0
        else:
            self.KEY_MOUSE = 0
        try:
            curses.curs_set(0)
        except:  # terminal doesn't support visibility requests
            pass
        self.screen.border(0)
        self.index = 0
        self.top_line_num = 0
        self.focus_line_num = 0
        self.lines, self.cols = curses.LINES - 1, curses.COLS - 1
        self.info, self.menu = str, str
        self.menu_titles = ['F1 Output', 'F2 Input', 'F3 Cards']
        self.data = []
        self.modes = [[[], 0, 0] for i in range(6)]
        self.active_mode = 0
        self.old_mode = 0
        self.change_mode_allowed = True
        self.n_lines, self.n_lines_info = 0, 0
        self.color_mode = color
        if color in (1, 2) and curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            curses.init_pair(2, curses.COLOR_YELLOW, -1)
            curses.init_pair(3, curses.COLOR_RED, -1)
            self.green = curses.color_pair(1)
            self.yellow = curses.color_pair(2)
            self.red = curses.color_pair(3)
            n = 7 if curses.COLORS < 256 else 67
            curses.init_pair(n, n - 1, -1)
            self.muted_color = curses.color_pair(n)
            if curses.COLORS < 256:
                self.gray_gradient = [curses.A_NORMAL] * 3
            else:
                try:
                    curses.init_pair(240, 240, -1)
                    curses.init_pair(243, 243, -1)
                    curses.init_pair(246, 246, -1)
                    self.gray_gradient = [
                        curses.color_pair(240),
                        curses.color_pair(243),
                        curses.color_pair(246),
                    ]
                except:
                    self.gray_gradient = [curses.A_NORMAL] * 3
        else:
            # if term has colors start them regardless of --color to avoid weird backgrounds
            # on some terminals
            if curses.has_colors():
                curses.start_color()
                curses.use_default_colors()
            self.gray_gradient = [curses.A_NORMAL] * 3
            self.green = self.yellow = self.red = self.muted_color = curses.A_NORMAL
        self.gradient = [self.green, self.yellow, self.red]
        self.submenu_data = []
        self.submenu_width = 30
        self.submenu_show = False
        self.submenu = curses.newwin(curses.LINES, 0, 0, 0)
        self.helpwin_show = False
        self.helpwin = curses.newwin(13, 62, 0, 0)
        try:
            self.helpwin.mvwin((curses.LINES // 2) - 6, (curses.COLS // 2) - 31)
        except:
            pass
        self.selected = None
        self.action = None

    def display_line(self, index, line, mod=curses.A_NORMAL):
        shift = 0
        for s in line.split('\n'):
            p = s.rsplit('|')
            p1 = ''.join(p[:-1])
            try:
                self.screen.addstr(index, shift, p1, int(p[-1]) | mod)
            except:
                self.screen.addstr(min(curses.LINES - 1, index), min(curses.COLS - 1, shift), p1, int(p[-1]) | mod)
            shift += len(p1)

    def change_mode(self, mode):
        if not self.change_mode_allowed:
            return
        self.modes[self.active_mode][1] = self.focus_line_num
        self.modes[self.active_mode][2] = self.top_line_num
        self.old_mode = self.active_mode
        self.MODE = self.MODE.fromkeys(self.MODE, 0)
        self.MODE[mode] = 1
        self.focus_line_num = self.modes[mode][1]
        self.top_line_num = self.modes[mode][2]
        self.active_mode = mode
        self.get_data()

    def next_mode(self):
        for mode, active in self.MODE.items():
            if active == 1:
                self.change_mode((1 + mode) % 3)
                return

    def update_menu(self):
        if self.change_mode_allowed:
            self.menu = '{}|{}\n  {}|{}\n  {}|{}\n {:>{}}|{}'.format(
                self.menu_titles[0], curses.A_BOLD if self.MODE[0] else curses.A_DIM,
                self.menu_titles[1], curses.A_BOLD if self.MODE[1] else curses.A_DIM,
                self.menu_titles[2], curses.A_BOLD if self.MODE[2] else curses.A_DIM,
                "? - help", self.cols - 30, curses.A_DIM)
        else:
            select = 'output' if type(self.selected[0].pa) is PulseSinkInputInfo else 'input'
            self.menu = "Select new {} device:|{}".format(select, curses.A_NORMAL)

    def update_info(self):
        focus = self.focus_line_num + self.top_line_num + 1
        try:
            bar, side = self.data[focus - 1][0], self.data[focus - 1][1]
        except IndexError:
            self.focus_line_num, self.top_line_num = 0, 0
            [self.scroll(self.UP) for _ in range(len(self.data))]
            return
        if side is Bar.NONE:
            self.info = str
            return
        side = 'All' if bar.locked else 'Mono' if bar.channels == 1 else self.SIDES[side]
        pos = int(focus * 100 / self.n_lines)
        name = '{}: {}'.format(bar.fullname, side)
        if len(name) > self.cols - 14:
            name = '{}: {}'.format(bar.fullname[:self.cols - (18 + len(side))], side)
        self.info = '{}|{}\n{}|{}\n{}|{}\n'.format(
            "L ", self.red if bar.locked else curses.A_DIM,
            "M  ", self.red if bar.muted else curses.A_DIM, name, curses.A_NORMAL)
        self.info += '{:>{}}%|{}'.format(pos, self.cols - len(name) - 6, curses.A_BOLD)

    def check_resize(self):
        if curses.is_term_resized(curses.LINES, curses.COLS):
            self.screen.erase()
            y, x = self.screen.getmaxyx()
            curses.resizeterm(y, x)
            self.submenu.resize(curses.LINES, self.submenu_width + 1)
            if self.submenu_show:
                self.submenu_show = False
                self.focus_line_num = self.modes[5][1]
                self.top_line_num = self.modes[5][2]
            self.helpwin.resize(13, 62)
            self.helpwin.mvwin((curses.LINES // 2) - 6, (curses.COLS // 2) - 31)
            self.helpwin_show = False
            self.screen.refresh()
        self.lines = curses.LINES - 2
        self.cols = curses.COLS - 1

    def run_mouse(self):
        try:
            _, x, y, _, c = curses.getmouse()
            if c & curses.BUTTON1_CLICKED:
                if y > 0:
                    top, bottom = self.top_line_num, len(self.data[self.top_line_num:self.top_line_num + self.lines]) - 1
                    if y - 1 <= bottom:
                        self.focus_line_num = max(top, min(bottom, y - 1))
                else:
                    f1 = len(self.menu_titles[0]) + 1 # 1 is 'spacing' after the title
                    f2 = f1 + len(self.menu_titles[1]) + 2
                    f3 = f2 + len(self.menu_titles[2]) + 3
                    if x in range(0, f1):
                        self.change_mode(0)
                    elif x in range(f1, f2):
                        self.change_mode(1)
                    elif x in range(f2, f3):
                        self.change_mode(2)
            return c
        except curses.error:
            return None

    def sigint(self):
        # if ^C pressed while doing pulse.reconnect wrapper.restore won't be called
        # so have to restore it manually here
        self.screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        sys.exit(0)

    def run(self, scr):
        signal.signal(signal.SIGINT, lambda signal, frame: self.sigint())
        from ctypes import _reset_cache as reset_cache
        while True:
            try:
                self.check_resize()
                if not self.submenu_show:
                    try:
                        self.get_data()
                    except RuntimeError:
                        self.focus_line_num = 0
                        self.data = [(Bar('PA - Connection refused.\nTrying to reconnect.'), Bar.NONE, 0)]
                        self.display()
                        pulse.reconnect()
                        continue
                    self.update_menu()
                    self.update_info()
                    self.display()
                    if self.helpwin_show:
                        self.display_helpwin()
                        self.run_helpwin()
                        continue
                elif self.change_mode_allowed:
                    self.display_submenu()
                    self.run_submenu()
                    continue
            except (curses.error, IndexError, ValueError) as e:
                self.screen.erase()
                self.screen.addstr("Terminal *might* be too small {}:{}\n".format(curses.LINES, curses.COLS))
                self.screen.addstr("{}\n{}\n".format(str(self.MODE), str(e)))
                self.screen.addstr(str(traceback.extract_tb(e.__traceback__)))

            focus = self.top_line_num + self.focus_line_num
            bar, side = self.data[focus][0], self.data[focus][1]

            c = self.screen.getch()

            if c == -1:
                continue
            elif c == self.KEY_MOUSE:
                c = self.run_mouse() or c
            elif c == 27:
                # translating key-sequences to keys recognized by curses
                l = []
                self.screen.timeout(0)
                for i in range(5):
                    l.append(self.screen.getch())
                self.screen.timeout(900)
                c = self.SEQ_TO_KEY.get(tuple(l), 27)

            if c == curses.KEY_F1:
                self.change_mode(0)
            elif c == curses.KEY_F2:
                self.change_mode(1)
            elif c == curses.KEY_F3:
                self.change_mode(2)
            elif c == ord('?'):
                self.helpwin_show = True
            elif c == ord('\n'):
                if not self.submenu_show and self.change_mode_allowed and side != Bar.NONE:
                    self.selected = self.data[focus]
                    if type(self.selected[0].pa) in (PulseSinkInfo, PulseSourceInfo):
                        self.submenu_data = ['Suspend', 'Resume', 'Set as default']
                        if self.selected[0].pa.n_ports:
                            self.submenu_data.append('Set port')
                    elif type(self.selected[0].pa) is PulseCard:
                        self.submenu_data = [p.description.decode() for p in self.selected[0].pa.profiles]
                    else:
                        self.submenu_data = ['Move', 'Kill']
                    self.submenu_show = True
                    self.modes[5][0] = 0
                    self.modes[5][1] = self.focus_line_num
                    self.modes[5][2] = self.top_line_num
                    self.focus_line_num = self.top_line_num = 0
                    self.n_lines = len(self.submenu_data)
                    self.submenu_width = min(self.cols - 2, max(30, len(max(self.submenu_data, key=len)) + 5))
                    self.submenu_data = [s[:self.submenu_width - 4] for s in self.submenu_data]
                elif not self.change_mode_allowed:
                    self.submenu_show = False
                    self.change_mode_allowed = True
                    if self.action == 'Move':
                        if type(self.selected[0].pa) is PulseSinkInputInfo:
                            pulse.sink_input_move(self.selected[0].index, self.data[focus][0].pa.index)
                        elif type(self.selected[0].pa) is PulseSourceOutputInfo:
                            pulse.source_output_move(self.selected[0].index, self.data[focus][0].pa.index)
                        self.change_mode(self.old_mode)
                        self.focus_line_num = self.modes[5][1]
                        self.top_line_num = self.modes[5][2]
                    else:
                        self.change_mode(self.old_mode)
            elif c == ord('\t'):
                self.next_mode()
            elif c == ord('q') or c == self.ESC_KEY:
                if not self.change_mode_allowed:
                    self.submenu_show = False
                    self.change_mode_allowed = True
                    self.change_mode(self.old_mode)
                    self.focus_line_num = self.modes[5][1]
                    self.top_line_num = self.modes[5][2]
                elif self.helpwin_show:
                    self.helpwin_show = False
                else:
                    sys.exit()

            if side is Bar.NONE:
                continue

            if c == curses.KEY_UP or c == ord('k'):
                if bar.locked:
                    if self.data[focus][1] == 0:
                        n = 1
                    else:
                        n = self.data[focus][1] + 1
                    [self.scroll(self.UP) for _ in range(n)]
                else:
                    self.scroll(self.UP)
                if not self.data[self.top_line_num + self.focus_line_num][0]:
                    self.scroll(self.UP)
            elif c == curses.KEY_DOWN or c == ord('j'):
                if bar.locked:
                    if self.data[focus][1] == self.data[focus][3] - 1:
                        n = 1
                    else:
                        n = ((self.data[focus][3] - 1) - self.data[focus][1]) + 1
                    [self.scroll(self.DOWN) for _ in range(n)]
                else:
                    self.scroll(self.DOWN)
                if not self.data[self.top_line_num + self.focus_line_num][0]:
                    self.scroll(self.DOWN)

            elif c == ord('m'):
                bar.mute_toggle()
            elif c == self.SPACE_KEY:
                bar.lock_toggle()
            elif c == curses.KEY_LEFT or c == ord('h') or any([c & i for i in self.SCROLL_DOWN]):
                bar.move(-1, side)
            elif c == curses.KEY_RIGHT or c == ord('l') or any([c & i for i in self.SCROLL_UP]):
                bar.move(1, side)
            elif c == curses.KEY_SLEFT or c == ord('H'):
                bar.move(-10, side)
            elif c == curses.KEY_SRIGHT or c == ord('L'):
                bar.move(10, side)
            elif c in self.DIGITS:
                percent = int(chr(c)) * 10
                bar.set(100 if percent == 0 else percent, side)

    def run_submenu(self):
        c = self.screen.getch()
        if c == ord('q') or c == self.ESC_KEY:
            self.submenu_show = False
            self.focus_line_num = self.modes[5][1]
            self.top_line_num = self.modes[5][2]
        elif c == curses.KEY_UP or c == ord('k'):
            self.scroll(self.UP)
        elif c == curses.KEY_DOWN or c == ord('j'):
            self.scroll(self.DOWN)
        elif c == ord('\n'):
            focus = self.focus_line_num + self.top_line_num
            self.action = self.submenu_data[focus]
            if self.action == 'Move':
                if self.active_mode == 0:
                    self.change_mode(3)
                elif self.active_mode == 1:
                    self.change_mode(4)
                self.change_mode_allowed = self.submenu_show = False
                return
            elif self.action == 'Kill':
                try:
                    pulse.kill_client(self.selected[0].pa.client.index)
                except:
                    if type(self.selected[0].pa) is PulseSinkInputInfo:
                        pulse.kill_sink(self.selected[2])
                    else:
                        pulse.kill_source(self.selected[2])
            elif self.action == 'Suspend':
                if type(self.selected[0].pa) is PulseSinkInfo:
                    pulse.sink_suspend(self.selected[2], 1)
                else:
                    pulse.source_suspend(self.selected[2], 1)
            elif self.action == 'Resume':
                if type(self.selected[0].pa) is PulseSinkInfo:
                    pulse.sink_suspend(self.selected[2], 0)
                else:
                    pulse.source_suspend(self.selected[2], 0)
            elif self.action == 'Set as default':
                if type(self.selected[0].pa) is PulseSinkInfo:
                    pulse.set_default_sink(self.selected[0].pa.name)
                else:
                    pulse.set_default_source(self.selected[0].pa.name)
            elif self.action == 'Set port':
                self.submenu_data = []
                for i in self.selected[0].pa.ports:
                    s = i.description.decode().strip('|')
                    if len(s) > 26:
                        s = s[:23] + '..'
                    self.submenu_data.append(s)
                    if self.selected[0].pa.active_port.name == i.name:
                        self.submenu_data[-1] = " {}|{}".format(self.submenu_data[-1], self.red)
                self.focus_line_num = self.top_line_num = 0
                self.n_lines = len(self.submenu_data)
                return
            else:
                index = self.selected[0].pa.index
                if type(self.selected[0].pa) is PulseSinkInfo:
                    pulse.set_sink_port(index, self.selected[0].pa.ports[focus].name)
                elif type(self.selected[0].pa) is PulseSourceInfo:
                    pulse.set_source_port(index, self.selected[0].pa.ports[focus].name)
                elif type(self.selected[0].pa) is PulseCard:
                    pulse.set_card_profile(index, self.selected[0].pa.profiles[focus].name)
            self.change_mode_allowed = True
            self.submenu_show = False
            self.focus_line_num = self.modes[5][1]
            self.top_line_num = self.modes[5][2]

    def build(self, to, devices, streams):
        tmp = []
        index = 0
        for device in devices:
            index += device.volume.channels
            stream_index = device.volume.channels
            tmp.append([device, device.volume.channels, index, stream_index])
            device_index = len(tmp) - 1
            for stream in streams:
                if stream.owner == device.index:
                    index += stream.volume.channels
                    stream_index += stream.volume.channels
                    tmp.append([stream, -1, index, stream_index])
                    tmp[device_index][1] += stream.volume.channels
            tmp[-1][1] = tmp[device_index][1]
        for s in tmp:
            found = False
            for i, data in enumerate(to):
                if s[0].index == data[2] and type(s[0]) == type(data[0].pa):
                    found = True
                    data[0].poll_data(s[0], s[1], s[3])
                    y = s[2] - (data[3] - data[1])
                    to[i], to[y] = to[y], to[i]
            if not found:
                bar = Bar(s[0])
                bar.owned = s[1]
                bar.stream_index = s[3]
                for c in range(s[0].volume.channels):
                    to.append((bar, c, s[0].index, s[0].volume.channels))
        for i in reversed(range(len(to))):
            data = to[i]
            for s in tmp:
                if s[0].index == data[2] and type(s[0]) == type(data[0].pa):
                    y = s[2] - (data[3] - data[1])
                    to[i], to[y] = to[y], to[i]
                    break
            else:
                del to[i]
                if self.focus_line_num + self.top_line_num >= i:
                    self.scroll(self.UP)
        return to

    def add_spacers(self, f):
        tmp = []
        l = len(f)
        for i, s in enumerate(f):
            tmp.append(s)
            if s[0].stream_index == s[0].owned and s[1] == s[0].channels - 1 and i != l - 1:
                tmp.append((None, -1, 0, 0))
        return tmp

    def get_data(self):
        if self.MODE[0]:
            self.data = self.build(self.modes[0][0], pulse.sink_list(), pulse.sink_input_list())
            self.data = self.add_spacers(self.data)
        elif self.MODE[1]:
            self.data = self.build(self.modes[1][0], pulse.source_list(), pulse.source_output_list())
            self.data = self.add_spacers(self.data)
        elif self.MODE[2]:
            self.data = self.build(self.modes[2][0], pulse.card_list(), [])
        elif type(self.selected[0].pa) is PulseSinkInputInfo:
            self.data = self.build(self.modes[3][0], pulse.sink_list(), [])
        elif type(self.selected[0].pa) is PulseSourceOutputInfo:
            self.data = self.build(self.modes[4][0], pulse.source_list(), [])
        self.server = pulse.get_server_info()
        self.n_lines = len(self.data)
        if not self.n_lines:
            self.focus_line_num = 0
            self.data.append((Bar('no data'), Bar.NONE, 0))
        if not self.data[self.top_line_num + self.focus_line_num][0]:
            self.scroll(self.UP)

    def display(self):
        self.screen.erase()
        top = self.top_line_num
        bottom = self.top_line_num + self.lines
        self.display_line(0, self.menu)
        for index, line in enumerate(self.data[top:bottom]):
            bar, bartype = line[0], line[1]
            if not bar:
                self.screen.addstr(index + 1, 0, '', curses.A_DIM)
                continue
            elif bartype is Bar.NONE:
                for i, name in enumerate(bar.name.split('\n')):
                    self.screen.addstr((self.lines // 2) + i, (self.cols // 2) - len(name) // 2, name, curses.A_DIM)
                break

            # hightlight lines from same bar
            same, found = [], False
            for i, v in enumerate(self.data[top:bottom]):
                if v[0] is self.data[self.top_line_num + self.focus_line_num][0]:
                    same.append(v[0])

            tree = ' '
            if bar.owner == -1 and bar.owned > bar.channels:
                tree = ' │'
            if bar.owner != -1:
                tree = ' │'
            if bartype == Bar.LEFT:
                if bar.owner == -1:
                    tree = ' '
                if bar.owner != -1:
                    tree = ' ├─'
                    if bar.stream_index == bar.owned:
                        tree = ' └─'
                if bar.channels != 1:
                    brackets = [BAR_TOP_LEFT, BAR_TOP_RIGHT]
                else:
                    brackets = [BAR_LEFT_MONO, BAR_RIGHT_MONO]
            elif bartype == bar.channels - 1:
                if bar.stream_index == bar.owned:
                    tree = ' '
                brackets = [BAR_BOTTOM_LEFT, BAR_BOTTOM_RIGHT]
            else:
                if bar.stream_index == bar.owned:
                    tree = ' '
                brackets = ['├', '┤']

            # focus current lines
            focus_hi, bracket_hi, arrow, gradient = 0, 0, ARROW, self.gradient
            if index == self.focus_line_num:
                focus_hi = bracket_hi = curses.A_BOLD
                arrow = ARROW_FOCUSED
            elif bar in same:
                focus_hi = curses.A_BOLD
                if bar.locked:
                    bracket_hi = curses.A_BOLD
                    arrow = ARROW_LOCKED
            elif not bar.muted and self.color_mode != 2:
                gradient = self.gray_gradient

            # highlight chosen sink/source or muted
            if not self.change_mode_allowed and self.selected[0].owner == self.data[index][0].index:
                bracket_hi = self.red | bracket_hi
            elif bar.muted:
                bracket_hi = bracket_hi | self.red
                focus_hi = focus_hi | self.muted_color
            off = 6 * (self.cols // (43 if self.cols <= 60 else 25)) - len(tree)
            cols = self.cols - 31 - off - len(tree)
            vol = list(BAR_OFF * (cols - (cols % 3 != 0)))
            n = int(len(vol) * bar.volume[bartype] / bar.maxsize)
            vol[:n] = BAR_ON * n
            vol = ''.join(vol)
            if bartype is Bar.LEFT:
                if bar.pa.name in (self.server.default_sink_name, self.server.default_source_name):
                    tree = '*'
                name = '{}{}'.format(bar.name, bar.media_name)
                name = name[:20 + off] + '~' if len(name) > 20 + off else name
                line = '{:<{}}|{}\n {:<3}|{}\n '.format(name, 22 + off, focus_hi,
                                                        '' if type(bar.pa) is PulseCard else bar.volume[0],
                                                        focus_hi)
            elif bartype is Bar.RIGHT:
                line = '{:>{}}|{}\n {}|{}\n {:<3}|{}\n '.format(
                    '', 21 + off, self.red if bar.locked else curses.A_DIM,
                    '', self.red if bar.muted else curses.A_DIM,
                    bar.volume[bartype], focus_hi)
            else:
                line = '{:>{}}{:<3}|{}\n '.format('', 23 + off, bar.volume[bartype], focus_hi)
            if type(bar.pa) is PulseCard:
                volbar = '\n{}|0'.format(bar.pa.active_profile.description.decode()[:len(vol)])
                brackets = [' ', ' ']
            else:
                volbar = ''
                for i, v in enumerate(re.findall('.{{{}}}'.format((len(vol) // 3)), vol)):
                    volbar += '\n{}|{}'.format(v, gradient[i] | focus_hi)
            line += '{:>1}|{}\n{}|{}{}\n{}|{}\n{}|{}'.format(arrow, curses.A_BOLD,
                                                             brackets[0], bracket_hi,
                                                             volbar,
                                                             brackets[1], bracket_hi,
                                                             arrow, curses.A_BOLD)
            self.display_line(index + 1, tree + "|0\n" + line)
        self.display_line(self.lines + 1, self.info)
        self.screen.refresh()

    def display_helpwin(self):
        '''h/j/k/l, arrows               navigation, volume change
          H/L, Shift+Left/Shift+Right   change volume by 10
          1/2/3/4/5/6/7/8/9/0           set volume to 10%-100%
          m                             mute/unmute
          Space                         lock/unlock channels together
          Enter                         context menu
          F1/F2/F3                      change modes
          Tab                           go to next mode
          Mouse left click              select device or mode
          Mouse wheel                   volume change
          q/Esc/^C                      quit'''
        self.helpwin.erase()
        self.helpwin.border()
        for i, s in enumerate(self.display_helpwin.__doc__.split('\n')):
            self.helpwin.addstr(i + 1, 1, s.strip(), curses.A_NORMAL)
        self.helpwin.refresh()

    def run_helpwin(self):
        c = self.screen.getch()
        if c == ord('q') or c == self.ESC_KEY:
            self.helpwin_show = False

    def display_submenu(self):
        self.submenu.erase()
        top = self.top_line_num
        bottom = self.top_line_num + self.lines + 2
        self.submenu.resize(curses.LINES, self.submenu_width + 1)
        self.submenu.vline(0, self.submenu_width, curses.ACS_VLINE, self.lines + 2)
        for index, line in enumerate(self.submenu_data[top:bottom]):
            if index == self.focus_line_num:
                focus_hi = curses.A_BOLD
                arrow = ARROW_FOCUSED
            else:
                focus_hi = curses.A_NORMAL
                arrow = ' '
            if '|' in line:
                self.display_line(index, ' ' + arrow + line, focus_hi)
            else:
                self.submenu.addstr(index, 1, arrow + ' ' + line, focus_hi)
        self.submenu.refresh()

    def scroll(self, n):
        next_line_num = self.focus_line_num + n

        if n == self.UP and self.focus_line_num == 0 and self.top_line_num != 0:
            self.top_line_num += self.UP
            return
        elif n == self.DOWN and next_line_num == self.lines and\
                (self.top_line_num + self.lines) != self.n_lines:
            self.top_line_num += self.DOWN
            return

        if n == self.UP and (self.top_line_num != 0 or self.focus_line_num != 0):
            self.focus_line_num = next_line_num
        elif n == self.DOWN and self.focus_line_num != self.lines and\
                (self.top_line_num + self.focus_line_num + 1) != self.n_lines:
            self.focus_line_num = next_line_num


def usage():
    print(__doc__)

pulse = None


def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hvl",
            ["help", "version", "list", "list-sinks", "list-sources", "id=",
             "set-volume=", "set-volume-all=", "change-volume=", "get-volume",
             "get-mute", "toggle-mute", "mute", "unmute",
             "color=", "server=", "no-mouse"])
    except getopt.GetoptError as err:
        sys.exit("ERR: {}".format(err))
    assert args == [], sys.exit('ERR: {} not not recognized'.format(' '.join(args).strip()))

    dopts = dict(opts)
    server = dopts.get('--server', '').encode() or None
    mouse = True if '--no-mouse' not in dopts else False
    try:
        color = min(2, max(0, int(dopts.get('--color', '') or 2)))
    except:
        sys.exit('ERR: color must be a number')
    global pulse
    pulse = Pulse('pulsemixer', server)

    noninteractive_opts = dict(dopts)
    noninteractive_opts.pop('--server', None)
    noninteractive_opts.pop('--color', None)
    noninteractive_opts.pop('--no-mouse', None)
    if not noninteractive_opts:
        if sys.stdout.isatty():
            title = 'pulsemixer {}'.format(server.decode() if server else '')
            sys.stdout.write('\033]2;{}\007'.format(title.strip()))
            sys.stdout.flush()
            curses.wrapper(Screen(color, mouse).run)
        else:
            sys.exit('ERR: output is not a tty-like device')

    sinks = pulse.sink_list()
    sink_inputs = pulse.sink_input_list()
    sources = pulse.source_list()
    source_outputs = pulse.source_output_list()
    server_info = pulse.get_server_info()
    index = [s.index for s in sinks if s.name == server_info.default_sink_name][0]
    streams = {}
    for i in source_outputs + sources + sink_inputs + sinks:
        streams[i.index] = i
    check_id = lambda x: x in streams or sys.exit('ERR: No such ID: ' + str(x))
    check_id(index)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            sys.exit(usage())

        if opt in ('-v', '--version'):
            sys.exit(print(VERSION))

        elif opt == '--id':
            try:
                index = int(arg)
            except:
                sys.exit('ERR: id must be a number')
            check_id(index)

        elif opt in ('-l', '--list'):
            for sink in sink_inputs:
                print("Sink input:\t", sink)
            for source in source_outputs:
                print("Source output:\t", source)
            for sink in sinks:
                print("Sink:\t\t", sink)
            for source in sources:
                print("Source:\t\t", source)

        elif opt == '--list-sinks':
            for sink in sink_inputs:
                print("Sink input:\t", sink)
            for sink in sinks:
                print("Sink:\t\t", sink)

        elif opt == '--list-sources':
            for source in source_outputs:
                print("Source output:\t", source)
            for source in sources:
                print("Source:\t\t", source)

        elif opt == '--get-mute':
            print(streams[index].mute)

        elif opt == '--mute':
            pulse.mute_stream(streams[index])

        elif opt == '--unmute':
            pulse.unmute_stream(streams[index])

        elif opt == '--toggle-mute':
            if streams[index].mute:
                pulse.unmute_stream(streams[index])
            else:
                pulse.mute_stream(streams[index])

        elif opt == '--get-volume':
            print(*streams[index].volume.values)

        elif opt == '--set-volume':
            vol = streams[index].volume
            for i, _ in enumerate(vol.values):
                vol.values[i] = int(arg)
            pulse.set_volume(streams[index], vol)

        elif opt == '--set-volume-all':
            vol = streams[index].volume
            arg = arg.strip(':').split(':')
            if len(arg) != len(vol.values):
                sys.exit("ERR: Specified volumes not equal to number of channles in the stream")
            for i, _ in enumerate(vol.values):
                vol.values[i] = int(arg[i])
            pulse.set_volume(streams[index], vol)

        elif opt == '--change-volume':
            vol = streams[index].volume
            for i, _ in enumerate(vol.values):
                vol.values[i] += int(arg)
            pulse.set_volume(streams[index], vol)


if __name__ == '__main__':
    main()
