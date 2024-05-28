# -*- coding: utf-8 -*-
"""
GUI routing for the Matchday Kodi plugin.
"""
#  Copyright (c) 2023
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import re
import sys

import routing
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from resources.lib.model.event import Match
from resources.lib.model.repository import CompetitionRepository, \
    TeamRepository, VideoSourceListRepository, EventRepository

__handle__ = int(sys.argv[1])
HLS_MIME_TYPE = 'application/mpegurl'
GENRES = ['Sports']
MAX_VIDEO_RETRIES = 5

PLUGIN = routing.Plugin()
# Data repositories
EVENT_REPO = EventRepository()
COMP_REPO = CompetitionRepository()
TEAM_REPO = TeamRepository()
VIDEO_SOURCE_REPO = VideoSourceListRepository()


# ==============================================================================
# Routes
# ==============================================================================
@PLUGIN.route('/')
def home():
    """
    Display the root (home) listing
    """
    xbmc.log("Creating main menu", xbmc.LOGINFO)
    # Display navigation links
    xbmcplugin.addDirectoryItem(PLUGIN.handle, PLUGIN.url_for(list_events),
                                xbmcgui.ListItem("All Events"), True)
    xbmcplugin.addDirectoryItem(PLUGIN.handle, PLUGIN.url_for(
        list_competitions), xbmcgui.ListItem("Competitions"), True)
    xbmcplugin.addDirectoryItem(PLUGIN.handle, PLUGIN.url_for(list_teams),
                                xbmcgui.ListItem("Teams"), True)
    xbmc.log("Created main menu successfully", xbmc.LOGINFO)
    # Finish creating virtual folder
    xbmcplugin.endOfDirectory(PLUGIN.handle)


@PLUGIN.route('/events')
def list_events():
    """
    Display a list of Events
    """
    url = None
    if 'url' in PLUGIN.args:
        url = PLUGIN.args['url'][0]
    xbmc.log(f"Getting Events from repo at URL: {url}", xbmc.LOGINFO)
    # Get Events from repo
    events = EVENT_REPO.get_all_events(url)
    # Display Events
    create_events_listing(events)


@PLUGIN.route('/competitions')
def list_competitions():
    """
    Display a listing of all competitions
    """
    # Set content type
    xbmcplugin.setContent(PLUGIN.handle, "mixed")
    xbmc.log("Getting all Competitions from repo", xbmc.LOGINFO)
    # Retrieve competition data from repo
    competitions = COMP_REPO.get_all_competitions()
    # Display the competitions as a directory listing
    create_competition_listing(competitions)


@PLUGIN.route('/teams')
def list_teams():
    """
    Display all teams
    """
    url = None
    if 'url' in PLUGIN.args:
        url = PLUGIN.args['url'][0]
    # Retrieve Team data from repo
    teams = TEAM_REPO.get_all_teams(url)
    # Display Teams
    create_teams_listing(teams)


@PLUGIN.route('/competitions/<competition_id>/teams')
def list_teams_by_competition_id(competition_id):
    """
    Displays a list of teams by competition_id
    :param competition_id: The competition_id for which we want teams
    """
    teams = COMP_REPO.get_teams_by_competition_id(competition_id)
    create_teams_listing(teams)


@PLUGIN.route('/competitions/details/<competition_id>')
def show_competition(competition_id):
    """
    Displays a list of Competition info, including events, etc.
    :param competition_id: The competition we want to show Events for
    :return: None
    """
    xbmc.log(f"Getting details for Competition: {competition_id}", xbmc.LOGINFO)
    # Display a link to the Teams for this competition_id
    competition = COMP_REPO.get_competition_by_id(competition_id)
    team_link = xbmcgui.ListItem("Teams")
    team_link.setArt({'fanart': competition.links['fanart']['href']})
    xbmcplugin.addDirectoryItem(PLUGIN.handle, PLUGIN.url_for(
        list_teams_by_competition_id, competition_id), team_link, True)
    # Get Events for this competition_id
    events = COMP_REPO.get_events_by_competition_id(competition_id)
    create_events_listing(events)


