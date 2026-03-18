#!/usr/bin/env python3
"""
Unit tests for PantheonOS realm isolation framework.
"""

import os
import sys
import json
import time
import shutil
import tempfile
from pathlib import Path
from unittest import TestCase, main

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from realms import IsolatedRealm, RealmState
from realms.isolation import (
    RealmMetadata,
    PortAllocator,
    REALMS_BASE,
    WORKTREES_BASE,
    cleanup_all_realms,
)


class TestPortAllocator(TestCase):
    """Test port allocation."""
    
    def test_allocate_port(self):
        """Test port allocation."""
        allocator = PortAllocator(port_range=(10000, 10005))
        port1 = allocator.allocate("realm1")
        port2 = allocator.allocate("realm2")
        self.assertNotEqual(port1, port2)
        self.assertGreaterEqual(port1, 10000)
        self.assertLessEqual(port1, 10005)
    
    def test_release_port(self):
        """Test port release."""
        allocator = PortAllocator(port_range=(10010, 10015))
        port = allocator.allocate("realm1")
        allocator.release(port)
        # Port should be available again
        new_port = allocator.allocate("realm2")
        self.assertEqual(port, new_port)


class TestRealmMetadata(TestCase):
    """Test realm metadata."""
    
    def test_metadata_serialization(self):
        """Test metadata to/from dict."""
        metadata = RealmMetadata(
            realm_id="test-realm",
            created_at="2024-01-01T00:00:00",
            state=RealmState.RUNNING,
            port=9000,
            worktree_path="/tmp/worktree",
            state_dir="/tmp/state",
            tags=["test"],
        )
        
        data = metadata.to_dict()
        self.assertEqual(data["realm_id"], "test-realm")
        self.assertEqual(data["state"], "running")
        
        restored = RealmMetadata.from_dict(data)
        self.assertEqual(restored.realm_id, metadata.realm_id)
        self.assertEqual(restored.state, metadata.state)


class TestIsolatedRealm(TestCase):
    """Test IsolatedRealm class."""
    
    def setUp(self):
        """Set up test environment."""
        # Clean up any existing test realms
        cleanup_all_realms()
        self.test_realm_id = f"test-realm-{int(time.time())}"
    
    def tearDown(self):
        """Clean up after test."""
        cleanup_all_realms()
    
    def test_create_realm(self):
        """Test realm creation."""
        realm = IsolatedRealm.create(self.test_realm_id)
        
        self.assertEqual(realm.realm_id, self.test_realm_id)
        self.assertEqual(realm.metadata.state, RealmState.CREATED)
        self.assertGreaterEqual(realm.port, 9000)
        self.assertLessEqual(realm.port, 9999)
        
        # Check directories exist
        self.assertTrue(realm.state_dir.exists())
        self.assertTrue(realm.worktree.exists())
        
        # Check metadata file
        metadata_file = realm.state_dir / "metadata.json"
        self.assertTrue(metadata_file.exists())
        
        with open(metadata_file, "r") as f:
            data = json.load(f)
            self.assertEqual(data["realm_id"], self.test_realm_id)
    
    def test_load_realm(self):
        """Test loading existing realm."""
        # Create realm
        realm1 = IsolatedRealm.create(self.test_realm_id)
        
        # Load realm
        realm2 = IsolatedRealm.load(self.test_realm_id)
        
        self.assertEqual(realm1.realm_id, realm2.realm_id)
        self.assertEqual(realm1.port, realm2.port)
    
    def test_boot_and_stop(self):
        """Test booting and stopping a realm."""
        realm = IsolatedRealm.create(self.test_realm_id)
        
        # Boot with echo command
        pid = realm.boot(command=["echo", "test"])
        self.assertIsNotNone(pid)
        self.assertEqual(realm.metadata.state, RealmState.RUNNING)
        
        # Wait for process to complete
        time.sleep(0.5)
        
        # Stop realm
        realm.stop()
        self.assertEqual(realm.metadata.state, RealmState.STOPPED)
    
    def test_teardown(self):
        """Test realm teardown."""
        realm = IsolatedRealm.create(self.test_realm_id)
        
        # Teardown
        realm.teardown(force=True)
        
        # Check directories are removed
        self.assertFalse(realm.state_dir.exists())
        self.assertFalse(realm.worktree.exists())
    
    def test_duplicate_realm_error(self):
        """Test error on duplicate realm creation."""
        IsolatedRealm.create(self.test_realm_id)
        
        with self.assertRaises(ValueError):
            IsolatedRealm.create(self.test_realm_id)
    
    def test_load_nonexistent_realm(self):
        """Test error loading non-existent realm."""
        with self.assertRaises(ValueError):
            IsolatedRealm.load("nonexistent-realm")


class TestRealmLifecycle(TestCase):
    """Test complete realm lifecycle."""
    
    def setUp(self):
        """Set up test environment."""
        cleanup_all_realms()
        self.test_realm_id = f"lifecycle-test-{int(time.time())}"
    
    def tearDown(self):
        """Clean up after test."""
        cleanup_all_realms()
    
    def test_full_lifecycle(self):
        """Test create -> boot -> stop -> teardown."""
        # Create
        realm = IsolatedRealm.create(self.test_realm_id)
        self.assertEqual(realm.metadata.state, RealmState.CREATED)
        
        # Boot
        pid = realm.boot(command=["sleep", "1"])
        self.assertEqual(realm.metadata.state, RealmState.RUNNING)
        
        # Stop
        realm.stop()
        self.assertEqual(realm.metadata.state, RealmState.STOPPED)
        
        # Teardown
        realm.teardown(force=True)
        self.assertEqual(realm.metadata.state, RealmState.TEARDOWN)


if __name__ == "__main__":
    main()