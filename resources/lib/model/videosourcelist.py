#!/usr/bin/env python3
"""
Represents video playlist set - master playlist + variant playlists.
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

from resources.lib.kodiutils import notification
from resources.lib.model.video_source import VideoSource


class VideoSourceList:
    """
    Represents video playlist (m3u8)
    """

    def __init__(self, source_dict):
        self.preferred_playlist_url = source_dict['_links']['preferred']['href']
        self.variants = []
        # Parse each video resource
        for resource in source_dict['_embedded']['video-sources']:
            self.variants.append(VideoSource.parse_video_resource(resource))
        # Sort variants
        self.variants.sort(key=self.sort_playlist_variants, reverse=True)

    def __str__(self):
        variant_count = len(self.variants)
        return "Video VideoSourceList (variants: {})".format(variant_count)

    def get_preferred_source(self):
        """
        Gets the highest-quality and/or most relevant variant video source.
        :return: The "best" variant
        """
        url = self.preferred_playlist_url
        return self.download_video_source(url)

    def get_variant_source(self, idx=0):
        """
        Retrieves the selected variant video source from the server
        :return: The selected video source (list of URLs)
        """
        selected_source = self.variants[idx]
        return self.download_video_source(selected_source.stream_url)

    @staticmethod
    def create_video_source_list(source_data):
        """
        Factory method to create a playlist, including master (default) playlist
        and variants.
        :param: source_data: The playlist data (JSON)
        :return: A VideoSourceList object
        """
        return VideoSourceList(source_data)

    @staticmethod
    def sort_playlist_variants(source):
        return source.resolution

    @staticmethod
    def download_video_source(url):
        """
        Fetch a video source from the server
        """
        try:
            response = requests.get(url)
            video_source = json.loads(response.text)
            xbmc.log("Got VideoPlaylist resource: {}".format(video_source), xbmc.LOGINFO)
            return video_source
        except HTTPError as http_error:
            notification("Could not retrieve playlist", f'Location: {url} \n {http_error}')
        except Exception as err:
            notification("Error", f'Error getting playlist from {url}: {err}')
