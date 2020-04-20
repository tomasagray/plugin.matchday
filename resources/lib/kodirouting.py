# -*- coding: utf-8 -*-
"""
GUI routing for the Matchday Kodi plugin.
"""
import os

import routing
import xbmc
import xbmcplugin
import xbmcaddon
from xbmcgui import ListItem
from resources.lib.model.repository import CompetitionRepository, TeamRepository
from resources.lib.model.server import Server

PLUGIN = routing.Plugin()
COMP_REPO = CompetitionRepository()
TEAM_REPO = TeamRepository()


@PLUGIN.route('/')
def home():
    """
    Display the root (home) listing
    """
    xbmc.log("Creating home menu")
    # Display navigation links
    xbmcplugin.addDirectoryItem(PLUGIN.handle, PLUGIN.url_for(
        list_competitions), ListItem("Competitions"), True)
    xbmcplugin.addDirectoryItem(PLUGIN.handle, PLUGIN.url_for(list_teams),
                                ListItem("All Teams"), True)
    # Display featured events
    events = Server().get_featured_events()
    create_events_listing(events)


@PLUGIN.route('/competitions')
def list_competitions():
    """
    Display a listing of all competitions
    """
    xbmc.log("Getting competitions from repo")
    # Retrieve competition data from repo
    competitions = COMP_REPO.get_all_competitions()
    # Display the competitions as a directory listing
    create_competition_listing(competitions)


@PLUGIN.route('/teams')
def list_teams():
    """
    Display all teams
    """
    xbmc.log("Getting all teams from repo")
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
    # Display a link to the Teams for this competition_id
    team_link = ListItem("Teams")
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
        fanart = get_default_fanart()
        # Setup list view item
        list_item = ListItem(label=title)
        list_item.setInfo('video', {'title': title, 'genre': 'Sports'})
        list_item.setArt({'thumb': thumb, 'fanart': fanart})
        # Add list item to listing
        xbmcplugin.addDirectoryItem(PLUGIN.handle,
                                    PLUGIN.url_for(show_competition, comp_id),
                                    list_item, True)
    # Ensure Kodi ignores "the" at beginning
    xbmcplugin.addSortMethod(PLUGIN.handle,
                             xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating virtual folder
    xbmcplugin.endOfDirectory(PLUGIN.handle)


def create_teams_listing(teams):
    """
    Create a directory listing for Team objects
    :param teams: A list of teams to be rendered
    :return: None
    """
    for team in teams:
        # TODO: why is unicode garbled in competition/teams listing?
        title = team.name
        team_id = team.team_id
        thumb = team.links['emblem']['href']
        # Create a list item view
        list_item = ListItem(label=title, thumbnailImage=thumb)
        list_item.setInfo('video', {'title': title, 'genre': 'Sports'})
        # Add list item to listing
        xbmcplugin.addDirectoryItem(PLUGIN.handle,
                                    PLUGIN.url_for(show_team, team_id),
                                    list_item, True)
    # Ensure Kodi ignores "the"
    xbmcplugin.addSortMethod(PLUGIN.handle,
                             xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating virtual folder
    xbmcplugin.endOfDirectory(PLUGIN.handle)


def create_events_listing(events):
    """
    Creates a directory listing of Event objects
    :param events: A list of Events
    :return: None
    """
    views = []
    for event in events:
        # Create a view for each Event
        views.append(create_event_tile(event))
    # Add view listing to main GUI
    xbmcplugin.addDirectoryItems(PLUGIN.handle, views, len(views))
    # Finish directory listing
    xbmcplugin.endOfDirectory(PLUGIN.handle)


def create_event_tile(event):
    """
    Creates an Event tile (view) for use in the GUI
    :param event: The Event for this tile
    :return: The Event view
    """
    competition = event.competition
    thumb = competition.links['emblem']['href']
    list_item = ListItem(label=event.title, thumbnailImage=thumb)
    list_item.setInfo('video', {'title': event.title, 'genre': 'Sports'})
    list_item.setProperty('IsPlayable', 'true')
    # Return the tile as a tuple
    return event.playlists.get_master_url(), list_item, False


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
