import dbus
from time import sleep
import subprocess
import gi
gi.require_version('Gtk', '3.0')

class MediaPlayerMonitor:
    def __init__(self):
        self.session_bus = dbus.SessionBus()
        self.players = {}
        self.current_player = None

        self.title_ = ''
        self.artist = ''
        self._album = ''
        self.psoition = ''
        self.playback_status = ''
        self.art_url = ''
        self.monitor()
        
    def get_players(self):
        for service in self.session_bus.list_names():
            if service.startswith("org.mpris.MediaPlayer2."):
                if service not in self.players:
                    self.players[service] = self.session_bus.get_object(service, "/org/mpris/MediaPlayer2")
        return self.players

    def get_player_properties(self, player):
        try:
            # iface = dbus.Interface(player, 'org.freedesktop.DBus.Properties')
            iface = dbus.Interface(player, 'org.freedesktop.DBus.Properties')
            metadata = iface.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
            playback_status = iface.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
            position = iface.Get('org.mpris.MediaPlayer2.Player', 'Position')
            title = metadata.get('xesam:title', 'Unknown Title')
            artist = ', '.join(metadata.get('xesam:artist', []))
            album = metadata.get('xesam:album', 'Unknown Album')
            art_url = metadata.get('mpris:artUrl', '')

            return {
                'title': title,
                'artist': artist,
                'album': album,
                'art_url': art_url,
                'playback_status': playback_status,
                'position': position // 1_000_000
            }
        except dbus.exceptions.DBusException as e:
            return None


    def update_current_player(self):
        active_found = False
        for service, player in self.players.items():
            properties = self.get_player_properties(player)
            if properties:
                if properties['playback_status'] == 'Playing' or properties['playback_status'] == 'Paused':
                    self.current_player = player
                    active_found = True
                    break
                if not active_found:
                    self.current_player = player
        if not active_found:
            self.current_player = None

    def monitor(self):
        self.get_players()
        self.update_current_player()

        if self.current_player:
            retry = 0
            while retry < 3:
                self.properties = self.get_player_properties(self.current_player)
                if self.properties and self.properties['title'] != 'Unknown Title':
                    break
                else:
                    sleep(0.3)
                    retry += 1

            if self.properties:
                self.title_ = f"{self.properties['title']}"
                self.artist = f"{self.properties['artist']}"
                self._album = f"{self.properties['album']}"
                self.psoition = f"{self.properties['position']}"
                self.playback_status = f"{self.properties['playback_status']}"
                self.art_url = f"{self.properties['art_url']}"
            else:
                self.title_ = ''
                self.artist = ''
                self._album = ''
                self.psoition = ''
                self.playback_status = ''
                self.art_url = ''
        else:
            self.title_ = ''
            self.artist = ''
            self._album = ''
            self.psoition = ''
            self.playback_status = ''
            self.art_url = ''