#!/usr/bin/env python3
"""
Represents video playlist set - master playlist + variant playlists.
"""


class Playlist:
    """
    Represents video playlist (m3u8)
    """
    def __init__(self, variants):
        self.variants = variants

    def get_master_url(self):
        """
        Return the master (default) playlist
        :return: The master playlist URL
        """
        self.get_best_variant_url()
        return self.variants['master']['href']

    def get_variant_url(self, variant_index):
        """
        Returns the variants specified by variant_index
        :param variant_index: The index of the desired variants
        :return: The URL of the requested variants playlist
        """
        return self.variants[variant_index]['href']

    @property
    def get_best_variant_url(self):
        """
        Gets the highest-quality and/or most relevant variant playlist.
        :return: The URL of the "best" variant
        """
        # No HD variant found; return first index
        best = self.variants['master']
        # Find & return first match
        for key, variant in self.variants.items():
            lower = key.lower()
            if "1080p" in lower:
                best = variant
                break
            if "1080i" in lower:
                best = variant
                break
            if "720p" in lower:
                best = variant
        return best['href']

    @staticmethod
    def create_playlist(playlist_data):
        """
        Factory method to create a playlist, including master (default) playlist
        and variants.
        :param playlist_data: The playlist data (JSON)
        :return: A Playlist object
        """
        return Playlist(playlist_data['_links'])
