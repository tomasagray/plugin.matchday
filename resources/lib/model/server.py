#!/usr/bin/env python3
"""
Represents remote data server.
"""

import json
import requests

from resources.lib.model.competition import Competition
from resources.lib.model.event import Event
from resources.lib.model.team import Team


class Server:
    """Represents the remote data server"""

    __REMOTE_SCHEMA = "http://"
    __REMOTE_ADDR = "192.168.0.105"
    __REMOTE_PORT = 8081

    def __init__(self):
        """
        Initialize remote server url
        """
        self.url = Server.__REMOTE_SCHEMA + \
                   Server.__REMOTE_ADDR + ":" + \
                   str(Server.__REMOTE_PORT)
        self.roots = None

    def get_roots(self):
        """
        Gets root elements from remote server
        :rtype: dict
        """
        # Load root data once
        if self.roots is None:
            remote_json = requests.get(self.url + "/").text
            self.roots = json.loads(remote_json)['_links']
        return self.roots

    def get_all_competitions(self):
        """
        Retrieve all competition_id data from remote server
        :return:
        """
        # Get link to competition_id data
        competition_url = self.get_roots().get("competitions")['href']
        # Read competition_id data
        competitions = requests.get(competition_url).text
        # Parse to JSON
        competition_json = json.loads(competitions)['_embedded']['competitions']
        # Map to competition_id objects & return
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

    def get_teams_by_competition(self, competition):
        """
        Retrieves all Teams competing in the specified competition_id
        :param competition: The competition_id for which we want Teams
        :return: A list of Teams in this competition_id
        """
        data_url = competition.links['teams']['href']
        # Read data from server
        team_data = \
            json.loads(requests.get(data_url).text)['_embedded']['teams']
        return list(map(Team.create_team, team_data))

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
