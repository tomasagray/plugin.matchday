# -*- coding: utf-8 -*-
"""
GUI routing for the Matchday Kodi plugin.
"""
#  Copyright (c) 2021
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
import sys
import urllib

import routing
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from resources.lib.model.event import Match
from resources.lib.model.repository import CompetitionRepository, \
    TeamRepository, PlaylistRepository, EventRepository

PLUGIN = routing.Plugin()
# Data repositories
EVENT_REPO = EventRepository()
COMP_REPO = CompetitionRepository()
TEAM_REPO = TeamRepository()
PLAYLIST_REPO = PlaylistRepository()


# ==============================================================================
# Routes
# ==============================================================================
@PLUGIN.route('/')
def home():
    """
    Display the root (home) listing
    """
    xbmc.log("Creating home menu", 2)
    # Display navigation links
    xbmcplugin.addDirectoryItem(PLUGIN.handle, PLUGIN.url_for(list_events),
                                xbmcgui.ListItem("All Events"), True)
    xbmcplugin.addDirectoryItem(PLUGIN.handle, PLUGIN.url_for(
        list_competitions), xbmcgui.ListItem("Competitions"), True)
    xbmcplugin.addDirectoryItem(PLUGIN.handle, PLUGIN.url_for(list_teams),
                                xbmcgui.ListItem("Teams"), True)
    xbmc.log("Created home menu successfully", 2)
    # Finish creating virtual folder
    xbmcplugin.endOfDirectory(PLUGIN.handle)


@PLUGIN.route('/events')
def list_events():
    """
    Display a list of all Events
    """
    xbmc.log("Getting all Events from repo", 2)
    # Get Events from repo
    events = EVENT_REPO.get_all_events()
    # Display Events
    create_events_listing(events)


@PLUGIN.route('/competitions')
def list_competitions():
    """
    Display a listing of all competitions
    """
    # Set content type
    xbmcplugin.setContent(PLUGIN.handle, "mixed")
    xbmc.log("Getting competitions from repo", 2)
    # Retrieve competition data from repo
    competitions = COMP_REPO.get_all_competitions()
    # Display the competitions as a directory listing
    create_competition_listing(competitions)


@PLUGIN.route('/teams')
def list_teams():
    """
    Display all teams
    """
    xbmc.log("Getting all teams from repo", 2)
    # Retrieve Team data from repo
    teams = TEAM_REPO.get_all_teams()
    # Display Teams
    create_teams_listing(teams)


@PLUGIN.route('/competitions/details/<competition_id>')
def show_competition(competition_id):
    """
    Displays a list of Competition info, including events, etc.
    :param competition_id: The competition we want to show Events for
    :return: None
    """
    xbmc.log("Getting details for competition: " + competition_id, 2)
    # Display a link to the Teams for this competition_id
    competition = COMP_REPO.get_competition_by_id(competition_id)
    team_link = xbmcgui.ListItem("Teams")
    team_link.setArt({'fanart': competition.links['fanart']['href']})
    xbmcplugin.addDirectoryItem(PLUGIN.handle, PLUGIN.url_for(
        list_teams_by_competition_id, competition_id), team_link, True)
    # Get Events for this competition_id
    events = COMP_REPO.get_events_by_competition_id(competition_id)
    create_events_listing(events)


@PLUGIN.route('/teams/details/<team_id>')
def show_team(team_id):
    """
    Display detailed data for team (info, events, etc.)
    :param team_id: The ID of the Team
    :return: None
    """
    # Get team Events from repo
    events = TEAM_REPO.get_events_for_team(team_id)
    create_events_listing(events)


@PLUGIN.route('/competitions/<competition_id>/teams')
def list_teams_by_competition_id(competition_id):
    """
    Displays a list of teams by competition_id
    :param competition_id: The competition_id for which we want teams
    """
    teams = COMP_REPO.get_teams_by_competition_id(competition_id)
    create_teams_listing(teams)


