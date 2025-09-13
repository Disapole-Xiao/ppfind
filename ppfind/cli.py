#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import time
import pandas as pd
from tqdm import tqdm
from .core import PaperInfoFetcher
from .config import config_manager

def parse_args():
    # Create main parser
        parser = argparse.ArgumentParser(
            description='ppfind - paper citations & links finder',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=False,
            epilog="""
Examples:
  ppfind i                                  # Interactive mode
  ppfind q "Attention Is All You Need"      # Query single paper
  ppfind f papers.csv                       # Process file
  ppfind f papers.xlsx --title-col "Paper Title"  # Specify title column
  
  ppfind config --api-key YOUR_API_KEY        # Set API key
  ppfind config --title-col "Paper Title"     # Set default title column
  ppfind config --show                        # Show current config
  ppfind config --reset                       # Reset to defaults
        """
    )
    
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Interactive subcommand
        parser_interactive = subparsers.add_parser(
            'i', 
            help='Enter interactive mode'
        )
        parser_interactive.add_argument('--api-key',
                                    help='SerpAPI key for this session')
        parser_interactive.set_defaults(func=cmd_interactive)
        
        # Query subcommand
        parser_query = subparsers.add_parser(
            'q',
            help='Query paper titles'
        )
        parser_query.add_argument('titles', nargs='+', metavar='TITLE',
                                help='Paper titles to query')
        parser_query.add_argument('--api-key',
                                help='SerpAPI key for this session')
        parser_query.set_defaults(func=cmd_query)
        
        # File subcommand
        parser_file = subparsers.add_parser(
            'f',
            help='Process CSV or XLSX file'
        )
        parser_file.add_argument('file', metavar='FILE',
                            help='CSV or XLSX file to process')
        parser_file.add_argument('--title-col',
                            help='Title column name in file')
        parser_file.add_argument('--citation-col',
                            help='Citation column name in file')
        parser_file.add_argument('--arxiv-col',
                            help='ArXiv link column name in file')
        parser_file.add_argument('--github-col',
                            help='GitHub link column name in file')
        parser_file.add_argument('--api-key',
                            help='SerpAPI key for this session')
        parser_file.set_defaults(func=cmd_file)
        
        # Config subcommand
        parser_config = subparsers.add_parser(
            'config',
            help='Manage PPFind configuration'
        )
        parser_config.add_argument('--api-key',
                                help='Set SerpAPI key')
        parser_config.add_argument('--title-col',
                                help='Set default title column name (default: title)')
        parser_config.add_argument('--citation-col',
                                help='Set default citation column name (default: citations)')
        parser_config.add_argument('--arxiv-col',
                                help='Set default ArXiv column name (default: arxiv_link)')
        parser_config.add_argument('--github-col',
                                help='Set default GitHub column name (default: github_link)')
        parser_config.add_argument('--show', action='store_true', dest='show_config',
                                help='Show current configuration')
        parser_config.add_argument('--reset', action='store_true', dest='reset_config',
                                help='Reset configuration to defaults')
        parser_config.set_defaults(func=cmd_config)

        # Parse arguments
        args = parser.parse_args()
        
        # If no command provided, show help
        if not hasattr(args, 'func'):
            parser.print_help()
            sys.exit(1)

        return args

def cmd_config(args):

    if args.show_config:
        config_manager.show_config()
        return
    
    if args.reset_config:
        try:
            config_manager.reset_config()
            print("Configuration reset to defaults")
        except Exception as e:
            print(f"Failed to reset configuration: {e}")
        return

    # Set config options
    config_updated = False
    
    if args.api_key:
        if config_manager.validate_api_key(args.api_key):
            config_manager.set_config('api_key', args.api_key)
            print("API key updated successfully")
            config_updated = True
        else:
            print("Error: Invalid API key format")
            return
    
    if args.title_col:
        config_manager.set_config('title_col', args.title_col)
        print(f"Title column updated to: {args.title_col}")
        config_updated = True
    
    if args.citation_col:
        config_manager.set_config('citation_col', args.citation_col)
        print(f"Citation column updated to: {args.citation_col}")
        config_updated = True
    
    if args.arxiv_col:
        config_manager.set_config('arxiv_col', args.arxiv_col)
        print(f"ArXiv column updated to: {args.arxiv_col}")
        config_updated = True
    
    if args.github_col:
        config_manager.set_config('github_col', args.github_col)
        print(f"GitHub column updated to: {args.github_col}")
        config_updated = True
    
    if not config_updated:
        print("No configuration options provided. Use 'ppfind config --help' to see available options")


