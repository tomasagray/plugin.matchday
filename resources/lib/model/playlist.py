#!/usr/bin/env python3
"""
Represents video playlist set - master playlist + variant playlists.
"""

import json


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
        'direct-stream-url': resource['_links']['direct_stream']['href'],
        'transcode-stream-url': resource['_links']['transcode_stream']['href']
    }
    return variant


def sort_playlist_variants(e):
    return e['resolution']


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

    def get_best_variant_url(self):
        """
        Gets the highest-quality and/or most relevant variant playlist.
        :return: The URL of the "best" variant
        """
        # Find & return first match
        return self.variants[0]['transcode-stream-url']

    @staticmethod
    def create_playlist(playlist_data):
        """
        Factory method to create a playlist, including master (default) playlist
        and variants.
        :param playlist_data: The playlist data (JSON)
        :return: A Playlist object
        """
        playlist_dict = json.loads(playlist_data)
        return Playlist(playlist_dict)
