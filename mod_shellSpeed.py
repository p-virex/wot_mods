# coding: utf-8
import BigWorld

from debug_utils import LOG_ERROR
from gui import GUI_SETTINGS
from gui.Scaleform.daapi.view.battle.shared.consumables_panel import TOOLTIP_FORMAT, TOOLTIP_NO_BODY_FORMAT, \
    ConsumablesPanel
from gui.Scaleform.locale.INGAME_GUI import INGAME_GUI
from gui.impl import backport
from gui.mods.hook import g_overrideLib
from items.vehicles import g_cache
from helpers import i18n

__version__ = 'V1.0.1 31.03.2020'
__author__ = 'PVirex'


@g_overrideLib.overrideMethod(ConsumablesPanel, '_ConsumablesPanel__makeShellTooltip')
def __makeShellTooltip(self, descriptor, piercingPower):
    kind = descriptor.kind
    player = BigWorld.player()
    gunID = player.getVehicleDescriptor().gun.id[-1]
    shellNation = descriptor.id[0]
    shellName = descriptor.name
    shellSpeed = 'error'
    shotsObject = g_cache.guns(shellNation).get(gunID).shots
    for i, shot in enumerate(shotsObject):
        if shotsObject[i].shell.name == shellName:
            shellSpeed = shotsObject[i].speed * 1.25
            break
    header = i18n.makeString('#ingame_gui:shells_kinds/{0:>s}'.format(kind),
                             caliber=backport.getNiceNumberFormat(descriptor.caliber), userString=descriptor.userString)
    if GUI_SETTINGS.technicalInfo:
        tooltipStr = INGAME_GUI.SHELLS_KINDS_PARAMS
        paramsDict = {'damage': str(int(descriptor.damage[0])),
                      'piercingPower': str(piercingPower)}
        if descriptor.hasStun and self.lobbyContext.getServerSettings().spgRedesignFeatures.isStunEnabled():
            stun = descriptor.stun
            tooltipStr = INGAME_GUI.SHELLS_KINDS_STUNPARAMS
            paramsDict['stunMinDuration'] = backport.getNiceNumberFormat(
                stun.guaranteedStunDuration * stun.stunDuration)
            paramsDict['stunMaxDuration'] = backport.getNiceNumberFormat(stun.stunDuration)
        body = i18n.makeString(tooltipStr, **paramsDict)
        fmt = TOOLTIP_FORMAT
    else:
        body = ''
        fmt = TOOLTIP_NO_BODY_FORMAT
    tmp = '\nСкорость снаряда: {} м/с\nМаксимальный/минимальный урон: {}/{}\nМаксимльное/минимальное пробитие: {}/{} мм'
    body += tmp.format(int(shellSpeed), int(descriptor.damage[0] * 1.25), int(descriptor.damage[0] * 0.75),
                       int(piercingPower * 1.25), int(piercingPower * 0.75))
    return fmt.format(header, body)


print '[MOD_LOADED] Loading mod: "shell_speed_in_tooltip" %s Author: %s' % (__version__, __author__)
