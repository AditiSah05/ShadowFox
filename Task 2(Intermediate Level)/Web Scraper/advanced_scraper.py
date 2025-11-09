"""
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

Advanced Web Scraping Tool with Multi-Threading and Deep Crawling
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import logging
from datetime import datetime
from urllib.parse import urljoin, urlparse, urlunparse
from typing import Dict, List, Optional, Set, Any
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque
import re


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


class AdvancedScraperConfig:
    """Configuration for advanced web scraper."""
    
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    DEFAULT_TIMEOUT = 15
    DEFAULT_DELAY = 1
    MAX_RETRIES = 3
    MAX_DEPTH = 3
    MAX_THREADS = 4
    OUTPUT_DIR = Path('scraped_data')
    
    SHADOWFOX_URL = "https://www.shadowfox.org.in/"


def print_banner():
    """Display the scraper banner."""
    banner = f"""
{Colors.RED}╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║{Colors.WHITE}                          SHADOWFOX WEB SCRAPER                             {Colors.RED}║
║{Colors.YELLOW}                           Advanced Edition v2.0                            {Colors.RED}║
║                                                                            ║
║{Colors.CYAN}                        LEARN • CREATE • LEAD                               {Colors.RED}║
║{Colors.BLUE}                    https://www.shadowfox.org.in/                           {Colors.RED}║
║                                                                            ║
║{Colors.YELLOW}         Unleash the power of Open-Source Intelligence                      {Colors.RED}║
║{Colors.GREEN}                  ~By: ShadowFox Development Team                           {Colors.RED}║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


