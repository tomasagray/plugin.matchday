#!/usr/bin/env python3
"""
Football team
"""


#  Copyright (c) 2022
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

class Team:
    """
    Represents a football team
    """

    def __init__(self, team_id, name, links):
        self.team_id = team_id
        self.name = name
        self.links = links

    @staticmethod
    def create_team(team_data):
        """
        Factory method to create a Team object from JSON data
        :param team_data: The JSON data representing a team
        :return: a Team object
        """
        return Team(team_data['id'], team_data['name']['name'], team_data['_links'])

    def __str__(self):
        return self.name
