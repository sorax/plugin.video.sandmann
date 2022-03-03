# -*- coding: utf-8 -*-
# Copyright 2022 sorax
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

import sys

from libs.episodes import getEpisodes
from threading import Timer

# -- Addon --
addon = xbmcaddon.Addon()
addon_handle = int(sys.argv[1])
addon_name = addon.getAddonInfo("name")
addon_icon = addon.getAddonInfo("icon")

base_path = sys.argv[0]

# -- Constants --
episodes_url = "https://appdata.ardmediathek.de/appdata/servlet/tv/Sendung?documentId=6503982&json"

# -- Settings --
dgs = addon.getSettingInt("dgs2")
interval = addon.getSettingInt("interval2")
quality = addon.getSettingInt("quality2")
update = addon.getSettingInt("update2")

# -- Variables --
# refresh_timer = None


def sandmann():
    episodes_list = getEpisodes(episodes_url, quality)

    item_list = []
    for episode in episodes_list:
        if dgs == 0 and episode["dgs"] == False:
            item_list.append((episode["stream"], getListItem(episode), False))
        if dgs == 1:
            item_list.append((episode["stream"], getListItem(episode), False))
        if dgs == 2 and episode["dgs"] == True:
            item_list.append((episode["stream"], getListItem(episode), False))

    xbmcplugin.addDirectoryItems(addon_handle, item_list, len(item_list))
    xbmcplugin.endOfDirectory(addon_handle)


def getListItem(item):
    li = xbmcgui.ListItem(label=item["title"])
    li.setArt({
        "thumb": item["thumb"],
        "fanart": item["fanart"]
    })
    li.setInfo(
        type="video",
        infoLabels={
            "title": item["title"],
            "plot": item["desc"],
            "duration": item["duration"]
        }
    )
    li.setProperty("IsPlayable", "true")
    return li
