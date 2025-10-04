# Test Suite for genpdf-butler

## Overview

This test suite provides comprehensive coverage for the genpdf-butler package with **97% code coverage** across all modules.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared fixtures and configuration
├── test_genpdf.py           # Tests for GenPDF module
├── test_main.py             # Tests for __main__ module  
├── test_patchtextcolor.py   # Tests for PatchTextColor module
└── pytest.ini              # pytest configuration
```

## Test Coverage

| Module | Coverage | Lines Tested | Missing Lines |
|--------|----------|--------------|---------------|
| GenPDF.py | 100% | 18/18 | None |
| PatchTextColor.py | 97% | 29/30 | Line 36 |
| __main__.py | 97% | 29/30 | Line 57 |
| __init__.py | 100% | 0/0 | None |
| **TOTAL** | **97%** | **76/78** | **2 lines** |

## Test Categories

### GenPDF Module Tests (`test_genpdf.py`)
- ✅ chordpro settings configuration
- ✅ File extension handling (case insensitive)
- ✅ Single file processing (.chopro and .cho)
- ✅ Directory processing with mixed file types
- ✅ Parameter variations (pagesize, showchords)
- ✅ Error handling for nonexistent files
- ✅ Unsupported file extension filtering

### PatchTextColor Module Tests (`test_patchtextcolor.py`)
- ✅ File collection (.chopro and .cho files)
- ✅ OnSong color code detection and replacement
- ✅ Multiple color sections in single file
- ✅ Files ending with color sections
- ✅ Files without color codes (unchanged)
- ✅ Exception handling during file processing
- ✅ Regex pattern matching validation

### Main Module Tests (`test_main.py`)
- ✅ Clean repository workflow
- ✅ Dirty repository detection and blocking
- ✅ Default argument handling
- ✅ Custom argument parsing
- ✅ Git repository initialization
- ✅ File filtering (only .chopro/.cho files considered)
- ✅ Error message output to stderr
- ✅ Git restore operations

## Key Testing Insights

### Git Behavior Understanding
The tests correctly account for the application's git workflow:

1. **PatchTextColor.PatchColors()** - Temporarily modifies .chopro/.cho files
2. **GenPDF.createPDFs()** - Processes the modified files to generate PDFs
3. **repo.git.restore()** - Reverts all changes back to original state

The tests focus on the **intermediate state** after PatchColors() but before git restore, which is the correct approach for unit testing these functions in isolation.

### Color Processing Logic
Tests validate the complex color processing logic:
- `&blue:` or `&blue` triggers color mode ON
- Lines without color codes turn color mode OFF
- Proper insertion of `{textcolour: blue}` and `{textcolour}` markers
- Correct removal of OnSong color codes from text

## Running Tests

### All Tests
```bash
python -m pytest tests/ -v
```

### With Coverage
```bash
python -m pytest tests/ --cov=src/genpdf_butler --cov-report=term-missing
```

### Specific Module
```bash
python -m pytest tests/test_genpdf.py -v
```

### CI Integration
Tests are designed to work with the CI workflow and include:
- Proper mocking of external dependencies (subprocess, git operations)
- Temporary file handling that doesn't interfere with git
- Cross-platform compatibility (Windows, macOS, Linux)

## Mock Strategy

The tests use comprehensive mocking to:
- **Avoid side effects**: Don't create permanent files or run actual chordpro commands
- **Test in isolation**: Each function tested independently
- **Handle external dependencies**: Git operations, subprocess calls, file system operations
- **Provide deterministic results**: Consistent test outcomes across environments

## Fixtures and Utilities

- `temp_dir`: Creates temporary directories for file operations
- `sample_chopro_content`: Standard test content for .chopro files
- `sample_cho_content`: Standard test content for .cho files  
- `create_test_files`: Factory for creating test files with specific content

## Future Improvements

To reach 100% coverage, add tests for:
1. Line 36 in PatchTextColor.py (likely an edge case in exception handling)
2. Line 57 in __main__.py (likely the final if __name__ == "__main__" check)

## Integration with CI/CD

These tests are configured to run in the GitHub Actions workflows:
- **CI workflow**: Runs tests on multiple Python versions and platforms
- **Build workflow**: Validates tests before building and publishing
- **Quality gates**: Tests must pass before deployment to PyPI
