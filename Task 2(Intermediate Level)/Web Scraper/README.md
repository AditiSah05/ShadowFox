# ShadowFox Web Scraper
![alt text](image.png)

![ShadowFox](https://img.shields.io/badge/ShadowFox-Web%20Scraper-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🦊 About

**ShadowFox Web Scraper** is a professional-grade web scraping toolkit developed by the ShadowFox Development Team. This project demonstrates advanced web scraping techniques with comprehensive error handling, multi-threading, and multiple export formats.

**Website:** [https://www.shadowfox.org.in/](https://www.shadowfox.org.in/)

**Tagline:** LEARN • CREATE • LEAD

---

## ✨ Features

### Basic Scraper (`app.py`)
- ✅ Beautiful Soup integration for HTML parsing
- ✅ Comprehensive error handling (HTTP, Connection, Timeout errors)
- ✅ Multiple export formats (JSON, CSV, TXT)
- ✅ Retry logic with exponential backoff
- ✅ Session management
- ✅ Logging system (console + file)
- ✅ Statistics tracking
- ✅ ShadowFox branding

### Advanced Scraper (`advanced_scraper.py`)
- 🚀 Multi-threaded crawling
- 🚀 Deep link discovery
- 🚀 Pattern matching
- 🚀 Configurable crawl depth
- 🚀 URL normalization
- 🚀 Progress tracking with colored output
- 🚀 Comprehensive data extraction
- 🚀 Respectful crawling with rate limiting

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install requests beautifulsoup4
```

---

## 🚀 Usage

### Basic Scraper

```python
from app import WebScraperPro, scrape_shadowfox_website, demo_scraper

# Run demonstration scraper
demo_scraper()

# Or scrape ShadowFox website
scrape_shadowfox_website()
```

**Run from command line:**
```bash
python app.py
```

### Advanced Scraper

```python
from advanced_scraper import AdvancedWebScraper

# Create scraper instance
scraper = AdvancedWebScraper(
    target_url="http://example.com/",
    max_depth=2,
    max_threads=4
)

# Start crawling
scraper.start_crawling()
```

**Run from command line:**
```bash
python advanced_scraper.py
```

---

## 📊 Output Files

All scraped data is saved in the `scraped_data/` directory:

### Basic Scraper Output
- `shadowfox_data_TIMESTAMP.json` - Complete scraped data in JSON format
- `shadowfox_report_TIMESTAMP.txt` - Human-readable report
- `shadowfox_links_TIMESTAMP.csv` - Extracted links in CSV format
- `scraper_TIMESTAMP.log` - Detailed log file

### Advanced Scraper Output
- `crawl_results_TIMESTAMP.json` - Complete crawl results with statistics
- `discovered_urls_TIMESTAMP.txt` - List of all discovered URLs
- `crawler_TIMESTAMP.log` - Detailed crawl log

---

## 🎨 Features Breakdown

### Data Extraction

The scrapers extract:
- **Metadata**: Title, description, keywords, Open Graph tags
- **Content**: Headings (H1-H6), paragraphs, lists
- **Links**: Internal and external links with text
- **Images**: Image sources, alt text, titles
- **Forms**: Form actions and methods
- **Scripts**: External script sources

### Error Handling

Comprehensive error handling for:
- HTTP errors (404, 403, 500, etc.)
- Connection errors
- Timeout errors
- Request exceptions
- Unexpected errors

### Rate Limiting

- Configurable delay between requests
- Respectful crawling to avoid overwhelming servers
- Session management for efficient requests

---

## ⚙️ Configuration

### Basic Scraper Configuration

```python
class ScraperConfig:
    DEFAULT_TIMEOUT = 15
    DEFAULT_DELAY = 2
    MAX_RETRIES = 3
    OUTPUT_DIR = Path('scraped_data')
```

### Advanced Scraper Configuration

```python
class AdvancedScraperConfig:
    DEFAULT_TIMEOUT = 15
    DEFAULT_DELAY = 1
    MAX_RETRIES = 3
    MAX_DEPTH = 3
    MAX_THREADS = 4
    OUTPUT_DIR = Path('scraped_data')
```

---

## 📈 Statistics

The scrapers track:
- Total requests made
- Successful requests
- Failed requests
- Data points extracted
- URLs discovered
- Crawling duration
- Average speed (pages/second)

---

## 🛡️ Best Practices

1. **Respect robots.txt**: Always check the website's robots.txt file
2. **Rate limiting**: Use appropriate delays between requests
3. **User-Agent**: Use a descriptive User-Agent header
4. **Error handling**: Handle errors gracefully
5. **Legal compliance**: Ensure you have permission to scrape the website
6. **Data privacy**: Respect user privacy and data protection laws

---

## 📝 Example Output

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                          SHADOWFOX WEB SCRAPER                             ║
║                           Advanced Edition v2.0                            ║
║                                                                            ║
║                        LEARN • CREATE • LEAD                               ║
║                    https://www.shadowfox.org.in/                           ║
║                                                                            ║
║         Unleash the power of Open-Source Intelligence                      ║
║                  ~By: ShadowFox Development Team                           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

TARGET: http://quotes.toscrape.com/

[!] Initializing Crawler...
[!] Max Depth: 2
[!] Max Threads: 4
[✓] Preparing Crawler (Utilizing 4 threads)

[!]Crawling: http://quotes.toscrape.com/
  → [✓] Matched: ['quotes']

Crawling finished.

[✓] Results exported to: scraped_data\crawl_results_20251107_225647.json
[✓] URLs exported to: scraped_data\discovered_urls_20251107_225647.txt

================================================================================
CRAWLING STATISTICS
================================================================================
Target URL:           http://quotes.toscrape.com/
URLs Crawled:         15
URLs Discovered:      47
Pages Extracted:      15
Errors Encountered:   0
Duration:             12.34 seconds
Average Speed:        1.22 pages/second
================================================================================
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Authors

**ShadowFox Development Team**

- Website: [https://www.shadowfox.org.in/](https://www.shadowfox.org.in/)
- Tagline: LEARN • CREATE • LEAD

---

## ⚠️ Disclaimer

This tool is for educational purposes only. Always ensure you have permission to scrape a website and comply with its terms of service and robots.txt file. The developers are not responsible for any misuse of this tool.

---

## 🙏 Acknowledgments

- Beautiful Soup library for HTML parsing
- Requests library for HTTP requests
- ShadowFox community for support and feedback

---

**Made with ❤️ by ShadowFox Development Team**
