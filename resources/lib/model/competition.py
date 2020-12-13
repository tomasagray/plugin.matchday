#!/usr/bin/env python3
"""
Competition (sports league)
"""


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
