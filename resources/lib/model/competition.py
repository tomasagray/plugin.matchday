#!/usr/bin/env python3
"""
Competition (sports league)
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

class Competition(object):
    """
    Represents a competition_id (sports league)
    """

    def __init__(self, comp_id, name, abbreviation, links):
        self.comp_id = comp_id
        self.name = name
        self.abbreviation = abbreviation
        self.links = links

    @staticmethod
    def create_competition(competition_data):
        """
        Factory method to create a competition_id from JSON data
        :param competition_data: The JSON data representing a competition_id
        :return: a Competition object
        """
        return Competition(competition_data['id'], competition_data['name'],
                           competition_data['abbreviation'],
                           competition_data['_links'])

    def __str__(self):
        return self.name
