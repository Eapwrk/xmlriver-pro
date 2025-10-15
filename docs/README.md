# 📚 XMLRiver Pro Documentation

## Quick Start

### Installation
```bash
# Latest version
pip install git+https://github.com/Eapwrk/xmlriver-pro.git

# Specific version
pip install git+https://github.com/Eapwrk/xmlriver-pro.git@v1.0.2
```

### Basic Usage
```python
from xmlriver_pro import GoogleClient, YandexClient

google = GoogleClient(user_id=123, api_key="your_key")
results = google.search("python programming")
print(f"Found: {results.total_results} results")
```

## Documentation Files

- **[examples.md](examples.md)** - Comprehensive usage examples
- **[versioning.md](versioning.md)** - Version management and releases
- **[llms.txt](llms.txt)** - AI-friendly documentation index

## Features

- ✅ Full Google and Yandex API coverage
- ✅ Type hints and modern architecture
- ✅ Comprehensive error handling
- ✅ 66 tests with 58% coverage
- ✅ Centralized versioning system
- ✅ GitHub Actions for releases

## Version Management

- **Current version**: 1.0.2
- **Versioning**: Semantic (MAJOR.MINOR.PATCH)
- **Updates**: Watch repository or check email
- **Scripts**: `update_version.py`, `create_release.py`

## API Limits

- **Concurrent streams**: 10 per system
- **Daily limits**: Google ~200k, Yandex ~150k
- **Response time**: 3-6 seconds (usually)
- **Timeout**: 60 seconds recommended

## Support

- 📧 **Email**: seo@controlseo.ru
- 🐛 **Issues**: [GitHub Issues](https://github.com/Eapwrk/xmlriver-pro/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Eapwrk/xmlriver-pro/discussions)