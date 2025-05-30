import subprocess
import unittest
import os

class TestLibraryVersionCompatibility(unittest.TestCase):
    def setUp(self):
        self.config_path = "test_config.json"
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"{self.config_path} does not exist!")

        # Use python entrypoint if tap-fullstory isn't in PATH
        self.tap_command = ["tap-fullstory"]

    def test_discovery_works_with_updated_libraries(self):
        """Run the tap with --discover to ensure schema discovery works"""
        result = subprocess.run(
            self.tap_command + ["--config", self.config_path, "--discover"],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Tap discovery failed:\n{result.stderr}")
        self.assertIn('"type": "SCHEMA"', result.stdout, "No schema found in discovery output")

    def test_sync_runs_with_updated_libraries(self):
        """Run the tap for a short sync to check no runtime errors"""
        result = subprocess.run(
            self.tap_command + ["--config", self.config_path],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Tap sync failed:\n{result.stderr}")
        self.assertIn('"type": "RECORD"', result.stdout, "No records emitted in sync output")
