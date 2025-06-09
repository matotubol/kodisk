import unittest
import datetime

# Setup environment
import tests.test_sc_api  # noqa: F401

from resources.lib.common.cache import SimpleCache

class CacheCleanupIsoTest(unittest.TestCase):
    def setUp(self):
        self.cache = SimpleCache()

    def test_property_initialized_iso(self):
        win = self.cache._win
        # clear property
        win.clearProperty("simplecache.clean.lastexecuted")
        self.cache.check_cleanup()
        val = win.getProperty("simplecache.clean.lastexecuted")
        self.assertRegex(val, r"\d{4}-\d{2}-\d{2}T")

    def test_old_repr_string_handled(self):
        win = self.cache._win
        old = repr(datetime.datetime(2020, 1, 1))
        win.setProperty("simplecache.clean.lastexecuted", old)
        # Should not raise
        self.cache.check_cleanup()
        new_val = win.getProperty("simplecache.clean.lastexecuted")
        self.assertRegex(new_val, r"\d{4}-\d{2}-\d{2}T")

if __name__ == '__main__':
    unittest.main()
