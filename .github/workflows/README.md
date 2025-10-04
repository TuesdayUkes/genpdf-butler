# GitHub Workflows Setup

This directory contains GitHub Actions workflows for the genpdf-butler project.

## Workflows

### 1. `build-and-publish.yml`
**Main build and publish workflow**

- **Triggers**: Push to main, tags, pull requests, and releases
- **Jobs**:
  - `test`: Runs tests on Python 3.11 and 3.12
  - `build`: Creates distribution packages
  - `publish-test`: Publishes to Test PyPI on main branch pushes
  - `publish-pypi`: Publishes to PyPI on GitHub releases

### 2. `ci.yml`
**Continuous Integration workflow**

- **Triggers**: Push and pull requests to main/develop branches
- **Jobs**:
  - `lint-and-format`: Code quality checks (black, flake8, isort, mypy)
  - `test`: Cross-platform testing on Ubuntu, Windows, macOS

### 3. `release.yml`
**Manual release workflow**

- **Triggers**: Manual workflow dispatch
- **Features**:
  - Updates version in pyproject.toml
  - Creates git tag
  - Creates GitHub release with built packages

## Setup Instructions

### 1. PyPI API Tokens

To enable publishing to PyPI, you need to set up API tokens:

1. **PyPI Token**:
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token
   - Add it as a repository secret named `PYPI_API_TOKEN`

2. **Test PyPI Token**:
   - Go to https://test.pypi.org/manage/account/token/
   - Create a new API token
   - Add it as a repository secret named `TEST_PYPI_API_TOKEN`

### 2. Repository Secrets

Go to your repository settings → Secrets and variables → Actions, and add:

- `PYPI_API_TOKEN`: Your PyPI API token
- `TEST_PYPI_API_TOKEN`: Your Test PyPI API token

### 3. Development Dependencies (Optional)

For local development with the same tools used in CI:

```bash
pip install black flake8 isort mypy pytest pytest-cov
```

## Usage

### Publishing a Release

1. **Automatic on GitHub Release**:
   - Create a release on GitHub
   - The workflow will automatically build and publish to PyPI

2. **Manual Release**:
   - Go to Actions → Release workflow
   - Click "Run workflow"
   - Enter the version number (e.g., "0.0.32")
   - Select release type

### Testing

- **On every push/PR**: CI workflow runs automatically
- **Before PyPI**: Test PyPI publishing happens on main branch pushes

### Monitoring

- Check the Actions tab for workflow status
- Failed workflows will be reported via GitHub notifications
- Build artifacts are available for download from successful builds

## Workflow Features

- **Multi-platform testing**: Ubuntu, Windows, macOS
- **Multiple Python versions**: 3.11, 3.12
- **Code quality**: Automated formatting and linting checks
- **Safe publishing**: Test PyPI before production
- **Artifact storage**: Built packages saved for manual inspection
- **Version management**: Automated version bumping for releases
