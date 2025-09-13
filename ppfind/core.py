#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Core functionality module that provides paper information fetching capabilities.
"""

import requests
import arxiv
from serpapi import GoogleSearch

class PaperInfoFetcher:
    
    def __init__(self, serp_api_key):
        """
        Args:
            serp_api_key: SerpAPI的API密钥
        """
        self.serp_api_key = serp_api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_citations_from_scholar(self, title):
        """
        Args:
            title: paper title
            
        Returns:
            int: citation count, or None if failed
        """
        try:
            params = {
                "engine": "google_scholar",
                "q": title,
                "api_key": self.serp_api_key
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if "organic_results" in results and len(results["organic_results"]) > 0:
                first_result = results["organic_results"][0]
                if "inline_links" in first_result and "cited_by" in first_result["inline_links"]:
                    cited_by = first_result["inline_links"]["cited_by"]
                    if "total" in cited_by:
                        return cited_by["total"]
            
            return None
            
        except Exception as e:
            print(f"Failed to get citations: {title} - {e}")
            return None
    
    def get_arxiv_link(self, title):
        """        
        Args:
            title: paper title

        Returns:
            str: ArXiv link, or None if failed
        """
        try:
            search = arxiv.Search(
                query=f'ti:"{title}"',  # search in title
                max_results=3,
                sort_by=arxiv.SortCriterion.Relevance
            )
            results = list(search.results())
            if results:
                return results[0].entry_id
            
            
            # if no exact title match, do a broader search
            search = arxiv.Search(
                query=title.replace(':', '').replace('-', ' '),
                max_results=3,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = list(search.results())
            if results:
                return results[0].entry_id
            
            return None
            
        except Exception as e:
            print(f"Failed to get ArXiv link: {title} - {e}")
            return None
    
    def get_github_link(self, title):
        """        
        Args:
            title: paper title

        Returns:
            str: GitHub link, or None if failed
        """
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                'q': title,
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data['total_count'] > 0:
                    return data['items'][0]['html_url']
            
            return None
            
        except Exception as e:
            print(f"Failed to get GitHub link: {title} - {e}")
            return None
    
    # def _is_title_similar(self, title1, title2, similarity_threshold=0.7):
    #     """
    #     Simple title similarity check
    #     """
    #     # to lower and remove punctuation
    #     t1 = ''.join(c.lower() for c in title1 if c.isalnum() or c.isspace())
    #     t2 = ''.join(c.lower() for c in title2 if c.isalnum() or c.isspace())
        
    #     words1 = set(t1.split())
    #     words2 = set(t2.split())
        
    #     # compute intersection ratio
    #     if len(words1) == 0 or len(words2) == 0:
    #         return False
        
    #     intersection = words1.intersection(words2)
    #     similarity = len(intersection) / min(len(words1), len(words2))
        
    #     return similarity > similarity_threshold

