# GitHub Workflows Structure

## Overview

The genpdf-butler project now uses a **three-workflow approach** for better separation of concerns:

## 🔧 Workflows

### 1. `ci.yml` - Continuous Integration
**Triggers:** Push and PR to main/develop branches
**Purpose:** Code quality and testing

- ✅ Code formatting (Black)
- ✅ Linting (flake8) 
- ✅ Import sorting (isort)
- ✅ Type checking (mypy)
- ✅ Unit tests (pytest)
- ✅ Multi-platform testing (Ubuntu, Windows, macOS)
- ✅ Coverage reporting

### 2. `test-pypi-publish.yml` - Test Publishing
**Triggers:** 
- Push to main branch (automatic)
- Manual workflow dispatch (with optional version override)

**Purpose:** Validate package builds and test publishing

- ✅ Run full test suite
- ✅ Build packages
- ✅ Publish to Test PyPI (`skip-existing: true`)
- ✅ Test installation from Test PyPI
- ✅ CLI functionality validation

### 3. `build-and-publish.yml` - Production Publishing  
**Triggers:**
- GitHub release published (automatic)
- Manual workflow dispatch (with confirmation required)

**Purpose:** Production releases to PyPI

- ✅ Run tests
- ✅ Build packages
- ✅ Publish to production PyPI
- ✅ Safety confirmation for manual runs

### 4. `release.yml` - Release Management
**Triggers:** Manual workflow dispatch

**Purpose:** Complete release process

- ✅ Version bumping in pyproject.toml
- ✅ Git tagging and commits
- ✅ GitHub release creation
- ✅ Automated package building

## 🚀 Recommended Release Process

### For Development/Testing:
1. **Push to main** → `test-pypi-publish.yml` runs automatically
2. **Test the package** from Test PyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ genpdf-butler
   ```

### For Production Release:
1. **Use release workflow** → Go to Actions → Release → Run workflow
2. **Specify new version** (e.g., "0.0.33") 
3. **Creates GitHub release** → Automatically triggers `build-and-publish.yml`
4. **Package published** to production PyPI

### Emergency Production Release:
1. **Manual production publish** → Go to Actions → Build and Publish to PyPI
2. **Type "publish"** to confirm
3. **Package published** directly to production PyPI

## ✅ Benefits

- **🔄 Continuous validation**: Every push tests on Test PyPI
- **🛡️ Safe releases**: Test before production
- **🎯 Clear separation**: Development vs. production workflows  
- **⚡ No version conflicts**: `skip-existing` prevents failures
- **🔐 Safety checks**: Confirmation required for manual production releases
- **📊 Full coverage**: All platforms and Python versions tested

## 🔧 Configuration Required

Make sure these secrets are set in your GitHub repository:
- `TEST_PYPI_API_TOKEN` - For Test PyPI publishing
- `PYPI_API_TOKEN` - For production PyPI publishing
