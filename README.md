[![PyPI version](https://badge.fury.io/py/eknowledge.svg)](https://badge.fury.io/py/eknowledge)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/eknowledge)](https://pepy.tech/project/eknowledge)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://www.linkedin.com/in/eugene-evstafev-716669181/)

# eknowledge

`eknowledge` is a Python package designed to facilitate the generation of knowledge graphs from textual inputs. It leverages language models to parse text and extract relationships between entities, organizing these relationships into a structured graph format. This tool is ideal for developers, researchers, and anyone interested in structured knowledge extraction from unstructured text.

## Installation

Install `eknowledge` using pip:

```bash
pip install eknowledge langchain_llm7
```

## Usage

Here's a simple example to get you started with `eknowledge`. This example demonstrates how to generate a knowledge graph from a given text input using the package.

### Example

```python
from eknowledge import execute_graph_generation
from langchain_llm7 import ChatLLM7

# Initialize the language model
MODEL = "deepseek-r1"
llm = ChatLLM7(model=MODEL)

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
# > Splitting text into 1 chunks of size 100 words.
# > Processing chunk 1/1...
# > Nodes successfully processed in chunk 1/1.
# > [{'from': 'quick brown fox', 'relationship': 'interacts_with', 'to': 'lazy dog'}]
```

This script will output a knowledge graph based on the relationships identified in the text.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for any bugs, features, or improvements you would like to see.

## License

`eknowledge` is MIT licensed, as found in the [LICENSE](https://opensource.org/licenses/MIT) file.
