# OpenID Connect (OIDC) Trusted Publishing Setup

## Overview

Your workflows have been updated to use **OIDC trusted publishing** instead of API tokens. This provides enhanced security by:

- ✅ **No long-lived secrets** stored in GitHub
- ✅ **Automatic token generation** per workflow run
- ✅ **Fine-grained permissions** per repository
- ✅ **Audit trail** of all publishing activities

## 🔧 Required Setup Steps

### 1. Configure PyPI Trusted Publishing

#### For Production PyPI:
1. Go to https://pypi.org/manage/project/genpdf-butler/settings/publishing/
2. Click **"Add a new trusted publisher"**
3. Fill in:
   - **Owner**: `TuesdayUkes`
   - **Repository name**: `genpdf-butler`
   - **Workflow filename**: `build-and-publish.yml`
   - **Environment name**: *(leave empty)*
4. Click **"Add"**

#### For Test PyPI:
1. Go to https://test.pypi.org/manage/project/genpdf-butler/settings/publishing/
2. Click **"Add a new trusted publisher"**
3. Fill in:
   - **Owner**: `TuesdayUkes`
   - **Repository name**: `genpdf-butler`
   - **Workflow filename**: `test-pypi-publish.yml`
   - **Environment name**: *(leave empty)*
4. Click **"Add"**

### 2. Remove Old API Token Secrets (Optional)

Once OIDC is working, you can remove these secrets from your GitHub repository:
- `PYPI_API_TOKEN`
- `TEST_PYPI_API_TOKEN`

Go to **Repository Settings** → **Secrets and variables** → **Actions** → **Delete** the old tokens.

## 📋 What Changed in Workflows

### ✅ Added OIDC Permissions:
```yaml
permissions:
  id-token: write  # IMPORTANT: mandatory for trusted publishing
  contents: read   # or write for release workflow
```

### ✅ Removed API Token References:
- **Before**: `password: ${{ secrets.TEST_PYPI_API_TOKEN }}`
- **After**: *(no password needed - OIDC handles authentication)*

### ✅ Updated PyPI Publish Actions:
All publishing steps now use trusted publishing automatically when OIDC is configured.

## 🔒 Security Benefits

### **Traditional API Tokens**:
❌ Long-lived secrets in GitHub  
❌ Broad permissions across all projects  
❌ Risk if leaked or stolen  
❌ Manual rotation required  

### **OIDC Trusted Publishing**:
✅ No secrets stored in GitHub  
✅ Repository-specific permissions  
✅ Automatic token expiration  
✅ GitHub audit trail  
✅ Can't be used outside GitHub Actions  

## 🚀 How It Works

1. **GitHub Actions** generates a short-lived OIDC token
2. **PyPI** verifies the token against your trusted publisher configuration
3. **If verified**, PyPI allows the package upload
4. **Token expires** automatically after use

## 🧪 Testing the Setup

### Test PyPI:
1. Push to main branch → Triggers `test-pypi-publish.yml`
2. Check workflow logs for successful OIDC authentication
3. Verify package appears on Test PyPI

### Production PyPI:
1. Create a release → Triggers `build-and-publish.yml`
2. Check workflow logs for successful OIDC authentication  
3. Verify package appears on production PyPI

## 🔧 Troubleshooting

### Common Issues:

**❌ "OIDC token request failed"**
- Check that `id-token: write` permission is set
- Verify workflow filename matches PyPI configuration exactly

**❌ "Trusted publisher not configured"**
- Ensure you've added the trusted publisher on PyPI/Test PyPI
- Check repository owner/name spelling
- Verify workflow filename is correct

**❌ "Authentication failed"**  
- Make sure you removed the `password:` line from publish steps
- Verify the repository name matches exactly (case-sensitive)

## 📚 References

- [PyPI Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [GitHub OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [PyPA Publish Action OIDC](https://github.com/pypa/gh-action-pypi-publish#trusted-publishing)
