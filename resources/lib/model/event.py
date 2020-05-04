#!/usr/bin/env python3
"""
Contains all event representations: the abstract event class, and its
concretions, Match and Highlight Show.
"""
from datetime import datetime
import dateutil.parser
import xbmc

from resources.lib.model.competition import Competition
from resources.lib.model.team import Team


class Event(object):
    """
    Represents a sporting event
    """

    def __init__(self, event_id, date, title, competition, fixture, season,
                 links):
        self.event_id = event_id
        self.date = date
        self.title = title
        self.competition = competition
        self.fixture = fixture
        self.season = season
        self.links = links

    def __str__(self):
        return self.title

    @staticmethod
    def create_event(event_data):
        """
        Factory method to create an Event of the appropriate subtype.
        :param event_data: The Event data (JSON)
        :return: An Event object or subtype
        """
        try:
            # Format date
            date = dateutil.parser.parse("{}".format(event_data['date']))
        except TypeError:
            xbmc.log("Date was unparseable; defaulting to NOW", 2)
            date = datetime.now()
        # Check for the presence of a team
        if 'homeTeam' in event_data.keys():
            # It's a Match event
            return Match(event_data['eventId'], date, event_data['title'],
                         Competition.create_competition(event_data['competition']),
                         event_data['fixture'], event_data['season'],
                         event_data['_links'],
                         Team.create_team(event_data['homeTeam']),
                         Team.create_team(event_data['awayTeam']))

        # It's a Highlight Show
        return Event(event_data['eventId'], date, event_data['title'],
                     Competition.create_competition(event_data['competition']),
                     event_data['fixture'], event_data['season'],
                     event_data['_links'])


class Match(Event):
    """
    Represents a football match - a meeting between two teams.
    """

    def __init__(self, event_id, date, title, competition, fixture, season,
                 links, home_team, away_team):
        super(Match, self).__init__(event_id, date, title, competition, fixture,
                                    season, links)
        self.home_team = home_team
        self.away_team = away_team
