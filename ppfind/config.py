#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPFind config management module

save and manage user configurations, including API keys and default column settings
"""

import json
from pathlib import Path


class ConfigManager:
    """
    Config dict:
    ```
    {
        'api_key': str,         # SerpAPI API key
        'title_col': str,       # CSV title column name
        'citation_col': str,    # CSV citation column name
        'arxiv_col': str,       # CSV arXiv link column name
        'github_col': str       # CSV GitHub link column name
    }
    ```
    """
    
    def __init__(self):
        # config file path (in user's home directory)
        self.config_dir = Path.home() / '.ppfind'
        self.config_file = self.config_dir / 'config.json'

        # default config
        self.default_config = {
            'api_key': None,
            'title_col': 'title',
            'citation_col': 'citations',
            'arxiv_col': 'arxiv_link',
            'github_col': 'github_link'
        }
        
        self.config_dir.mkdir(exist_ok=True)
    
    def load_config(self):
        """        
        Returns:
            dict: config dictionary
        """
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            # merge config
            merged_config = self.default_config.copy()
            merged_config.update(config)
            return merged_config
        else:
            return self.default_config.copy()
    
    def save_config(self, config):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    
    def set_config(self, key, value):
        """
        Set single config value
        """
        config = self.load_config()
        config[key] = value
        return self.save_config(config)
    
    def get_config(self, key=None):
        """
        Get single config value or config dict
        
        Args:
            key: config key, if None return all config

        Returns:
            config value or dict
        """
        config = self.load_config()
        if key is None:
            return config
        return config.get(key)
    
    def show_config(self):
        config = self.load_config()
        
        print(f"Config file: {self.config_file}\n")
        
        # API Key (masked)
        api_key = config.get('api_key')
        if api_key:
            masked_key = api_key[:8] + '*' * (len(api_key) - 16) + api_key[-8:] if len(api_key) > 16 else '*' * len(api_key)
            print(f"    - API Key: \t\t{masked_key}")
        else:
            print("    - API Key: \t\tNot set")
        
        print(f"    - Title Column:\t{config.get('title_col')}")
        print(f"    - Citation Column:\t{config.get('citation_col')}")
        print(f"    - ArXiv Column:\t{config.get('arxiv_col')}")
        print(f"    - GitHub Column:\t{config.get('github_col')}")

    def reset_config(self):
        return self.save_config(self.default_config.copy())
    
    def validate_api_key(self, api_key):
        """
        Validate API key format
        """
        if not api_key:
            return False

        # Basic length check (SerpAPI key is usually a 64-character hexadecimal string)
        if len(api_key) < 32:
            return False

        # Check for valid characters
        valid_chars = set('0123456789abcdefABCDEF')
        if not all(c in valid_chars for c in api_key):
            return False
        
        return True


# Global config manager instance
config_manager = ConfigManager()
