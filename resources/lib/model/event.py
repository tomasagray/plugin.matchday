#!/usr/bin/env python3
"""
Contains all event representations: the abstract event class, and its
concretions, Match and Highlight Show.
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

from datetime import datetime

import dateutil.parser

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
    :param: event_data: The Event data (JSON)
    :return: An Event object or subtype
    """
    # Format date
    try:
      date = dateutil.parser.parse("{}".format(event_data['date']))
    except TypeError:
      date = datetime.now()

    # Extract data
    event_id = event_data.get('eventId')
    title = event_data.get('title')
    comp = event_data.get('competition')
    # Create a Competition object
    competition = Competition.create_competition(comp)
    fixture = event_data.get('fixture')
    season = event_data.get('season')
    links = event_data.get('_links')

    # Check for the presence of a team
    if 'homeTeam' in list(event_data.keys()):
      # It's a Match event
      home_team = Team.create_team(event_data['homeTeam'])
      away_team = Team.create_team(event_data['awayTeam'])
      return Match(event_id, date, title, competition, fixture, season,
                   links, home_team, away_team)

    # It's a Highlight Show
    return Event(event_id, date, title, competition, fixture, season, links)


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
