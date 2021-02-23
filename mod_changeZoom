import Keys

from Avatar import PlayerAvatar

from constants import BigWorld
from debug_utils import LOG_ERROR

from gui.mods.hook import g_overrideLib
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore

__version__ = 'V1.2 26.03.2020'
__author__ = 'PVirex'


class HelpKey:
    settingsCore = dependency.instance(ISettingsCore)  # type: ISettingsCore
    currentValue = True


@g_overrideLib.registerEvent(PlayerAvatar, 'handleKey')
def new_handleKey(self, isDown, key, mods):
    if BigWorld.isKeyDown(Keys.KEY_H):
        HelpKey.settingsCore.applySetting('increasedZoom', HelpKey.currentValue)
        HelpKey.currentValue = False if HelpKey.currentValue else True


@g_overrideLib.registerEvent(PlayerAvatar, '_PlayerAvatar__destroyGUI', True, True)
def new__destroyGUI(self):
    HelpKey.currentValue = True


@g_overrideLib.registerEvent(PlayerAvatar, '_PlayerAvatar__initGUI', True, True)
def new__initGUI(self):
    HelpKey.settingsCore.applySetting('increasedZoom', False)


print '[MOD_LOADED] Loading mod: "chang_increasedZoom" %s Author: %s' % (__version__, __author__)
