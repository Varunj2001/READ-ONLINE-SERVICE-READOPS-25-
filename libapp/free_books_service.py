"""
Free Books Service for ReadOps Library Management System
Finds free alternatives for books not available in the library
"""

import requests
import json
from typing import List, Dict, Optional
from django.conf import settings

class FreeBooksService:
    """
    Service to find free book alternatives from various platforms
    """
    
    def __init__(self):
        self.free_platforms = {
            'project_gutenberg': {
                'name': 'Project Gutenberg',
                'url': 'https://www.gutenberg.org/ebooks/search/?query={query}',
                'api_url': 'https://www.gutenberg.org/ebooks/search/?query={query}&format=json',
                'description': 'Free ebooks from the world\'s first digital library'
            },
            'open_library': {
                'name': 'Open Library',
                'url': 'https://openlibrary.org/search?q={query}',
                'api_url': 'https://openlibrary.org/search.json?q={query}',
                'description': 'Open, editable library catalog'
            },
            'many_books': {
                'name': 'ManyBooks',
                'url': 'https://manybooks.net/search-book?search={query}',
                'description': 'Free ebooks in various formats'
            },
            'free_ebooks': {
                'name': 'Free-eBooks.net',
                'url': 'https://www.free-ebooks.net/search/{query}',
                'description': 'Free ebooks and magazines'
            },
            'google_books': {
                'name': 'Google Books (Free)',
                'url': 'https://books.google.com/books?q={query}&filter=free-ebooks',
                'description': 'Free books from Google Books'
            },
            'archive_org': {
                'name': 'Internet Archive',
                'url': 'https://archive.org/search.php?query={query}&sin=TXT&and[]=mediatype:texts',
                'description': 'Digital library of free books and media'
            },
            'hathitrust': {
                'name': 'HathiTrust',
                'url': 'https://catalog.hathitrust.org/Search/Home?lookfor={query}&type=all&setid=set_ft',
                'description': 'Digital preservation repository'
            },
            'libgen': {
                'name': 'Library Genesis',
                'url': 'https://libgen.is/search.php?req={query}',
                'description': 'Academic and scientific literature'
            }
        }
    
    def search_free_books(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search for free books across multiple platforms
        """
        results = []
        
        # Clean and prepare query
        clean_query = query.strip().replace(' ', '+')
        
        # Search each platform
        for platform_id, platform_info in self.free_platforms.items():
            try:
                platform_results = self._search_platform(platform_id, clean_query, limit)
                if platform_results:
                    results.extend(platform_results)
            except Exception as e:
                print(f"Error searching {platform_info['name']}: {str(e)}")
                continue
        
        # Remove duplicates and limit results
        unique_results = self._remove_duplicates(results)
        return unique_results[:limit]
    
    def _search_platform(self, platform_id: str, query: str, limit: int) -> List[Dict]:
        """
        Search a specific platform for free books
        """
        platform = self.free_platforms[platform_id]
        results = []
        
        if platform_id == 'open_library':
            return self._search_open_library(query, limit)
        elif platform_id == 'project_gutenberg':
            return self._search_project_gutenberg(query, limit)
        else:
            # For platforms without API, return direct links
            return [{
                'title': f'Search {platform["name"]}',
                'author': 'Various Authors',
                'url': platform['url'].format(query=query),
                'platform': platform['name'],
                'description': platform['description'],
                'is_direct_link': True
            }]
    
    def _search_open_library(self, query: str, limit: int) -> List[Dict]:
        """
        Search Open Library API
        """
        try:
            url = f"https://openlibrary.org/search.json?q={query}&limit={limit}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            results = []
            for doc in data.get('docs', [])[:limit]:
                if doc.get('ebook_count_i', 0) > 0:  # Only include books with ebooks
                    results.append({
                        'title': doc.get('title', 'Unknown Title'),
                        'author': ', '.join(doc.get('author_name', ['Unknown Author'])),
                        'url': f"https://openlibrary.org{doc.get('key', '')}",
                        'platform': 'Open Library',
                        'description': f"Available as ebook with {doc.get('ebook_count_i', 0)} formats",
                        'is_direct_link': False,
                        'year': doc.get('first_publish_year', 'Unknown')
                    })
            
            return results
        except Exception as e:
            print(f"Error searching Open Library: {str(e)}")
            return []
    
    def _search_project_gutenberg(self, query: str, limit: int) -> List[Dict]:
        """
        Search Project Gutenberg (simplified)
        """
        # Project Gutenberg doesn't have a public API, so we return direct search links
        return [{
            'title': f'Search Project Gutenberg for "{query}"',
            'author': 'Various Authors',
            'url': f"https://www.gutenberg.org/ebooks/search/?query={query}",
            'platform': 'Project Gutenberg',
            'description': 'Free ebooks from the world\'s first digital library',
            'is_direct_link': True
        }]
    
    def _remove_duplicates(self, results: List[Dict]) -> List[Dict]:
        """
        Remove duplicate results based on title and author
        """
        seen = set()
        unique_results = []
        
        for result in results:
            key = (result['title'].lower(), result['author'].lower())
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        return unique_results
    
    def get_platform_suggestions(self, book_title: str, book_author: str = None) -> Dict:
        """
        Get platform suggestions for a specific book
        """
        query = book_title
        if book_author:
            query = f"{book_title} {book_author}"
        
        free_books = self.search_free_books(query, limit=3)
        
        # Create direct search links for all platforms
        platform_links = []
        for platform_id, platform_info in self.free_platforms.items():
            platform_links.append({
                'name': platform_info['name'],
                'url': platform_info['url'].format(query=query),
                'description': platform_info['description']
            })
        
        return {
            'book_title': book_title,
            'book_author': book_author,
            'free_books_found': free_books,
            'platform_links': platform_links,
            'search_query': query
        }
    
    def get_subject_specific_platforms(self, subject: str) -> List[Dict]:
        """
        Get platforms that are good for specific subjects
        """
        subject_platforms = {
            'computer science': ['project_gutenberg', 'open_library', 'libgen'],
            'mathematics': ['project_gutenberg', 'open_library', 'libgen'],
            'physics': ['project_gutenberg', 'open_library', 'libgen'],
            'literature': ['project_gutenberg', 'open_library', 'many_books'],
            'history': ['project_gutenberg', 'open_library', 'archive_org'],
            'philosophy': ['project_gutenberg', 'open_library', 'libgen'],
            'science': ['project_gutenberg', 'open_library', 'libgen'],
            'engineering': ['open_library', 'libgen', 'hathitrust']
        }
        
        subject_lower = subject.lower()
        recommended_platforms = []
        
        for category, platforms in subject_platforms.items():
            if category in subject_lower:
                for platform_id in platforms:
                    if platform_id in self.free_platforms:
                        platform = self.free_platforms[platform_id]
                        recommended_platforms.append({
                            'name': platform['name'],
                            'url': platform['url'],
                            'description': platform['description'],
                            'reason': f'Great for {category} books'
                        })
        
        # If no specific match, return general platforms
        if not recommended_platforms:
            recommended_platforms = [
                {
                    'name': platform['name'],
                    'url': platform['url'],
                    'description': platform['description'],
                    'reason': 'General purpose free book platform'
                }
                for platform in list(self.free_platforms.values())[:4]
            ]
        
        return recommended_platforms

# Create a global instance
free_books_service = FreeBooksService()
