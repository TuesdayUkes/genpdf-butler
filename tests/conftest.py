"""Shared test fixtures and configuration."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_chopro_content():
    """Sample chopro file content for testing."""
    return [
        "{title: Test Song}\n",
        "{artist: Test Artist}\n",
        "\n",
        "[G]This is a test [C]song\n",
        "With some &blue: colored text\n",
        "And normal text too\n",
        "More &blue text here\n",
        "Back to normal\n"
    ]


@pytest.fixture
def sample_cho_content():
    """Sample .cho file content for testing."""
    return [
        "Test Song\n",
        "Test Artist\n",
        "\n",
        "G           C\n",
        "This is a test song\n",
        "With normal text\n"
    ]


@pytest.fixture
def create_test_files(temp_dir):
    """Factory fixture to create test files in temp directory."""
    def _create_files(files_dict):
        """Create files with given content.
        
        Args:
            files_dict: Dict mapping filename to content list
            
        Returns:
            List of Path objects for created files
        """
        created_files = []
        for filename, content in files_dict.items():
            file_path = temp_dir / filename
            file_path.write_text(''.join(content), encoding='utf-8')
            created_files.append(file_path)
        return created_files
    
    return _create_files