@PLUGIN.route('/play/<path:playlist_url>')
def play_video(playlist_url):
    """
    Retrieve the playlist from the repo; get the best variant and send it to
    Kodi to play.
    :param playlist_url: The URL of the playlist resource
    :return: None
    """
    # Parse passed-in URL
    url = urllib.unquote(urllib.unquote(playlist_url))
    # Get playlist
    playlist = PLAYLIST_REPO.fetch_playlist(url)
    xbmc_playlist = playlist.get_xbmc_playlist()
    xbmc.log("Playing URL: {}".format(playlist_url), 2)
    # Pass PlayList to Kodi player
    xbmc.Player().play(item=xbmc_playlist, windowed=False)


# ==============================================================================
# Creation methods
# ==============================================================================
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
        list_item.setInfo('video', {'title': title, 'genre': 'Sports'})
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
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    xbmcplugin.endOfDirectory(PLUGIN.handle)


def create_teams_listing(teams):
    """
    Create a directory listing for Team objects
    :param teams: A list of teams to be rendered
    :return: None
    """
    for team in teams:
        # TODO: why is unicode garbled in competition/teams listing?
        title = u'{}'.format(team).encode('utf-8')
        team_id = team.team_id
        thumb = team.links['emblem']['href']
        # Create a list item view
        list_item = xbmcgui.ListItem(label=title, thumbnailImage=thumb)
        list_item.setInfo('video', {'title': title, 'genre': 'Sports'})
        # Add list item to listing
        xbmcplugin.addDirectoryItem(PLUGIN.handle,
                                    PLUGIN.url_for(show_team, team_id),
                                    list_item, True)
    # Ensure Kodi ignores "the"
    xbmcplugin.addSortMethod(PLUGIN.handle,
                             xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating virtual folder
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    xbmcplugin.endOfDirectory(PLUGIN.handle)


def create_events_listing(events):
    """
    Creates a directory listing of Event objects
    :param events: A list of Events
    :return: None
    """
    for event in events:
        # Create a view for each Event
        tile = create_event_tile(event)
        playlist_url = event.links['video']['href']
        # Add tile to GUI with link to play item
        xbmcplugin.addDirectoryItem(PLUGIN.handle,
                                    PLUGIN.url_for(play_video, playlist_url),
                                    tile)
    # Finish directory listing
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(PLUGIN.handle)


def create_event_tile(event):
    """
    Creates an Event tile (view) for use in the GUI
    :param event: The Event for this tile
    :return: The Event view
    """
    xbmc.log(u"Creating event tile: {}".format(event).encode('utf-8'), 2)
    competition = event.competition
    thumb = competition.links['emblem']['href']
    list_item = xbmcgui.ListItem(label=event.title, thumbnailImage=thumb)
    list_item.setInfo('video', {
        'title': event.title,
        'genre': 'Sports',
        'date': event.date.strftime("%d.%m.%Y")
    })
    list_item.setProperty('IsPlayable', 'true')
    list_item.setProperty('EventDate', event.date.strftime("%d/%m"))
    if isinstance(event, Match):
        # Set Match-specific properties
        list_item.setProperty('IsMatch', 'true')
        list_item.setProperty('HomeTeam',
                              u'{}'.format(event.home_team).encode('utf-8'))
        list_item.setProperty('HomeTeamEmblemUrl',
                              event.home_team.links['emblem']['href'])
        list_item.setProperty('AwayTeam',
                              u'{}'.format(event.away_team).encode('utf-8'))
        list_item.setProperty('AwayTeamEmblemUrl',
                              event.away_team.links['emblem']['href'])
    else:
        # Set HighlightShow properties
        list_item.setProperty('IsHighlight', 'true')
        list_item.setProperty('CompetitionEmblemUrl',
                              competition.links['emblem']['href'])
    # Set fanart from competition
    list_item.setArt({'fanart': competition.links['fanart']['href'],
                      'clearlogo':
                          competition.links['monochrome_emblem']['href']})
    # Return the tile as a tuple
    return list_item


def get_default_fanart():
    """
    Gets the default fanart image from the resources directory.
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