@PLUGIN.route('/play/<path:video_source_url>')
def play_video(video_source_url):
    """
    Retrieve the playlist from the repo, get the best variant
    :param video_source_url: The URL of the playlist resource
    :return: None
    """
    xbmc.log("Playing playlist at URL: {}".format(video_source_url), xbmc.LOGINFO)
    # Get "best" video source
    video_source_list = VIDEO_SOURCE_REPO.fetch_video_source_list(video_source_url)
    video_source = video_source_list.get_preferred_source()
    play_video_source(video_source)


@PLUGIN.route('/video/select_video_source/<path:video_source_url>')
def select_video_source(video_source_url):
    video_source_list = VIDEO_SOURCE_REPO.fetch_video_source_list(video_source_url)
    xbmc.log("Retrieved playlist: {}".format(video_source_list), xbmc.LOGINFO)

    sources = []
    for variant in video_source_list.variants:
        item = xbmcgui.ListItem(label="{}".format(variant))
        sources.append(item)

    # display select video source dialog
    dialog = xbmcgui.Dialog()
    selected_idx = dialog.select('Select video source', sources)
    # handle dialog selection; -1 = cancel
    if selected_idx != -1:
        selected = video_source_list.get_variant_source(selected_idx)
        play_video_source(selected)


def play_video_source(video_source):
    """
    Play all items in a playlist
    """
    global __handle__
    global MAX_VIDEO_RETRIES

    xbmc.log("Playing Video Source: {}".format(video_source), xbmc.LOGINFO)
    items = video_source['uris']

    # begin playing first item
    item = items[0]
    list_item = xbmcgui.ListItem(path=item['uri'], label=item['title'])
    list_item.setContentLookup(False)
    list_item.setMimeType(HLS_MIME_TYPE)
    xbmcplugin.setResolvedUrl(__handle__, True, listitem=list_item)

    # add remaining items to playlist
    kodi_playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    for item in items[1:]:
        li = xbmcgui.ListItem(label=item['title'])
        li.setContentLookup(False)
        li.setMimeType(HLS_MIME_TYPE)
        url = item['uri']
        kodi_playlist.add(url=url, listitem=li)


def get_playlist_items(playlist):
    xbmc.log("Parsing playlist:\n{}".format(playlist), xbmc.LOGINFO)
    items = []
    segments = playlist.split("\n")
    title = ""
    for segment in segments:
        if segment.startswith("#"):
            title = segment[1:].strip()
        if validate_url(segment):
            url = segment.strip()
            xbmc.log("Media segment: title is: {}; URL is: {}".format(title, url), xbmc.LOGINFO)
            items.append({'url': url, 'title': title})
    return items


def validate_url(url):
    regex = re.compile(r'^https?://[\w.]+:?\d*[/\w.-]*\??[\w&=]*', re.IGNORECASE)
    return re.match(regex, url)


# ==============================================================================
# Creation methods
# ==============================================================================
def force_view(mode):
    """
    Determine if view mode should be changed according to settings,
    and force the specified mode if desired
    """
    matchday = xbmcaddon.Addon()
    force_view_setting = matchday.getSetting('matchday-force-view')
    if force_view_setting == 'true':
        xbmc.executebuiltin(f"Container.SetViewMode({mode})")


def create_events_listing(data):
    """
    Creates a directory listing of Event objects
    :param data: A list of Events and a link to more
    :return: None
    """
    for event in data['events']:
        # Create a view for each Event
        tile = create_event_tile(event)
        video_source_url = event.links['video']['href']
        # Add tile to GUI with link to play item
        xbmcplugin.addDirectoryItem(PLUGIN.handle,
                                    PLUGIN.url_for(play_video, video_source_url),
                                    tile)
    next_url = data['next']
    if next_url is not None:
        __create_next_button(list_events, next_url)

    # Finish directory listing
    xbmcplugin.setContent(int(__handle__), 'episodes')
    xbmcplugin.endOfDirectory(PLUGIN.handle)
    force_view(56)


