import unittest
from unittest.mock import patch
import sys
import types

# Provide fake Kodi modules required for import
fake_xbmc = types.ModuleType('xbmc')
fake_xbmc.getInfoLabel = lambda *args, **kwargs: '18.0'
fake_xbmc.getUserAgent = lambda: ''
fake_xbmc.getSkinDir = lambda: 'default'
fake_xbmc.executebuiltin = lambda *args, **kwargs: None
fake_xbmc.getCondVisibility = lambda *args, **kwargs: False
fake_xbmc.getLanguage = lambda *args, **kwargs: 'en'
fake_xbmc.ISO_639_1 = 1
fake_xbmc.LOGDEBUG = 0
fake_xbmc.LOGINFO = 1
fake_xbmc.LOGWARNING = 2
fake_xbmc.LOGERROR = 3
fake_xbmc.log = lambda *args, **kwargs: None
fake_xbmc.sleep = lambda x: None
class _Monitor:
    def abortRequested(self):
        return False
fake_xbmc.Monitor = _Monitor
sys.modules.setdefault('xbmc', fake_xbmc)

fake_xbmcvfs = types.ModuleType('xbmcvfs')
fake_xbmcvfs.translatePath = lambda x: x
fake_xbmcvfs.validatePath = lambda x: x
fake_xbmcvfs.makeLegalFilename = lambda x: x
fake_xbmcvfs.mkdir = lambda *args, **kwargs: None
fake_xbmcvfs.mkdirs = lambda *args, **kwargs: None
fake_xbmcvfs.exists = lambda *args, **kwargs: False
class _Stat:
    def __init__(self, filename):
        self._size = 0
    def st_size(self):
        return self._size
fake_xbmcvfs.Stat = _Stat
class _File:
    def __init__(self, filename, mode='r'):
        pass
    def read(self, *args, **kwargs):
        return ''
    def write(self, *args, **kwargs):
        pass
    def close(self):
        pass
fake_xbmcvfs.File = _File
sys.modules.setdefault('xbmcvfs', fake_xbmcvfs)

fake_xbmcgui = types.ModuleType('xbmcgui')
class _Window:
    def __init__(self, id=0):
        self.props = {}
    def getProperty(self, key):
        return self.props.get(key, '')
    def setProperty(self, key, value):
        self.props[key] = value
    def clearProperty(self, key):
        self.props.pop(key, None)
class _Monitor:
    def abortRequested(self):
        return False
fake_xbmcgui.Window = _Window
fake_xbmcgui.getCurrentWindowId = lambda: 10000
fake_xbmcgui.WindowXMLDialog = object
sys.modules.setdefault('xbmcgui', fake_xbmcgui)
fake_xbmcplugin = types.ModuleType('xbmcplugin')
for name in [
    'SORT_METHOD_ALBUM', 'SORT_METHOD_ALBUM_IGNORE_THE', 'SORT_METHOD_ARTIST',
    'SORT_METHOD_ARTIST_IGNORE_THE', 'SORT_METHOD_BITRATE',
    'SORT_METHOD_CHANNEL', 'SORT_METHOD_COUNTRY', 'SORT_METHOD_DATE',
    'SORT_METHOD_DATEADDED', 'SORT_METHOD_DATE_TAKEN', 'SORT_METHOD_DRIVE_TYPE',
    'SORT_METHOD_DURATION', 'SORT_METHOD_EPISODE', 'SORT_METHOD_FILE',
    'SORT_METHOD_FULLPATH', 'SORT_METHOD_GENRE', 'SORT_METHOD_LABEL',
    'SORT_METHOD_LABEL_IGNORE_FOLDERS', 'SORT_METHOD_LABEL_IGNORE_THE',
    'SORT_METHOD_LASTPLAYED', 'SORT_METHOD_LISTENERS', 'SORT_METHOD_MPAA_RATING',
    'SORT_METHOD_NONE', 'SORT_METHOD_PLAYCOUNT', 'SORT_METHOD_PLAYLIST_ORDER',
    'SORT_METHOD_PRODUCTIONCODE', 'SORT_METHOD_PROGRAM_COUNT', 'SORT_METHOD_SIZE',
    'SORT_METHOD_SONG_RATING', 'SORT_METHOD_STUDIO', 'SORT_METHOD_STUDIO_IGNORE_THE',
    'SORT_METHOD_TITLE', 'SORT_METHOD_TITLE_IGNORE_THE', 'SORT_METHOD_TRACKNUM',
    'SORT_METHOD_UNSORTED', 'SORT_METHOD_VIDEO_RATING', 'SORT_METHOD_VIDEO_RUNTIME',
    'SORT_METHOD_VIDEO_SORT_TITLE', 'SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE',
    'SORT_METHOD_VIDEO_TITLE', 'SORT_METHOD_VIDEO_USER_RATING', 'SORT_METHOD_VIDEO_YEAR'
]:
    setattr(fake_xbmcplugin, name, 0)
sys.modules.setdefault('xbmcplugin', fake_xbmcplugin)

fake_xbmcaddon = types.ModuleType('xbmcaddon')
class _Addon:
    def __init__(self, id=None):
        self.id = id
    def getAddonInfo(self, info):
        return ''
    def getSetting(self, key):
        return ''
    def getSettingBool(self, key):
        return False
    def getSettingInt(self, key):
        return 0
    def setSetting(self, key, value):
        pass
    def getLocalizedString(self, id):
        return ''
fake_xbmcaddon.Addon = _Addon
sys.modules.setdefault('xbmcaddon', fake_xbmcaddon)

fake_requests = types.ModuleType('requests')
class _HTTPError(Exception):
    def __init__(self, response=None):
        self.response = response
fake_requests.exceptions = types.SimpleNamespace(HTTPError=_HTTPError)
def _dummy_request(*args, **kwargs):
    class _Resp:
        url = ''
        def raise_for_status(self):
            pass
        def json(self):
            return {}
        @property
        def content(self):
            return b''
    return _Resp()
fake_requests.request = _dummy_request
fake_requests.Session = lambda: None
sys.modules.setdefault('requests', fake_requests)

from resources.lib.api.sc import Sc

class DownloadMenuBgTest(unittest.TestCase):
    @patch('threading.Thread')
    def test_download_menu_bg_thread_target(self, mock_thread):
        Sc.download_menu_bg()
        mock_thread.assert_called_once_with(target=Sc.download_menu)
        mock_thread.return_value.start.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
