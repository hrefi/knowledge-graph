# Knowledge Graph Agent

## Description

This project aims to transform unstructured data related to a specific entity, such as a company or person, into a structured knowledge graph. Given a query like "Elon Musk," the system collects data from various unstructured sources online and then builds a knowledge graph around that entity.

## Getting Started

### Prerequisites

- Python 3.8+
- Pip or Conda for Python package installation

### Installation

1. Clone the repository to your local machine.
2. Install the required Python packages:
   ```sh
   pip install networkx matplotlib requests tiktoken openai
   ```
3. Set up environment variables (in a .env file) for API keys for OpenAI, Bing, and Crunchbase.

### Usage

1. Data Retrieval: Use the dataRetrieval.py script to fetch data from the web based on your query.
2. Knowledge Extraction: Process the fetched data using nlpProcessing.py to extract entities and their relationships.
3. Graph Construction: Utilize knowledgeGraph.py to construct the knowledge graph from the extracted information.
4. Visualization: With knowledgeGraph.py, the knowledge graph can be visualized within a Python environment using Matplotlib.

## Project Structure

- dataRetrieval.py: Script for web search and data fetching.
- nlpProcessing.py: Module for natural language processing and entity relationship extraction.
- knowledgeGraph.py: Utility for knowledge graph construction and visualization.
- numTokens.py: Module for calculating the number of tokens in strings or chat messages. Useful for optimizing API usage with token limits in mind.
- agent.ipynb: Interactive Jupyter Notebook for demonstration.
- test.ipynb: Script for comparing the execution time of different methods

## Example Workflow

The agent.ipynb Jupyter Notebook provides an interactive platform to demonstrate the project's capabilities. It demonstrates a step-by-step process from data retrieval to graph visualization and provides useful examples.