def cmd_file(args):

    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' does not exist")
        return
    
    # construct output filename
    filename = args.file
    path, ext = os.path.splitext(filename)
    output_file = path + '_new' + ext

    print(f"Reading file: {filename}")
    
    # read file
    try:
        if ext.lower() == '.csv':
            df = pd.read_csv(filename, encoding='utf-8')
        elif ext.lower() == '.xlsx':
            df = pd.read_excel(filename)
        else:
            print("Error: Unsupported file format. Only CSV and XLSX are supported.")
            return
    except Exception as e:
        print(f"Error: Failed to read file: {e}")
        return
    
    print(f"Read {len(df)} records")

    title_col = args.title_col
    citation_col = args.citation_col
    arxiv_col = args.arxiv_col
    github_col = args.github_col

    # Check if title column exists
    if title_col not in df.columns:
        print(f"Error: Specified title column '{title_col}' does not exist")
        print(f"Available columns: {list(df.columns)}")
        return
    
    # Check and add missing columns
    for col in [citation_col, arxiv_col, github_col]:
        if col not in df.columns:
            df[col] = None
        df[col] = df[col].astype('object')
    
    fetcher = PaperInfoFetcher(args.api_key)

    # Process each row
    pbar  = tqdm(total=len(df), unit='paper', desc='Processing')
    for index, row in df.iterrows():
        title = row[title_col]
        if pd.isna(title) or title.strip() == '':
            continue

        # Get citations
        if pd.isna(row[citation_col]) or row[citation_col] == '':
            citations = fetcher.get_citations_from_scholar(title)
            if citations is not None:
                df.at[index, citation_col] = citations

        # Get ArXiv link
        if pd.isna(row[arxiv_col]) or row[arxiv_col] == '':
            arxiv_link = fetcher.get_arxiv_link(title)
            if arxiv_link:
                df.at[index, arxiv_col] = arxiv_link

        # Get GitHub link
        if pd.isna(row[github_col]) or row[github_col] == '':
            github_link = fetcher.get_github_link(title)
            if github_link:
                df.at[index, github_col] = github_link
        
        pbar.update(1)
        time.sleep(0.1)  # To avoid hitting rate limits
    pbar.close()

    # Save results
    if ext.lower() == '.csv':
        df.to_csv(output_file, index=False, encoding='utf-8')
    elif ext.lower() == '.xlsx':
        df.to_excel(output_file, index=False)

    print(f"\nProcessing complete! Results saved to: {output_file}")


def cmd_interactive(args):

    api_key = args.api_key
    fetcher = PaperInfoFetcher(args.api_key)

    print("Enter paper titles to query citations and related links")
    print("Type 'quit' or 'q' to exit")
    
    while True:
        try:
            title = input("### ").strip()
            
            if title.lower() in ['quit', 'q']:
                print("exit")
                break
            
            if not title:
                print("Please enter a paper title")
                continue
            
            # add loading indicator
            citations = fetcher.get_citations_from_scholar(title)
            arxiv_link = fetcher.get_arxiv_link(title)
            github_link = fetcher.get_github_link(title)

            print(f"  - Citations: {citations}")
            print(f"  - ArXiv Link: {arxiv_link}")
            print(f"  - GitHub Link: {github_link}")
            
        except KeyboardInterrupt:
            print()
            continue
        except Exception as e:
            print(f"Error occurred during query: {e}")


def cmd_query(args):
    """Handle query command"""
    fetcher = PaperInfoFetcher(args.api_key)

    for title in args.titles:
        citations = fetcher.get_citations_from_scholar(title)
        arxiv_link = fetcher.get_arxiv_link(title)
        github_link = fetcher.get_github_link(title)

        print(f"### {title}")
        print(f"  - Citations: {citations}")
        print(f"  - ArXiv Link: {arxiv_link}")
        print(f"  - GitHub Link: {github_link}")
        print()


def main():
    try:
        args = parse_args()
        
        if args.command != 'config':
            # merge config
            config = config_manager.load_config()
            for k,v in config.items():
                if hasattr(args, k) and getattr(args, k) is None:
                    setattr(args, k, v)
            
            # check api key
            api_key = getattr(args, 'api_key', None)
            if not api_key:
                print("Error: No API key found")
                print("Please set your SerpAPI key using one of these methods:")
                print("    1. Save permanently: 'ppfind config --api-key YOUR_API_KEY'")
                print(f"    2. Use temporarily: 'ppfind {' '.join(sys.argv[1:])} --api-key YOUR_API_KEY'")
                print("\nGet your free API key at: https://serpapi.com/")
                sys.exit(1)

        # Execute the selected command
        args.func(args)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt")
    except Exception as e:
        print(f"Program execution error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    
    main()
