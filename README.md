[![PyPI version](https://badge.fury.io/py/eknowledge.svg)](https://badge.fury.io/py/eknowledge)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/eknowledge)](https://pepy.tech/project/eknowledge)

# eKnowledge

`eKnowledge` is a Python package designed to facilitate the generation of knowledge graphs from textual inputs using various language models. The package leverages the power of NLP to extract relationships and constructs from code snippets or any other structured text.

## Installation

To install `eKnowledge`, you can use pip:

```bash
pip install eknowledge
```

## Usage

`eKnowledge` supports various language models for processing input text, including locally hosted models and remote API-based models. Below is an example using the `ChatOllama` model, which requires a locally downloaded model from [ollama.com](https://ollama.com/). The recommended model for local usage is "codestral:22b-v0.1-q2_K".

### Example with Local Language Model (ChatOllama)

```python
from eknowledge import execute_graph_generation
from langchain_community.chat_models import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings

# Configure the language model
MISTRAL_MODEL = "codestral:22b-v0.1-q2_K"
MAX_TOKENS = 1500

# Initialize the model with the desired configuration
llm = ChatOllama(model=MISTRAL_MODEL, max_tokens=MAX_TOKENS)

# Sample Python code to process
input_text = """
def factorial(x):
    if x == 1:
        return 1
    else:
        return (x * factorial(x-1))

num = 3
print("The factorial of", num, "is", factorial(num))
"""

# Generate the knowledge graph
embed = HuggingFaceEmbeddings()
graph = execute_graph_generation(input_text, llm, embed, max_attempts=1)

print(graph)
# Output: 
# [
#   {
#       'from_node': 'factorial', 
#       'relation': 'depends_on', 
#       'to_node': 'x'
#   }, 
#   {
#       'from_node': 'factorial', 
#       'relation': 'composed_of', 
#       'to_node': 'factorial(x-1)'
#   }, 
#   {
#       'from_node': 'num', 
#       'relation': 'is_a', 
#       'to_node': '3'
#   }, 
#   {
#       'from_node': 'factorial(num)', 
#       'relation': 'used_for', 
#       'to_node': 'print function'
#   }
#]
```

## Features

- Supports multiple language models including remote API and local executions.
- Extracts structured knowledge from unstructured text.
- Can be used in various domains like academic research, software development, and data science.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/chigwell/eknowledge/issues).

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

The `codestral` model is licensed under [The Mistral AI Non-Production License](https://mistral.ai/news/mistral-ai-non-production-license-mnpl/).
