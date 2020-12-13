#!/usr/bin/env python3
"""
Represents data repositories.
"""
import xbmc

from resources.lib.model.playlist import Playlist
from resources.lib.model.server import Server


class EventRepository:
    """
    Local cache of Events; controls data refresh for Events
    """

    def __init__(self):
        self.server = Server()
        self.events = None

    def __fetch_events(self):
        """
        Refreshes local Event data cache
        """
        self.events = self.server.get_all_events()

    def get_all_events(self):
        """
        Determines if it is necessary to refresh local cache & returns fresh
        Events in a list
        :return: A list of all latest Events
        """
        if self.events is None:
            self.__fetch_events()
        return self.events

    def get_event_by_id(self, event_id):
        """
        Retrieves a specific Event based on the ID
        :param event_id: The ID of the Event
        :return: The requested Event, or None if not found
        """
        for event in self.events:
            if event.event_id == event_id:
                return event
        # ID not found
        return None


class CompetitionRepository:
    """
    Represents a Competition data store.
    """

    def __init__(self):
        self.server = Server()
        self.competitions = None

    def __fetch_competitions(self):
        """
        Retrieve all competitions from remote data server.
        """
        self.competitions = self.server.get_all_competitions()

    def get_all_competitions(self):
        """
        Return all competitions
        :return: All Competitions from the remote server
        """
        # If competition data is empty, refresh
        if self.competitions is None:
            self.__fetch_competitions()
        return self.competitions

    def get_competition_by_id(self, comp_id):
        """
        Get a specific competition
        :param comp_id: The ID of the competition
        :return: The requested competition, or None if not found
        """
        for competition in self.get_all_competitions():
            if competition.comp_id == comp_id:
                return competition
        # Not found
        return None

    def get_events_by_competition_id(self, comp_id):
        """
        Get all events for a specific competition
        :param comp_id: The ID of the competition
        :return: A list of Events
        """
        competition = self.get_competition_by_id(comp_id)
        return self.server.get_events_by_competition(competition)

    def get_teams_by_competition_id(self, competition_id):
        """
        Get all Teams for a given competition
        :param competition_id: The ID of the Competition
        :return: A list of Teams
        """
        competition = self.get_competition_by_id(competition_id)
        return self.server.get_teams_by_competition(competition)


class TeamRepository:
    """
    Represents the local data store for Team objects
    """

    def __init__(self):
        self.server = Server()
        self.teams = None

    def __fetch_teams(self):
        """
        Retrieves all Team data from remote server
        :return: None
        """
        self.teams = self.server.get_all_teams()

    def get_all_teams(self):
        """
        Gets all team objects from local data store
        :return: A list of Team objects
        """
        # If the local data store is empty, update
        if self.teams is None:
            self.__fetch_teams()
        return self.teams

    def get_team_by_id(self, team_id):
        """
        Get a specific Team
        :param team_id: The ID of the Team
        :return: The requested Team, or None if not found
        """
        for team in self.get_all_teams():
            if team.team_id == team_id:
                return team
        # Not found
        return None

    def get_events_for_team(self, team_id):
        """
        Get a list of all Events in which the specified team participates
        :param team_id: The ID of the Team
        :return: A list of Events for this Team
        """
        # Get the team
        team = self.get_team_by_id(team_id)
        return self.server.get_events_by_team(team)


class PlaylistRepository:
    """
    Represents the local data access to playlists on remote server
    """

    def __init__(self):
        self.server = Server()
        self.playlists = []

    def fetch_playlist(self, url):
        """
        Fetch playlist data from remote server; create a Playlist instance
        from the data & return
        :param url: The URL of the playlist
        :return: a Playlist instance
        """
        xbmc.log("Retrieving data from URL: {}".format(url), 2)
        playlist_json = self.server.get_playlist(url)
        return Playlist.create_playlist(playlist_json)
