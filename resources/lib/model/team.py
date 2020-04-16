#!/usr/bin/env python3
"""
Football team
"""


class Team:
    """
    Represents a football team
    """
    def __init__(self, team_id, name, abbreviation, links):
        self.team_id = team_id
        self.name = name
        self.abbreviation = abbreviation
        self.links = links

    @staticmethod
    def create_team(team_data):
        """
        Factory method to create a Team object from JSON data
        :param team_data: The JSON data representing a team
        :return: a Team object
        """
        return Team(team_data['id'], team_data['name'],
                    team_data['abbreviation'], team_data['_links'])

    def __str__(self):
        return self.name
