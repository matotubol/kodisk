import unittest
from unittest.mock import patch

# Import environment setup from other tests
import tests.test_sc_api  # noqa: F401
import sys

# Prepare argv for modules that read sys.argv at import time
sys.argv = ['plugin', '1', '']
# Extend fake xbmcgui module with attributes required for import
fake_xbmcgui = sys.modules.get('xbmcgui')
fake_xbmcgui.NOTIFICATION_INFO = 0
fake_xbmcgui.INPUT_ALPHANUM = 0
fake_xbmcgui.INPUT_TYPE_TEXT = 0
fake_xbmcgui.INPUT_NUMERIC = 0
fake_xbmcgui.Dialog = type('Dialog', (), {})
fake_xbmcgui.DialogProgressBG = type('DialogProgressBG', (), {})
fake_xbmcgui.DialogProgress = type('DialogProgress', (), {})
fake_xbmcgui.ListItem = type('ListItem', (), {})

fake_xbmc = sys.modules.get('xbmc')
fake_xbmc.Player = type('Player', (), {})

from resources.lib.streamcinema import Scinema
from resources.lib.constants import SC

class CmdWhitelistTest(unittest.TestCase):
    def setUp(self):
        self.sc = Scinema()
        self.sc.args = {}

    def test_allowed_command_executes(self):
        self.sc.args = {SC.ITEM_ACTION: SC.ACTION_CMD, 'url': 'cmd://Action(Back)'}
        with patch('resources.lib.streamcinema.exec_build_in') as mock_exec:
            self.sc.action_cmd()
            mock_exec.assert_called_once_with('Action(Back)')
            self.assertTrue(self.sc.send_end)

    def test_blocked_command_ignored(self):
        self.sc.args = {SC.ITEM_ACTION: SC.ACTION_CMD, 'url': 'cmd://System.Exec(bad)'}
        with patch('resources.lib.streamcinema.exec_build_in') as mock_exec, \
             patch('resources.lib.streamcinema.warning') as mock_warn:
            self.sc.action_cmd()
            mock_exec.assert_not_called()
            mock_warn.assert_called()

if __name__ == '__main__':
    unittest.main()
