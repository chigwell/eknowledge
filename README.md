[![PyPI version](https://badge.fury.io/py/eknowledge.svg)](https://badge.fury.io/py/eknowledge)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/eknowledge)](https://pepy.tech/project/eknowledge)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://www.linkedin.com/in/eugene-evstafev-716669181/)

# eknowledge

`eknowledge` is a Python package designed to facilitate the generation of knowledge graphs from textual inputs. It leverages language models to parse text and extract relationships between entities, organizing these relationships into a structured graph format. This tool is ideal for developers, researchers, and anyone interested in structured knowledge extraction from unstructured text.

## Installation

Install `eknowledge` using pip:

```bash
pip install eknowledge
```

## Usage

Here's a simple example to get you started with `eknowledge`. This example demonstrates how to generate a knowledge graph from a given text input using the package.

### Example

First, import the `execute_graph_generation` function from the `eknowledge` package:

```python
from eknowledge import execute_graph_generation
```

You will also need a language model from the `langchain_ollama` package. Here's how to set it up and use it with `eknowledge`:

```python
from langchain_ollama import ChatOllama

# Initialize the language model
MODEL = "llama3.1:8b"
llm = ChatOllama(model=MODEL, max_tokens=1500)

# Define your input text
input_text = "The quick brown fox jumps over the lazy dog."

# Generate the graph
graph = execute_graph_generation(
    text=input_text,
    llm=llm,
    chunk_size=100,
    verbose=True
)

# Output the graph
print(graph)
```

This script will output a knowledge graph based on the relationships identified in the text.

## Contributing

Contributions are welcome! Please read the contributing guide to learn how you can propose bug fixes, improvements, or open issues.

## License

`eknowledge` is MIT licensed, as found in the [LICENSE](https://opensource.org/licenses/MIT) file.
