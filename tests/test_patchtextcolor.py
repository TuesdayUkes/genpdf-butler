"""Tests for PatchTextColor module."""

import tempfile
from pathlib import Path

from genpdf_butler.PatchTextColor import PatchColors


class TestPatchColors:
    """Test cases for the PatchColors function."""

    def test_no_files_found_directory(self):
        """Test behavior when no chopro/cho files are found in directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Empty directory should not cause errors
            PatchColors(temp_dir)

    def test_directory_file_collection(self):
        """Test that files are collected from a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            chopro_file = Path(temp_dir) / "test1.chopro"
            cho_file = Path(temp_dir) / "test2.cho"

            chopro_file.write_text("test content", encoding="utf-8")
            cho_file.write_text("test content", encoding="utf-8")

            # Function should process the directory without errors
            PatchColors(temp_dir)

    def test_actual_file_modification_and_restore(self):
        """Test actual file processing showing temporary nature."""
        test_content = "Normal line\n&blue: This is blue text\nMore text\n"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".chopro", delete=False, encoding="utf-8"
        ) as tmp_file:
            tmp_file.write(test_content)
            tmp_file_path = tmp_file.name

        try:
            # Store original content
            original_content = Path(tmp_file_path).read_text(encoding="utf-8")

            # Process the file (this actually modifies it)
            PatchColors(tmp_file_path)

            # Read the modified content
            modified_content = Path(tmp_file_path).read_text(encoding="utf-8")

            # Verify modifications occurred
            assert modified_content != original_content
            assert "{textcolour: blue}" in modified_content
            assert "&blue:" not in modified_content

            # Simulate git restore by restoring original content
            Path(tmp_file_path).write_text(original_content, encoding="utf-8")

            # Verify restoration
            restored_content = Path(tmp_file_path).read_text(encoding="utf-8")
            assert restored_content == original_content
            assert "&blue:" in restored_content

        finally:
            Path(tmp_file_path).unlink()
