#!/usr/bin/env python3
"""
Represents video playlist set - master playlist + variant playlists.
"""


class Playlist:
    """
    Represents video playlist (m3u8)
    """
    def __init__(self, master, variants):
        self.master = master
        self.variants = variants

    def get_master_url(self):
        """
        Return the master (default) playlist
        :return: The master playlist URL
        """
        return self.master['href']

    def get_variant_url(self, variant_index):
        """
        Returns the variants specified by variant_index
        :param variant_index: The index of the desired variants
        :return: The URL of the requested variants playlist
        """
        return self.variants[variant_index]['href']

    @staticmethod
    def create_playlist(playlist_data):
        """
        Factory method to create a playlist, including master (default) playlist
        and variants.
        :param playlist_data: The playlist data (JSON)
        :return: A Playlist object
        """
        master = None
        variants = []
        # Assemble variants
        for key, variant in playlist_data['_links'].items():
            if key == 'master':
                master = variant
            else:
                variants.append(variant)
        return Playlist(master, variants)
