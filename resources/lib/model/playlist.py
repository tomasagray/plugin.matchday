#!/usr/bin/env python3
"""
Represents video playlist set - master playlist + variant playlists.
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
from urllib.error import HTTPError

import requests
import xbmc

from lib.kodiutils import notification


def parse_video_resource(resource):
    variant = {
        'channel': resource['channel'] if 'channel' in resource else '',
        'source': resource['source'] if 'source' in resource else '',
        'languages': resource['languages'] if 'languages' in resource else '',
        'resolution': resource['resolution'] if 'resolution' in resource else '',
        'media-container': resource['mediaContainer'] if 'mediaContainer' in resource else '',
        'bitrate': resource['bitrate'] if 'bitrate' in resource else '',
        'framerate': resource['frameRate'] if 'frameRate' in resource else '',
        'video-codec': resource['videoCodec'] if 'videoCodec' in resource else '',
        'audio-codec': resource['audioCodec'] if 'audioCodec' in resource else '',
        'direct-stream-url': resource['_links']['stream']['href'] if '_links' in resource else '',
    }
    return variant


def sort_playlist_variants(e):
    return e['resolution']


def download_playlist(uri):
    """
    Fetch a remote playlist
    """
    try:
        response = requests.get(uri)
        playlist = json.loads(response.text)
        xbmc.log("Got VideoPlaylist resource: {}".format(playlist), 1)
        return playlist
    except HTTPError as http_error:
        notification("Could not retrieve playlist", f'Location: {uri} \n {http_error}')
    except Exception as err:
        notification("Error", f'Error getting playlist from {uri}: {err}')


class Playlist:
    """
    Represents video playlist (m3u8)
    """

    def __init__(self, playlist_dict):
        self.preferred_playlist_url = playlist_dict['_links']['preferred']['href']
        self.variants = []
        # Parse each video resource
        for resource in playlist_dict['_embedded']['video-sources']:
            self.variants.append(parse_video_resource(resource))
        # Sort variants
        self.variants.sort(key=sort_playlist_variants)

    def get_playlist_resource(self):
        """
        Gets the highest-quality and/or most relevant variant playlist.
        :return: The URL of the "best" variant
        """
        url = self.preferred_playlist_url
        playlist = download_playlist(url)
        return playlist

    @staticmethod
    def create_playlist(playlist_data):
        """
        Factory method to create a playlist, including master (default) playlist
        and variants.
        :param: playlist_data: The playlist data (JSON)
        :return: A Playlist object
        """
        return Playlist(playlist_data)
