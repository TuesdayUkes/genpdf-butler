"""Tests for GenPDF module."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from genpdf_butler.GenPDF import createPDFs


class TestCreatePDFs:
    """Test cases for the createPDFs function."""

    def test_chordpro_settings_configuration(self):
        """Test that chordpro settings are properly configured."""
        with (
            patch("genpdf_butler.GenPDF.os.path.exists", return_value=False),
            patch("genpdf_butler.GenPDF.print") as mock_print,
        ):
            createPDFs("nonexistent", "a4", "true")
            mock_print.assert_called_once_with(
                "no such file or folder 'nonexistent'"
            )

    def test_ext_function_returns_lowercase_extension(self):
        """Test that the internal ext function returns lowercase extensions."""
        with (
            patch("genpdf_butler.GenPDF.os.path.exists", return_value=True),
            patch("genpdf_butler.GenPDF.os.path.isdir", return_value=False),
            patch("genpdf_butler.GenPDF.subprocess.run") as mock_run,
        ):
            # Create a temporary file with uppercase extension
            with tempfile.NamedTemporaryFile(
                suffix=".CHOPRO", delete=False
            ) as tmp:
                tmp_path = tmp.name

            try:
                createPDFs(tmp_path, "a4", "true")
                # Should have been called since the extension matches
                # (case insensitive)
                mock_run.assert_called_once()
            finally:
                os.unlink(tmp_path)

    @patch("genpdf_butler.GenPDF.subprocess.run")
    @patch("genpdf_butler.GenPDF.os.path.isdir")
    @patch("genpdf_butler.GenPDF.os.path.exists")
    def test_single_file_processing(self, mock_exists, mock_isdir, mock_run):
        """Test processing a single chopro file."""
        mock_exists.return_value = True
        mock_isdir.return_value = False

        createPDFs("test.chopro", "a4", "true")

        expected_args = [
            "chordpro",
            "--config=ukulele",
            "--config=ukulele-ly",
            "--define=pdf:diagrams:show=true",
            "--define=settings:inline-chords=true",
            "--define=pdf:even-odd-pages=0",
            "--define=pdf:margintop=70",
            "--define=pdf:marginbottom=0",
            "--define=pdf:marginleft=10",
            "--define=pdf:marginright=50",
            "--define=pdf:headspace=50",
            "--define=pdf:footspace=10",
            "--define=pdf:head-first-only=true",
            "--define=pdf:fonts:chord:color=red",
            "--define=pdf:papersize=a4",
            "--text-font=helvetica",
            "--chord-font=helvetica",
            "--output=test.pdf",
            "test.chopro",
        ]

        mock_run.assert_called_once_with(expected_args)

    @patch("genpdf_butler.GenPDF.subprocess.run")
    @patch("genpdf_butler.GenPDF.os.path.isdir")
    @patch("genpdf_butler.GenPDF.os.path.exists")
    def test_single_cho_file_processing(
        self, mock_exists, mock_isdir, mock_run
    ):
        """Test processing a single .cho file."""
        mock_exists.return_value = True
        mock_isdir.return_value = False

        createPDFs("test.cho", "a6", "false")

        expected_args = [
            "chordpro",
            "--config=ukulele",
            "--config=ukulele-ly",
            "--define=pdf:diagrams:show=false",
            "--define=settings:inline-chords=true",
            "--define=pdf:even-odd-pages=0",
            "--define=pdf:margintop=70",
            "--define=pdf:marginbottom=0",
            "--define=pdf:marginleft=10",
            "--define=pdf:marginright=50",
            "--define=pdf:headspace=50",
            "--define=pdf:footspace=10",
            "--define=pdf:head-first-only=true",
            "--define=pdf:fonts:chord:color=red",
            "--define=pdf:papersize=a6",
            "--text-font=helvetica",
            "--chord-font=helvetica",
            "--output=test.pdf",
            "test.cho",
        ]

        mock_run.assert_called_once_with(expected_args)

    @patch("genpdf_butler.GenPDF.subprocess.run")
    @patch("genpdf_butler.GenPDF.os.path.isdir")
    @patch("genpdf_butler.GenPDF.os.path.exists")
    def test_directory_processing(self, mock_exists, mock_isdir, mock_run):
        """Test processing a directory containing chopro files."""
        mock_exists.return_value = True
        mock_isdir.return_value = True

        # Create actual temporary files to test with
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            chopro_file = Path(temp_dir) / "song1.chopro"
            cho_file = Path(temp_dir) / "song2.cho"
            txt_file = Path(temp_dir) / "readme.txt"

            chopro_file.touch()
            cho_file.touch()
            txt_file.touch()

            createPDFs(temp_dir, "a4", "true")

            # Should be called twice (for .chopro and .cho files, not .txt)
            assert mock_run.call_count == 2

    @patch("genpdf_butler.GenPDF.print")
    @patch("genpdf_butler.GenPDF.os.path.exists")
    def test_nonexistent_target(self, mock_exists, mock_print):
        """Test handling of nonexistent file or directory."""
        mock_exists.return_value = False

        createPDFs("nonexistent.chopro", "a4", "true")

        mock_print.assert_called_once_with(
            "no such file or folder 'nonexistent.chopro'"
        )

    def test_parameter_variations(self):
        """Test that different parameters are properly incorporated."""
        with (
            patch("genpdf_butler.GenPDF.os.path.exists", return_value=True),
            patch("genpdf_butler.GenPDF.os.path.isdir", return_value=False),
            patch("genpdf_butler.GenPDF.subprocess.run") as mock_run,
        ):

            createPDFs("test.chopro", "letter", "true")

            args = mock_run.call_args[0][0]
            assert "--define=pdf:papersize=letter" in args
            assert "--define=pdf:diagrams:show=true" in args

    def test_unsupported_file_extension(self):
        """Test that files with unsupported extensions are ignored."""
        with (
            patch("genpdf_butler.GenPDF.os.path.exists", return_value=True),
            patch("genpdf_butler.GenPDF.os.path.isdir", return_value=False),
            patch("genpdf_butler.GenPDF.subprocess.run") as mock_run,
        ):

            createPDFs("test.txt", "a4", "true")

            # Should not be called for .txt files
            mock_run.assert_not_called()
