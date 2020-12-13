#!/usr/bin/env python3
"""
Represents remote data server.
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

import json

import requests

from resources.lib.model.competition import Competition
from resources.lib.model.event import Event
from resources.lib.model.team import Team


class Server:
    """Represents the remote data server"""
    # Todo: move to options
    __SCHEMA = "http://"
    __ADDR = "192.168.0.104"
    __PORT = 8080

    # TODO: Add error handling for data retrieval failure
    def __init__(self):
        """
        Initialize remote server url
        """
        self.url = Server.__SCHEMA + Server.__ADDR + ":" + str(Server.__PORT)
        self.roots = None

    def get_roots(self):
        """
        Gets root elements from remote server
        :rtype: dict
        """
        # Load root data once
        # if self.roots is None:
        remote_json = requests.get(self.url + "/").text
        self.roots = json.loads(remote_json)['_links']
        return self.roots

    def get_all_events(self):
        """
        Retrieves all latest Events from remote data server
        :return: A list of Event objects
        """
        events_url = self.get_roots().get("events")['href']
        # Read Events data
        events = requests.get(events_url).text
        # Parse into JSON
        events_json = json.loads(events)['_embedded']['events']
        # Map to Event objects & return
        return list(map(Event.create_event, events_json))

    def get_all_competitions(self):
        """
        Retrieve all competition_id data from remote server
        :return:
        """
        # Get link to competition data
        competition_url = self.get_roots().get("competitions")['href']
        # Read competition data
        competitions = requests.get(competition_url).text
        # Parse to JSON
        competition_json = json.loads(competitions)['_embedded']['competitions']
        # Map to competition objects & return
        return list(map(Competition.create_competition, competition_json))

    def get_all_teams(self):
        """
        Retrieves all teams from remote server
        :return: A list of teams
        """
        # Get team data url
        teams_url = self.get_roots().get("teams")['href']
        # Read teams data
        teams = requests.get(teams_url).text
        # Parse into JSON and return
        team_json = json.loads(teams)['_embedded']['teams']
        # Map to Team object & return
        return list(map(Team.create_team, team_json))

    def get_featured_events(self):
        """
        Get the featured events from the remote server
        :return: A list of events
        """
        # Get featured events
        root_data = requests.get(self.url + "/").text
        featured_event_data = \
            json.loads(root_data)['featuredEvents']['_embedded']['events']
        return list(map(Event.create_event, featured_event_data))

    # TODO: Static methods? Combine with repo logic?
    def get_teams_by_competition(self, competition):
        """
        Retrieves all Teams competing in the specified competition_id
        :param competition: The competition_id for which we want Teams
        :return: A list of Teams in this competition_id
        """
        data_url = competition.links['teams']['href']
        # Read data from server
        team_data = requests.get(data_url).text
        # Parse into JSON
        teams_json = json.loads(team_data)['_embedded']['teams']
        return list(map(Team.create_team, teams_json))

    def get_events_by_competition(self, competition):
        """
        Retrieves all Events for the specified competition_id from the server
        :param competition: The competition_id for which we want events
        :return: A list of Events in this competition_id
        """
        # Competition data url
        data_url = competition.links['events']['href']
        # Get data from server
        comp_event_data = \
            json.loads(requests.get(data_url).text)['_embedded']['events']
        return list(map(Event.create_event, comp_event_data))

    def get_events_by_team(self, team):
        """
        Retrieves all Events in which the specified Team participates from  the
        remote data server.
        :param team: The Team for which Events are desired
        :return: A list of Events
        """
        data_url = team.links['events']['href']
        # Read team Events from server
        event_data = \
            json.loads(requests.get(data_url).text)['_embedded']['events']
        return list(map(Event.create_event, event_data))

    def get_playlist(self, url):
        """
        Retrieve playlist resource JSON from remote server
        :param url: The URL of the playlist resource
        :return: A JSON object of the playlist resource
        """
        # Fetch the playlist resource
        playlists_data = requests.get(url).text
        return playlists_data
