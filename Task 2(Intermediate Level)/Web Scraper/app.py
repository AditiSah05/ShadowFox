"""
Professional Web Scraper for ShadowFox
======================================
A robust, production-ready web scraping solution with comprehensive
error handling, logging, and data export capabilities.

ShadowFox - LEARN • CREATE • LEAD
Website: https://www.shadowfox.org.in/

Author: ShadowFox Development Team
Version: 2.0
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import logging
from datetime import datetime
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Any
from pathlib import Path
import sys


def print_shadowfox_banner():
    """Display ShadowFox branding banner."""
    banner = """
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║                           🦊 ShadowFox Web Scraper                         ║
    ║                                                                            ║
    ║                        LEARN • CREATE • LEAD                               ║
    ║                                                                            ║
    ║                    https://www.shadowfox.org.in/                           ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


class ScraperConfig:
    """Configuration class for web scraper settings."""
    
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    DEFAULT_TIMEOUT = 15
    DEFAULT_DELAY = 2
    MAX_RETRIES = 3
    OUTPUT_DIR = Path('scraped_data')
    
    SHADOWFOX_URL = "https://www.shadowfox.org.in/"
    SHADOWFOX_TAGLINE = "LEARN • CREATE • LEAD"


class WebScraperPro:
    """
    Professional-grade web scraper with advanced features.
    
    Features:
    - Robust error handling and retry logic
    - Comprehensive logging
    - Multiple export formats (JSON, CSV, TXT)
    - Rate limiting and respectful scraping
    - Session management
    - Data validation
    """
    
    def __init__(self, base_url: str, headers: Optional[Dict] = None, log_level: str = 'INFO'):
        """
        Initialize the professional web scraper.
        
        Args:
            base_url: The base URL to scrape
            headers: Optional custom HTTP headers
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.base_url = base_url
        self.headers = headers or ScraperConfig.DEFAULT_HEADERS
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.stats = {
            'requests_made': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'data_points_extracted': 0
        }
        
        # Create output directory first
        ScraperConfig.OUTPUT_DIR.mkdir(exist_ok=True)
        
        # Setup logging
        self._setup_logging(log_level)
        
        self.logger.info(f"WebScraperPro initialized for: {base_url}")
    
    def _setup_logging(self, log_level: str):
        """Configure logging with both file and console handlers."""
        self.logger = logging.getLogger('WebScraperPro')
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_format)
        
        # File handler
        log_file = ScraperConfig.OUTPUT_DIR / f'scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def fetch_page(self, url: str, timeout: int = ScraperConfig.DEFAULT_TIMEOUT, 
                   retries: int = ScraperConfig.MAX_RETRIES) -> Optional[BeautifulSoup]:
        """
        Fetch a web page with retry logic and comprehensive error handling.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            retries: Number of retry attempts
            
        Returns:
            BeautifulSoup object or None if all attempts fail
        """
        self.stats['requests_made'] += 1
        
        for attempt in range(1, retries + 1):
            try:
                self.logger.debug(f"Fetching {url} (Attempt {attempt}/{retries})")
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                
                soup = BeautifulSoup(response.text, 'html.parser')
                self.stats['successful_requests'] += 1
                self.logger.info(f"[OK] Successfully fetched: {url}")
                return soup
                
            except requests.exceptions.HTTPError as e:
                self.logger.error(f"[ERROR] HTTP Error {response.status_code} for {url}: {e}")
                if response.status_code in [404, 403, 401]:
                    break
                    
            except requests.exceptions.ConnectionError:
                self.logger.error(f"[ERROR] Connection Error: Unable to reach {url}")
                
            except requests.exceptions.Timeout:
                self.logger.error(f"[ERROR] Timeout Error: {url} took too long to respond")
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"[ERROR] Request Error for {url}: {e}")
                
            except Exception as e:
                self.logger.error(f"[ERROR] Unexpected error fetching {url}: {e}")
            
            if attempt < retries:
                wait_time = attempt * 2
                self.logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        
        self.stats['failed_requests'] += 1
        return None
    
    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract comprehensive metadata from a webpage."""
        metadata = {
            'title': None,
            'description': None,
            'keywords': None,
            'author': None,
            'og_title': None,
            'og_description': None,
            'og_image': None
        }
        
        try:
            title_tag = soup.find('title')
            if title_tag:
                metadata['title'] = title_tag.get_text(strip=True)
            
            desc_tag = soup.find('meta', attrs={'name': 'description'})
            if desc_tag and desc_tag.get('content'):
                metadata['description'] = desc_tag.get('content')
            
            keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
            if keywords_tag and keywords_tag.get('content'):
                metadata['keywords'] = keywords_tag.get('content')
            
            author_tag = soup.find('meta', attrs={'name': 'author'})
            if author_tag and author_tag.get('content'):
                metadata['author'] = author_tag.get('content')
            
            og_title_tag = soup.find('meta', attrs={'property': 'og:title'})
            if og_title_tag and og_title_tag.get('content'):
                metadata['og_title'] = og_title_tag.get('content')
            
            og_desc_tag = soup.find('meta', attrs={'property': 'og:description'})
            if og_desc_tag and og_desc_tag.get('content'):
                metadata['og_description'] = og_desc_tag.get('content')
            
            og_image_tag = soup.find('meta', attrs={'property': 'og:image'})
            if og_image_tag and og_image_tag.get('content'):
                metadata['og_image'] = og_image_tag.get('content')
            
            self.logger.debug(f"Extracted metadata: {metadata['title']}")
            
        except Exception as e:
            self.logger.error(f"[ERROR] Error extracting metadata: {e}")
        
        return metadata
    
    def extract_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract main content from webpage."""
        content = {
            'headings': [],
            'paragraphs': [],
            'links': [],
            'images': [],
            'lists': []
        }
        
        try:
            # Headings
            for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                headings = soup.find_all(tag)
                for h in headings:
                    text = h.get_text(strip=True)
                    if text:
                        content['headings'].append({
                            'level': tag,
                            'text': text
                        })
            
            # Paragraphs
            paragraphs = soup.find_all('p')
            content['paragraphs'] = [p.get_text(strip=True) for p in paragraphs 
                                    if len(p.get_text(strip=True)) > 20]
            
            # Links
            links = soup.find_all('a', href=True)
            for link in links:
                text = link.get_text(strip=True)
                href = urljoin(self.base_url, link['href'])
                if text and href:
                    content['links'].append({
                        'text': text,
                        'url': href,
                        'is_internal': urlparse(href).netloc == urlparse(self.base_url).netloc
                    })
            
            # Images
            images = soup.find_all('img')
            for img in images:
                content['images'].append({
                    'src': urljoin(self.base_url, img.get('src', '')),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
            
            # Lists
            for ul in soup.find_all(['ul', 'ol']):
                items = [li.get_text(strip=True) for li in ul.find_all('li')]
                if items:
                    content['lists'].append(items)
            
            self.stats['data_points_extracted'] += len(content['headings']) + len(content['paragraphs'])
            self.logger.debug(f"Extracted {len(content['headings'])} headings, {len(content['paragraphs'])} paragraphs")
            
        except Exception as e:
            self.logger.error(f"[ERROR] Error extracting content: {e}")
        
        return content
    
    def scrape_website(self, url: str) -> Dict[str, Any]:
        """
        Perform comprehensive scraping of a website.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary containing all scraped data
        """
        self.logger.info(f"Starting comprehensive scrape of: {url}")
        
        soup = self.fetch_page(url)
        if not soup:
            return {'error': 'Failed to fetch page', 'url': url}
        
        data = {
            'url': url,
            'scraped_at': datetime.now().isoformat(),
            'scraped_by': 'ShadowFox Web Scraper',
            'metadata': self.extract_metadata(soup),
            'content': self.extract_content(soup)
        }
        
        return data
    
    def export_json(self, data: Any, filename: str):
        """Export data to JSON with pretty formatting."""
        try:
            filepath = ScraperConfig.OUTPUT_DIR / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"[OK] Data exported to JSON: {filepath}")
        except Exception as e:
            self.logger.error(f"[ERROR] Error exporting to JSON: {e}")
    
    def export_csv(self, data: List[Dict], filename: str):
        """Export data to CSV format."""
        try:
            if not data:
                self.logger.warning("[WARN] No data to export to CSV")
                return
            
            filepath = ScraperConfig.OUTPUT_DIR / filename
            keys = data[0].keys()
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            
            self.logger.info(f"[OK] Data exported to CSV: {filepath}")
        except Exception as e:
            self.logger.error(f"[ERROR] Error exporting to CSV: {e}")
    
    def export_txt(self, data: Dict, filename: str):
        """Export data to readable text format."""
        try:
            filepath = ScraperConfig.OUTPUT_DIR / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("SHADOWFOX WEB SCRAPING REPORT\n")
                f.write(f"Website: {ScraperConfig.SHADOWFOX_URL}\n")
                f.write(f"Tagline: {ScraperConfig.SHADOWFOX_TAGLINE}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                if 'metadata' in data:
                    f.write("METADATA\n")
                    f.write("-" * 80 + "\n")
                    for key, value in data['metadata'].items():
                        if value:
                            f.write(f"{key.upper()}: {value}\n")
                    f.write("\n")
                
                if 'content' in data and 'headings' in data['content']:
                    f.write("HEADINGS\n")
                    f.write("-" * 80 + "\n")
                    for h in data['content']['headings'][:10]:
                        f.write(f"[{h['level'].upper()}] {h['text']}\n")
                    f.write("\n")
                
                if 'content' in data and 'paragraphs' in data['content']:
                    f.write("CONTENT PREVIEW\n")
                    f.write("-" * 80 + "\n")
                    for p in data['content']['paragraphs'][:5]:
                        f.write(f"{p}\n\n")
            
            self.logger.info(f"[OK] Data exported to TXT: {filepath}")
        except Exception as e:
            self.logger.error(f"[ERROR] Error exporting to TXT: {e}")
    
    def print_statistics(self):
        """Print scraping statistics."""
        print("\n" + "=" * 80)
        print("SCRAPING STATISTICS")
        print("=" * 80)
        print(f"Total Requests Made:      {self.stats['requests_made']}")
        print(f"Successful Requests:      {self.stats['successful_requests']}")
        print(f"Failed Requests:          {self.stats['failed_requests']}")
        print(f"Data Points Extracted:    {self.stats['data_points_extracted']}")
        success_rate = (self.stats['successful_requests']/max(self.stats['requests_made'],1)*100)
        print(f"Success Rate:             {success_rate:.1f}%")
        print("=" * 80 + "\n")


def scrape_shadowfox_website():
    """Scrape the official ShadowFox website."""
    print_shadowfox_banner()
    
    print("\n[INFO] Initializing ShadowFox Web Scraper...")
    scraper = WebScraperPro(ScraperConfig.SHADOWFOX_URL, log_level='INFO')
    
    # Scrape the website
    data = scraper.scrape_website(ScraperConfig.SHADOWFOX_URL)
    
    if 'error' not in data:
        # Display summary
        print("\n" + "-" * 80)
        print("SCRAPING SUMMARY")
        print("-" * 80)
        print(f"Website:     {data['metadata']['title'] or 'ShadowFox'}")
        desc = data['metadata']['description']
        print(f"Description: {desc[:100] if desc else 'N/A'}...")
        print(f"Headings:    {len(data['content']['headings'])} found")
        print(f"Paragraphs:  {len(data['content']['paragraphs'])} found")
        print(f"Links:       {len(data['content']['links'])} found")
        print(f"Images:      {len(data['content']['images'])} found")
        print("-" * 80 + "\n")
        
        # Display sample headings
        if data['content']['headings']:
            print("SAMPLE HEADINGS:")
            for i, heading in enumerate(data['content']['headings'][:5], 1):
                print(f"  {i}. [{heading['level'].upper()}] {heading['text']}")
            print()
        
        # Export data in multiple formats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scraper.export_json(data, f'shadowfox_data_{timestamp}.json')
        scraper.export_txt(data, f'shadowfox_report_{timestamp}.txt')
        
        # Export links to CSV
        if data['content']['links']:
            scraper.export_csv(data['content']['links'][:50], f'shadowfox_links_{timestamp}.csv')
    else:
        print(f"\n[ERROR] {data['error']}")
    
    # Print statistics
    scraper.print_statistics()


def demo_scraper():
    """Demonstration with a working example website."""
    print_shadowfox_banner()
    
    print("\n[INFO] Running demonstration scraper...")
    scraper = WebScraperPro("http://quotes.toscrape.com/", log_level='INFO')
    
    # Scrape the quotes website
    data = scraper.scrape_website("http://quotes.toscrape.com/")
    
    if 'error' not in data:
        # Display summary
        print("\n" + "-" * 80)
        print("SCRAPING SUMMARY")
        print("-" * 80)
        print(f"Website:     {data['metadata']['title'] or 'Quotes to Scrape'}")
        print(f"Headings:    {len(data['content']['headings'])} found")
        print(f"Paragraphs:  {len(data['content']['paragraphs'])} found")
        print(f"Links:       {len(data['content']['links'])} found")
        print(f"Images:      {len(data['content']['images'])} found")
        print("-" * 80 + "\n")
        
        # Display sample content
        if data['content']['headings']:
            print("SAMPLE HEADINGS:")
            for i, heading in enumerate(data['content']['headings'][:5], 1):
                print(f"  {i}. [{heading['level'].upper()}] {heading['text']}")
            print()
        
        if data['content']['paragraphs']:
            print("SAMPLE CONTENT:")
            for i, para in enumerate(data['content']['paragraphs'][:3], 1):
                preview = para[:100] + "..." if len(para) > 100 else para
                print(f"  {i}. {preview}")
            print()
        
        # Export data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scraper.export_json(data, f'demo_data_{timestamp}.json')
        scraper.export_txt(data, f'demo_report_{timestamp}.txt')
        
        if data['content']['links']:
            scraper.export_csv(data['content']['links'][:20], f'demo_links_{timestamp}.csv')
    
    scraper.print_statistics()


if __name__ == "__main__":
    # Run demonstration scraper
    demo_scraper()
    
    # Uncomment to scrape ShadowFox website
    # scrape_shadowfox_website()
