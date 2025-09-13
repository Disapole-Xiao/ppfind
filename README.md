# ppfind - paper citations & links finder

A command-line tool to find paper citations, ArXiv links, and GitHub repository links easily.

[![PyPI version](https://img.shields.io/pypi/v/ppfind)](https://pypi.org/project/ppfind/)

## Features

1. **Citation Fetching**: Get paper citations through Google Scholar API (SerpAPI)
2. **ArXiv Links**: Search and get related paper ArXiv links through ArXiv API  
3. **GitHub Links**: Search and get related code repository links through GitHub REST API
4. **Batch Processing**: Supports CSV & XLSX file batch processing and customized column name
5. **Interactive Mode**: Supports interactive continuous querying

## Installation

### From PyPI (Recommended)

```bash
pip install ppfind
```

### From Source

```bash
git clone https://github.com/Disapole-Xiao/ppfind.git
cd ppfind
pip install -e .
```

## API key

Get a free or paid API Key at [SerpAPI](https://serpapi.com/) for Google Scholar API use. The free plan offers 250 search per month.

## Usage

Type `ppfind --help` or `ppfind <cmd> --help` to see all available options.

### 1. Interactive Mode

```bash
ppfind i
```

### 2. Direct Query

```bash
# Query single paper
ppfind q "Attention Is All You Need"

# Query multiple papers
ppfind q "Attention Is All You Need" "ResNet: Deep Residual Learning for Image Recognition"
```
Output example:
```
### Attention Is All You Need
  - Citations: 193680
  - ArXiv Link: http://arxiv.org/abs/1706.03762v7
  - GitHub Link: https://github.com/jadore801120/attention-is-all-you-need-pytorch
```

**Note**: You may need to wait for a few seconds to get results.

### 3. File Processing

Currenly, CSV and XLSX files are supported. [Here](./example.csv) is an example file.

By default, `ppfind` gets paper titles at `title` column and outputs results to `citations`, `arxiv_link` and `github_link`. Modify this by adding options or in config.

```bash
# Basic usage (output file will be {original_name}_new.csv)
ppfind f examples.csv

# Specify column names
ppfind f papers.xlsx --title-col "Paper Title" --citation-col "Citation Count"
```

### 4. Configuration

Set default options so that you don't have to input options every time.

```bash
# Set options
ppfind config --api-key YOUR_SERP_API_KEY --title-col "Paper Title" --citation-col "Citations" --arxiv-col "Arxiv Link" --github-col "Github Link"

# Show current configuration
ppfind config --show

# Reset to defaults
ppfind config --reset
```

## Notes

- To avoid incorrect matches, please search using the full paper title.
- This tool is intended for reference only. Please confirm the accuracy of the results on your own.