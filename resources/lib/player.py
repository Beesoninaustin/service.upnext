# -*- coding: utf-8 -*-
# GNU General Public License v2.0 (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

from __future__ import absolute_import, division, unicode_literals
import xbmc
from . import utils
from .api import Api
from .developer import Developer
from .state import State


class Player(xbmc.Player):
    ''' Service class for playback monitoring '''
    last_file = None
    track = False

    def __init__(self):
        self.api = Api()
        self.state = State()
        self.developer = Developer()
        xbmc.Player.__init__(self)

    def set_last_file(self, filename):
        self.state.last_file = filename

    def get_last_file(self):
        return self.state.last_file

    def is_tracking(self):
        return self.state.track

    def disable_tracking(self):
        self.state.track = False

    def onPlayBackStarted(self):  # pylint: disable=invalid-name
        ''' Will be called when kodi starts playing a file '''
        xbmc.sleep(5000)  # Delay for slower devices, should really use onAVStarted for Leia
        if not xbmc.getCondVisibility('videoplayer.content(episodes)'):
            return
        self.state.track = True
        if utils.settings('developerMode') == 'true':
            self.developer.developer_play_back()

    def onPlayBackPaused(self):  # pylint: disable=invalid-name
        self.state.pause = True

    def onPlayBackResumed(self):  # pylint: disable=invalid-name
        self.state.pause = False

    def onPlayBackStopped(self):  # pylint: disable=invalid-name
        ''' Will be called when user stops playing a file '''
        self.api.reset_addon_data()
        self.state = State()  # Reset state