class AdvancedWebScraper:
    """
    Advanced web scraper with deep crawling and multi-threading capabilities.
    
    Features:
    - Multi-threaded crawling
    - Deep link discovery
    - Pattern matching
    - Comprehensive data extraction
    - Progress tracking
    """
    
    def __init__(self, target_url: str, max_depth: int = 2, max_threads: int = 4):
        """
        Initialize the advanced scraper.
        
        Args:
            target_url: Target website URL
            max_depth: Maximum crawling depth
            max_threads: Number of concurrent threads
        """
        self.target_url = target_url
        self.base_domain = urlparse(target_url).netloc
        self.max_depth = max_depth
        self.max_threads = max_threads
        
        self.session = requests.Session()
        self.session.headers.update(AdvancedScraperConfig.DEFAULT_HEADERS)
        
        self.visited_urls: Set[str] = set()
        self.to_visit: deque = deque([(target_url, 0)])
        self.found_data: List[Dict] = []
        
        self.stats = {
            'urls_crawled': 0,
            'urls_found': 0,
            'data_extracted': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Create output directory
        AdvancedScraperConfig.OUTPUT_DIR.mkdir(exist_ok=True)
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        log_file = AdvancedScraperConfig.OUTPUT_DIR / f'crawler_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def print_status(self, message: str, status: str = 'info'):
        """Print colored status messages."""
        if status == 'success':
            print(f"{Colors.GREEN}[✓]{Colors.RESET} {message}")
        elif status == 'error':
            print(f"{Colors.RED}[!]{Colors.RESET} {message}")
        elif status == 'crawling':
            print(f"{Colors.YELLOW}[!]Crawling:{Colors.RESET} {message}")
        elif status == 'matched':
            print(f"  {Colors.GREEN}→ [✓] Matched:{Colors.RESET} {message}")
        else:
            print(f"{Colors.BLUE}[!]{Colors.RESET} {message}")
    
    def normalize_url(self, url: str) -> str:
        """Normalize URL by removing fragments and query parameters."""
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and belongs to target domain."""
        try:
            parsed = urlparse(url)
            return (
                parsed.scheme in ['http', 'https'] and
                parsed.netloc == self.base_domain and
                not any(ext in parsed.path.lower() for ext in ['.pdf', '.jpg', '.png', '.gif', '.zip', '.exe'])
            )
        except:
            return False
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage."""
        try:
            response = self.session.get(
                url,
                timeout=AdvancedScraperConfig.DEFAULT_TIMEOUT,
                allow_redirects=True
            )
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            return BeautifulSoup(response.text, 'html.parser')
            
        except requests.exceptions.RequestException as e:
            self.stats['errors'] += 1
            self.logger.error(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error(f"Unexpected error: {e}")
            return None
    
    def extract_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """Extract all valid links from a page."""
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(current_url, href)
            normalized_url = self.normalize_url(absolute_url)
            
            if self.is_valid_url(normalized_url) and normalized_url not in self.visited_urls:
                links.append(normalized_url)
        
        return links
    
    def extract_page_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract comprehensive data from a page."""
        data = {
            'url': url,
            'title': None,
            'headings': [],
            'paragraphs': [],
            'links': [],
            'images': [],
            'forms': [],
            'scripts': [],
            'meta': {},
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Title
            if soup.title:
                data['title'] = soup.title.get_text(strip=True)
            
            # Headings
            for tag in ['h1', 'h2', 'h3']:
                for heading in soup.find_all(tag):
                    text = heading.get_text(strip=True)
                    if text:
                        data['headings'].append({'level': tag, 'text': text})
            
            # Paragraphs
            for p in soup.find_all('p'):
                text = p.get_text(strip=True)
                if len(text) > 20:
                    data['paragraphs'].append(text)
            
            # Links
            for link in soup.find_all('a', href=True):
                data['links'].append({
                    'text': link.get_text(strip=True),
                    'href': link['href']
                })
            
            # Images
            for img in soup.find_all('img'):
                data['images'].append({
                    'src': img.get('src', ''),
                    'alt': img.get('alt', '')
                })
            
            # Forms
            for form in soup.find_all('form'):
                data['forms'].append({
                    'action': form.get('action', ''),
                    'method': form.get('method', 'get')
                })
            
            # Scripts
            for script in soup.find_all('script', src=True):
                data['scripts'].append(script['src'])
            
            # Meta tags
            for meta in soup.find_all('meta'):
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    data['meta'][name] = content
            
            self.stats['data_extracted'] += 1
            
        except Exception as e:
            self.logger.error(f"Error extracting data from {url}: {e}")
        
        return data
    
    def crawl_url(self, url: str, depth: int) -> List[str]:
        """Crawl a single URL and return discovered links."""
        if url in self.visited_urls or depth > self.max_depth:
            return []
        
        self.visited_urls.add(url)
        self.stats['urls_crawled'] += 1
        
        self.print_status(url, 'crawling')
        
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        # Extract data
        page_data = self.extract_page_data(soup, url)
        self.found_data.append(page_data)
        
        # Pattern matching (example: looking for specific keywords)
        patterns = ['contact', 'about', 'service', 'product', 'blog']
        for pattern in patterns:
            if pattern in url.lower():
                self.print_status(f"['{pattern}']", 'matched')
                break
        
        # Extract new links
        new_links = self.extract_links(soup, url)
        self.stats['urls_found'] += len(new_links)
        
        # Add delay to be respectful
        time.sleep(AdvancedScraperConfig.DEFAULT_DELAY)
        
        return new_links
    
    def start_crawling(self):
        """Start the crawling process with multi-threading."""
        print_banner()
        
        print(f"\n{Colors.MAGENTA}TARGET:{Colors.RESET} {self.target_url}")
        print(f"\n{Colors.BLUE}[!] Initializing Crawler...{Colors.RESET}")
        print(f"{Colors.BLUE}[!] Max Depth: {self.max_depth}{Colors.RESET}")
        print(f"{Colors.BLUE}[!] Max Threads: {self.max_threads}{Colors.RESET}")
        print(f"{Colors.GREEN}[✓] Preparing Crawler (Utilizing {self.max_threads} threads){Colors.RESET}\n")
        
        self.stats['start_time'] = datetime.now()
        
        try:
            while self.to_visit:
                current_batch = []
                
                # Collect URLs for current batch
                while self.to_visit and len(current_batch) < self.max_threads:
                    url, depth = self.to_visit.popleft()
                    if url not in self.visited_urls:
                        current_batch.append((url, depth))
                
                if not current_batch:
                    break
                
                # Process batch with threading
                with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                    future_to_url = {
                        executor.submit(self.crawl_url, url, depth): (url, depth)
                        for url, depth in current_batch
                    }
                    
                    for future in as_completed(future_to_url):
                        url, depth = future_to_url[future]
                        try:
                            new_links = future.result()
                            # Add new links to queue
                            for link in new_links:
                                if link not in self.visited_urls:
                                    self.to_visit.append((link, depth + 1))
                        except Exception as e:
                            self.logger.error(f"Error processing {url}: {e}")
            
            self.stats['end_time'] = datetime.now()
            
            print(f"\n{Colors.GREEN}Crawling finished.{Colors.RESET}\n")
            
            # Export results
            self.export_results()
            
            # Print statistics
            self.print_statistics()
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Crawling interrupted by user{Colors.RESET}")
            self.export_results()
            self.print_statistics()
    
    def export_results(self):
        """Export crawling results to files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Prepare stats for JSON export
        stats_export = self.stats.copy()
        if stats_export['start_time']:
            stats_export['start_time'] = stats_export['start_time'].isoformat()
        if stats_export['end_time']:
            stats_export['end_time'] = stats_export['end_time'].isoformat()
        
        # Export to JSON
        json_file = AdvancedScraperConfig.OUTPUT_DIR / f'crawl_results_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'target': self.target_url,
                'stats': stats_export,
                'data': self.found_data
            }, f, indent=2, ensure_ascii=False)
        
        print(f"{Colors.GREEN}[✓] Results exported to: {json_file}{Colors.RESET}")
        
        # Export URLs to text file
        urls_file = AdvancedScraperConfig.OUTPUT_DIR / f'discovered_urls_{timestamp}.txt'
        with open(urls_file, 'w', encoding='utf-8') as f:
            f.write(f"Discovered URLs from: {self.target_url}\n")
            f.write(f"Total URLs: {len(self.visited_urls)}\n")
            f.write("=" * 80 + "\n\n")
            for url in sorted(self.visited_urls):
                f.write(f"{url}\n")
        
        print(f"{Colors.GREEN}[✓] URLs exported to: {urls_file}{Colors.RESET}")
    
    def print_statistics(self):
        """Print crawling statistics."""
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds() if self.stats['end_time'] else 0
        
        print(f"\n{Colors.CYAN}{'=' * 80}{Colors.RESET}")
        print(f"{Colors.BOLD}CRAWLING STATISTICS{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 80}{Colors.RESET}")
        print(f"Target URL:           {self.target_url}")
        print(f"URLs Crawled:         {self.stats['urls_crawled']}")
        print(f"URLs Discovered:      {self.stats['urls_found']}")
        print(f"Pages Extracted:      {self.stats['data_extracted']}")
        print(f"Errors Encountered:   {self.stats['errors']}")
        print(f"Duration:             {duration:.2f} seconds")
        print(f"Average Speed:        {self.stats['urls_crawled']/max(duration, 1):.2f} pages/second")
        print(f"{Colors.CYAN}{'=' * 80}{Colors.RESET}\n")


def main():
    """Main function to run the scraper."""
    # Example usage
    target = "http://quotes.toscrape.com/"
    
    scraper = AdvancedWebScraper(
        target_url=target,
        max_depth=2,
        max_threads=4
    )
    
    scraper.start_crawling()


if __name__ == "__main__":
    main()
