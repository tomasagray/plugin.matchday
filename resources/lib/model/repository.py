#!/usr/bin/env python3
"""
Represents data repositories.
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

    def __fetch_events(self, url=None):
        """
        Refreshes local Event data cache
        """
        self.events = self.server.get_all_events(url)

    def get_all_events(self, url=None):
        """
        Fetches Events
        :return: A list of all latest Events
        """
        self.__fetch_events(url)
        return self.events

    def get_event_by_id(self, event_id):
        """
        Retrieves a specific Event based on the eventId
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
        Get all competitions
        :return: List of Competitions from the remote server
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
        xbmc.log(f'Using ID: {comp_id}, found Competition in memory: {competition}',
                 1)
        comp_events = self.server.get_events_by_competition(competition)
        return comp_events

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

    def __fetch_teams(self, url=None):
        """
        Retrieves all Team data from remote server
        :return: None
        """
        self.teams = self.server.get_all_teams(url)

    def get_all_teams(self, url=None):
        """
        Gets all team objects from local data store
        :return: A list of Team objects
        """
        # If the local data store is empty, update
        if self.teams is None:
            self.__fetch_teams(url)
        return self.teams

    def __find_team_by_id(self, team_id):
        for team in self.teams:
            if team.team_id == team_id:
                return team


class PlaylistRepository:
    """
    Represents the local data access to media playlists on remote server
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
        xbmc.log("Retrieving video playlist data from URL: {}".format(url), 1)
        playlist_json = self.server.get_playlist(url)
        return Playlist.create_playlist(playlist_json)
