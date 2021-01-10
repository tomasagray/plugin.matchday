#!/usr/bin/env python3
"""
Represents video playlist set - master playlist + variant playlists.
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

import re

import requests
import xbmc
import xbmcgui


def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url)


def parse_video_resource(resource):
    variant = {
        'channel': resource['channel'],
        'source': resource['source'],
        'languages': resource['languages'],
        'resolution': resource['resolution'],
        'media-container': resource['mediaContainer'],
        'bitrate': resource['bitrate'],
        'framerate': resource['frameRate'],
        'video-codec': resource['videoCodec'],
        'audio-codec': resource['audioCodec'],
        'direct-stream-url': resource['_links']['direct_variant']['href'],
        'transcode-stream-url': resource['_links']['transcode_stream']['href'],
        'transcode-pls-url': resource['_links']['transcode_pls_stream']['href']
    }
    return variant


def sort_playlist_variants(e):
    return e['resolution']


def parse_playlist(uri):
    xbmc_playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    xbmc_playlist.clear()
    playlist = requests.get(uri)
    segments = playlist.text.split("\n")
    for segment in segments:
        if validate_url(segment):
            list_item = xbmcgui.ListItem()
            xbmc_playlist.add(url=segment, listitem=list_item)
    return xbmc_playlist


class Playlist:
    """
    Represents video playlist (m3u8)
    """

    def __init__(self, playlist_dict):
        self.master_playlist_url = playlist_dict['_links']['direct_master']['href']
        self.variants = []
        # Parse each video resource
        for resource in playlist_dict['_embedded']['video-resources']:
            self.variants.append(parse_video_resource(resource))
        # Sort variants
        self.variants.sort(key=sort_playlist_variants)

    def get_xbmc_playlist(self):
        """
        Gets the highest-quality and/or most relevant variant playlist.
        :return: The URL of the "best" variant
        """
        # Find & return first match
        url = self.variants[0]['transcode-stream-url']
        playlist = parse_playlist(url)
        return playlist

    @staticmethod
    def create_playlist(playlist_data):
        """
        Factory method to create a playlist, including master (default) playlist
        and variants.
        :param playlist_data: The playlist data (JSON)
        :return: A Playlist object
        """
        return Playlist(playlist_data)
