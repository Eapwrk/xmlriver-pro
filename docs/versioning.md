# 🔄 Versioning and Releases

## Version Management

XMLRiver Pro uses centralized versioning system:

- **Version location**: `__version__ = "2.0.0"` in `xmlriver_pro/__init__.py`
- **Synchronized files**: `pyproject.toml`, `setup.py`, `__init__.py`
- **History**: `CHANGELOG.md` with full release history
- **Format**: Semantic Versioning (MAJOR.MINOR.PATCH)

## Scripts

### `update_version.py`
Updates version in all files:
```bash
python update_version.py 1.1.0
```

### `create_release.py`
Creates release with checks:
```bash
python create_release.py 2.0.0
```

## Release Process

1. Update version: `python update_version.py 2.0.0`
2. Commit: `git commit -m "Bump version to 2.0.0"`
3. Create tag: `git tag -a v2.0.0 -m "Release 2.0.0"`
4. Push: `git push origin main --tags`
5. GitHub Actions automatically creates release

## Installation and Updates

### From GitHub (recommended):
```bash
# Latest version
pip install git+https://github.com/Eapwrk/xmlriver-pro.git

# Specific version
pip install git+https://github.com/Eapwrk/xmlriver-pro.git@v2.0.0

# Update to latest
pip install --upgrade git+https://github.com/Eapwrk/xmlriver-pro.git
```

### Check version:
```bash
python -c "import xmlriver_pro; print(xmlriver_pro.__version__)"
```

## Notifications

- ⭐ **GitHub Watch** repository for notifications
- 📧 **Email**: seo@controlseo.ru
- 🐛 **Issues**: [GitHub Issues](https://github.com/Eapwrk/xmlriver-pro/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Eapwrk/xmlriver-pro/discussions)

## GitHub Actions

Automatic release process:
- Triggers on git tag creation
- Runs tests and linting
- Builds package
- Creates GitHub Release
- Optional PyPI upload (if token configured)

## Changelog

See [CHANGELOG.md](../CHANGELOG.md) for detailed release history.
