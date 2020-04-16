#!/usr/bin/env python3
"""
Contains all event representations: the abstract event class, and its
concretions, Match and Highlight Show.
"""
from resources.lib.model.competition import Competition
from resources.lib.model.playlist import Playlist
from resources.lib.model.team import Team


class Event(object):
    """
    Represents a sporting event
    """

    def __init__(self, event_id, date, title, competition, fixture, season,
                 playlists):
        self.event_id = event_id
        self.date = date
        self.title = title
        self.competition = competition
        self.fixture = fixture
        self.season = season
        self.playlists = playlists

    def __str__(self):
        return self.title

    @staticmethod
    def create_event(event_data):
        """
        Factory method to create an Event of the appropriate subtype.
        :param event_data: The Event data (JSON)
        :return: An Event object or subtype
        """
        # Check for the presence of a team
        if 'homeTeam' in event_data.keys():
            # It's a Match event
            return Match(event_data['eventId'], event_data['date'],
                         event_data['title'],
                         Competition.create_competition(
                             event_data['competition']),
                         event_data['fixture'], event_data['season'],
                         Playlist.create_playlist(event_data['playlists']),
                         Team.create_team(event_data['homeTeam']),
                         Team.create_team(event_data['awayTeam']))

        # It's a Highlight Show
        return Event(event_data['eventId'], event_data['date'],
                     event_data['title'],
                     Competition.create_competition(
                         event_data['competition']),
                     event_data['fixture'], event_data['season'],
                     Playlist.create_playlist(event_data['playlists']))


class Match(Event):
    """
    Represents a football match - a meeting between two teams.
    """

    def __init__(self, event_id, date, title, competition, fixture, season,
                 playlists, home_team, away_team):
        super(Match, self).__init__(event_id, date, title, competition, fixture,
                                    season, playlists)
        self.home_team = home_team
        self.away_team = away_team
