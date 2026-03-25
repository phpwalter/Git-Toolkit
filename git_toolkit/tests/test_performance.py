import unittest
import time
import os
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch
from git_toolkit.logging import set_cache, get_cache, clear_cache, CACHE_DIR
from git_toolkit.git_wrapper import get_repo_status, get_repo_stats
from git_toolkit.config import Repository

class TestPerformance(unittest.TestCase):
    def setUp(self):
        # Ensure a clean cache directory for each test
        if CACHE_DIR.exists():
            shutil.rmtree(CACHE_DIR)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        # Clean up
        if CACHE_DIR.exists():
            shutil.rmtree(CACHE_DIR)

    def test_cache_set_get(self):
        set_cache("test_key", {"data": "value"}, ttl=10)
        data = get_cache("test_key")
        self.assertEqual(data, {"data": "value"})

    def test_cache_expiration(self):
        set_cache("expired_key", {"data": "old"}, ttl=-1) # Already expired
        data = get_cache("expired_key")
        self.assertIsNone(data)

    def test_clear_cache(self):
        set_cache("key1", "val1")
        set_cache("key2", "val2")
        clear_cache()
        self.assertIsNone(get_cache("key1"))
        self.assertIsNone(get_cache("key2"))

    @patch('git_toolkit.git_wrapper.Repo')
    def test_get_repo_status_caching(self, mock_repo):
        # Mocking Repo to avoid actual git operations
        mock_repo_instance = MagicMock()
        mock_repo_instance.active_branch.name = "main"
        mock_repo_instance.is_dirty.return_value = False
        mock_repo.return_value = mock_repo_instance
        
        repo_config = Repository(name="test-repo", path="fake/path", url="http://fake.url")
        
        # Mock path existence
        with patch('git_toolkit.git_wrapper.Path.exists', return_value=True):
            # First call - should hit mock_repo
            status1 = get_repo_status(repo_config)
            self.assertEqual(status1["branch"], "main")
            mock_repo.assert_called_once()
            
            # Second call - should hit cache
            mock_repo.reset_mock()
            status2 = get_repo_status(repo_config)
            self.assertEqual(status2["branch"], "main")
            mock_repo.assert_not_called()

    @patch('git_toolkit.git_wrapper.Repo')
    def test_get_repo_stats_caching(self, mock_repo):
        mock_repo_instance = MagicMock()
        mock_repo_instance.active_branch.name = "main"
        mock_repo_instance.iter_commits.return_value = [MagicMock(), MagicMock()] # 2 commits
        mock_repo.return_value = mock_repo_instance
        
        repo_config = Repository(name="test-stats-repo", path="fake/path", url="http://fake.url")
        
        with patch('git_toolkit.git_wrapper.Path.exists', return_value=True):
            # First call
            stats1 = get_repo_stats(repo_config)
            self.assertEqual(stats1["commit_count"], 2)
            
            # Second call - should be cached
            with patch('git_toolkit.git_wrapper.Repo') as mock_repo_new:
                stats2 = get_repo_stats(repo_config)
                self.assertEqual(stats2["commit_count"], 2)
                mock_repo_new.assert_not_called()

if __name__ == '__main__':
    unittest.main()