def create_event_tile(event):
    """
    Creates an Event tile (view) for use in the GUI
    :param event: The Event for this tile
    :return: The Event view
    """
    global __handle__

    xbmc.log("Creating Event tile: {}".format(event), xbmc.LOGINFO)
    list_item = xbmcgui.ListItem(label=event.title)
    list_item.setProperty('IsPlayable', 'true')
    list_item.setProperty('EventDate', event.date.strftime("%d/%m"))

    # artwork
    competition = event.competition
    thumb = event.links['artwork']['href']
    list_item.setArt({'icon': thumb, 'thumb': thumb, 'landscape': thumb})
    list_item.setArt({'poster': competition.links['emblem']['href']})
    list_item.setArt({'fanart': competition.links['fanart']['href']})

    # metadata
    info_tag = list_item.getVideoInfoTag()
    info_tag.setTitle(event.title)
    info_tag.setGenres(GENRES)
    info_tag.setDateAdded("{}".format(event.date))

    # context menu
    playlist_url = event.links['video']['href']
    select_video = PLUGIN.url_for(select_video_source, playlist_url)
    list_item.addContextMenuItems([('Select source...', 'PlayMedia(%s)' % select_video)])

    if isinstance(event, Match):
        # Set Match-specific properties
        list_item.setProperty('IsMatch', 'true')
        list_item.setProperty('HomeTeam',
                              '{}'.format(event.home_team))
        list_item.setProperty('HomeTeamEmblemUrl',
                              event.home_team.links['emblem']['href'])
        list_item.setProperty('AwayTeam',
                              '{}'.format(event.away_team))
        list_item.setProperty('AwayTeamEmblemUrl',
                              event.away_team.links['emblem']['href'])
    else:
        # Set HighlightShow properties
        list_item.setProperty('IsHighlight', 'true')
        list_item.setProperty('CompetitionEmblemUrl',
                              competition.links['emblem']['href'])
    # Return the tile as a tuple
    return list_item


def __create_next_button(action, next_url):
    plus_icon = 'special://home/addons/plugin.matchday/resources/img/more_icon.png'
    next_button = xbmcgui.ListItem(label='More...')
    next_button.setArt({'icon': plus_icon, 'thumb': plus_icon})
    xbmcplugin.addDirectoryItem(PLUGIN.handle, PLUGIN.url_for(
        action, url=next_url['href']), next_button, True)


def create_competition_listing(competitions):
    """
    Create a directory listing for competition objects
    :param competitions: A list of competition objects
    :return: None
    """
    for competition in competitions:
        title = competition.name
        comp_id = competition.comp_id
        thumb = competition.links['emblem']['href']
        fanart = competition.links['fanart']['href']
        # Setup list view item
        list_item = xbmcgui.ListItem(label=title)
        video_info = list_item.getVideoInfoTag()
        video_info.setTitle(title)
        video_info.setGenres(GENRES)
        list_item.setArt({
            'thumb': thumb,
            'fanart': fanart,
            'clearart': thumb
        })
        # Add list item to listing
        xbmcplugin.addDirectoryItem(PLUGIN.handle,
                                    PLUGIN.url_for(show_competition, comp_id),
                                    list_item, True)
    # Ensure Kodi ignores "the" at beginning
    xbmcplugin.addSortMethod(PLUGIN.handle,
                             xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating virtual folder
    xbmcplugin.setContent(int(__handle__), 'tvshows')
    xbmcplugin.endOfDirectory(PLUGIN.handle)
    force_view(561)


def create_teams_listing(data):
    """
    Create a directory listing for Team objects
    :param data: A list of teams to be rendered & a link to more
    :return: None
    """
    for team in data['teams']:
        title = '{}'.format(team)
        thumb = team.links['emblem']['href']
        events_url = team.links['events']['href']
        # Create a list item view
        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({'icon': thumb})
        video_info = list_item.getVideoInfoTag()
        video_info.setTitle(title)
        video_info.setGenres(GENRES)
        # Add list item to listing
        xbmcplugin.addDirectoryItem(PLUGIN.handle,
                                    PLUGIN.url_for(list_events, url=events_url),
                                    list_item, True)
    next_url = data['next']
    if next_url is not None:
        __create_next_button(list_teams, next_url)
    # Ensure Kodi ignores "the"
    xbmcplugin.addSortMethod(PLUGIN.handle,
                             xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating virtual folder
    xbmcplugin.setContent(int(__handle__), 'videos')
    xbmcplugin.endOfDirectory(PLUGIN.handle)
    force_view(56)


def get_default_fanart():
    """
    Gets the default fanart image from the 'resources' directory.
    :return: Default fanart image
    """
    addon = xbmcaddon.Addon()
    return os.path.join(addon.getAddonInfo('path'), 'resources',
                        'img', 'fanart.jpg')


def run():
    """
    Wrap the plugin run() method
    """
    PLUGIN.run()
