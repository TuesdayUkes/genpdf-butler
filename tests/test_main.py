"""Tests for __main__ module."""

import os
import sys
from unittest.mock import Mock, patch

from genpdf_butler.__main__ import main


class TestMain:
    """Test cases for the main function."""

    @patch("genpdf_butler.__main__.Repo")
    @patch("genpdf_butler.__main__.GenPDF.createPDFs")
    @patch("genpdf_butler.__main__.PatchTextColor.PatchColors")
    def test_main_with_clean_repo(
        self, mock_patch_colors, mock_create_pdfs, mock_repo
    ):
        """Test main function with a clean repository."""
        # Mock a clean repository
        mock_repo_instance = Mock()
        mock_repo_instance.index.diff.return_value = []
        mock_repo_instance.untracked_files = []
        mock_repo_instance.git.restore = Mock()
        mock_repo.return_value = mock_repo_instance

        # Mock command line arguments
        test_args = [
            "genpdf",
            "test_dir",
            "--pagesize",
            "a4",
            "--showchords",
            "true",
        ]

        with patch.object(sys, "argv", test_args):
            main()

            # Verify that the processing functions were called
            mock_patch_colors.assert_called_once()
            mock_create_pdfs.assert_called_once_with("test_dir", "a4", "true")

            # Verify git restore was called for both file types
            mock_repo_instance.git.restore.assert_any_call("*.chopro")
            mock_repo_instance.git.restore.assert_any_call("*.cho")

    @patch("genpdf_butler.__main__.Repo")
    @patch("genpdf_butler.__main__.GenPDF.createPDFs")
    @patch("genpdf_butler.__main__.PatchTextColor.PatchColors")
    @patch("builtins.print")
    def test_main_with_dirty_repo(
        self, mock_print, mock_patch_colors, mock_create_pdfs, mock_repo
    ):
        """Test main function with modified chopro files in repository."""
        # Mock a repository with dirty chopro files
        mock_repo_instance = Mock()
        mock_diff_item = Mock()
        mock_diff_item.a_path = "song.chopro"
        mock_repo_instance.index.diff.return_value = [mock_diff_item]
        mock_repo_instance.untracked_files = ["new_song.cho"]
        mock_repo.return_value = mock_repo_instance

        test_args = ["genpdf", "test_dir"]

        with patch.object(sys, "argv", test_args):
            main()

            # Verify that processing functions were NOT called
            mock_patch_colors.assert_not_called()
            mock_create_pdfs.assert_not_called()

            # Verify error messages were printed
            mock_print.assert_called()
            print_calls = [call[0][0] for call in mock_print.call_args_list]

            # Check that appropriate error messages were printed
            error_message_found = any(
                "Cannot operate on a repo" in call for call in print_calls
            )
            assert error_message_found

    @patch("genpdf_butler.__main__.Repo")
    @patch("genpdf_butler.__main__.GenPDF.createPDFs")
    @patch("genpdf_butler.__main__.PatchTextColor.PatchColors")
    def test_main_default_arguments(
        self, mock_patch_colors, mock_create_pdfs, mock_repo
    ):
        """Test main function with default arguments."""
        # Mock a clean repository
        mock_repo_instance = Mock()
        mock_repo_instance.index.diff.return_value = []
        mock_repo_instance.untracked_files = []
        mock_repo_instance.git.restore = Mock()
        mock_repo.return_value = mock_repo_instance

        # Test with minimal arguments (just the script name)
        test_args = ["genpdf"]

        with (
            patch.object(sys, "argv", test_args),
            patch("os.getcwd", return_value="/current/dir"),
        ):

            main()

            # Verify default values were used
            mock_create_pdfs.assert_called_once_with(
                "/current/dir", "a6", "false"
            )

    @patch("genpdf_butler.__main__.Repo")
    @patch("genpdf_butler.__main__.GenPDF.createPDFs")
    @patch("genpdf_butler.__main__.PatchTextColor.PatchColors")
    def test_main_custom_arguments(
        self, mock_patch_colors, mock_create_pdfs, mock_repo
    ):
        """Test main function with custom arguments."""
        # Mock a clean repository
        mock_repo_instance = Mock()
        mock_repo_instance.index.diff.return_value = []
        mock_repo_instance.untracked_files = []
        mock_repo_instance.git.restore = Mock()
        mock_repo.return_value = mock_repo_instance

        test_args = [
            "genpdf",
            "/music/folder",
            "--pagesize",
            "letter",
            "--showchords",
            "true",
        ]

        with patch.object(sys, "argv", test_args):
            main()

            mock_create_pdfs.assert_called_once_with(
                "/music/folder", "letter", "true"
            )

    @patch("genpdf_butler.__main__.Repo")
    @patch("builtins.print")
    def test_stderr_output(self, mock_print, mock_repo):
        """Test that status message is printed to stderr."""
        mock_repo_instance = Mock()
        mock_repo_instance.index.diff.return_value = []
        mock_repo_instance.untracked_files = []
        mock_repo_instance.git.restore = Mock()
        mock_repo.return_value = mock_repo_instance

        test_args = ["genpdf"]

        with (
            patch.object(sys, "argv", test_args),
            patch("genpdf_butler.__main__.PatchTextColor.PatchColors"),
            patch("genpdf_butler.__main__.GenPDF.createPDFs"),
        ):

            main()

            # Check that the status message was printed
            mock_print.assert_called_with(
                "Generating Music List (this takes a few seconds)",
                file=sys.stderr,
            )

    @patch("genpdf_butler.__main__.Repo")
    def test_git_repo_initialization(self, mock_repo):
        """Test that git repository is properly initialized."""
        mock_repo_instance = Mock()
        mock_repo_instance.index.diff.return_value = []
        mock_repo_instance.untracked_files = []
        mock_repo_instance.git.restore = Mock()
        mock_repo.return_value = mock_repo_instance

        test_args = ["genpdf"]

        with (
            patch.object(sys, "argv", test_args),
            patch("genpdf_butler.__main__.PatchTextColor.PatchColors"),
            patch("genpdf_butler.__main__.GenPDF.createPDFs"),
        ):

            main()

            # Verify Repo was initialized with correct parameters
            mock_repo.assert_called_once_with(
                path=".", search_parent_directories=True
            )

    @patch("genpdf_butler.__main__.Repo")
    @patch("builtins.print")
    def test_dirty_files_filtering(self, mock_print, mock_repo):
        """Test that only chopro/cho files are considered for dirty check."""
        # Mock repository with mixed file types
        mock_diff_items = [
            Mock(a_path="song.chopro"),
            Mock(a_path="readme.txt"),
            Mock(a_path="config.cho"),
            Mock(a_path="script.py"),
        ]

        mock_repo_instance = Mock()
        mock_repo_instance.index.diff.return_value = mock_diff_items
        mock_repo_instance.untracked_files = [
            "new_song.chopro",
            "other.md",
            "test.cho",
        ]
        mock_repo.return_value = mock_repo_instance

        test_args = ["genpdf"]

        with patch.object(sys, "argv", test_args):
            main()

            # Should print information about chopro/cho files only
            print_calls = [call[0][0] for call in mock_print.call_args_list]

            # Non chopro/cho files should not be mentioned
            txt_mentioned = any("readme.txt" in call for call in print_calls)
            py_mentioned = any("script.py" in call for call in print_calls)
            md_mentioned = any("other.md" in call for call in print_calls)

            assert not txt_mentioned
            assert not py_mentioned
            assert not md_mentioned

    def test_argument_parser_configuration(self):
        """Test that argument parser is configured correctly."""
        from genpdf_butler.__main__ import main

        # We can't easily test the parser directly, but we can test
        # through sys.argv
        test_cases = [
            (["genpdf"], (os.getcwd(), "a6", "false")),
            (["genpdf", "custom_dir"], ("custom_dir", "a6", "false")),
            (["genpdf", "--pagesize", "a4"], (os.getcwd(), "a4", "false")),
            (["genpdf", "--showchords", "true"], (os.getcwd(), "a6", "true")),
        ]

        for test_args, expected_args in test_cases:
            with (
                patch.object(sys, "argv", test_args),
                patch("genpdf_butler.__main__.Repo") as mock_repo,
                patch("genpdf_butler.__main__.PatchTextColor.PatchColors"),
                patch(
                    "genpdf_butler.__main__.GenPDF.createPDFs"
                ) as mock_create_pdfs,
            ):

                # Mock clean repo
                mock_repo_instance = Mock()
                mock_repo_instance.index.diff.return_value = []
                mock_repo_instance.untracked_files = []
                mock_repo_instance.git.restore = Mock()
                mock_repo.return_value = mock_repo_instance

                main()

                mock_create_pdfs.assert_called_once_with(*expected_args)
