from setuptools import setup, find_packages


setup(
    name='eknowledge',
    version='0.1.4',
    author='Eugene Evstafev',
    author_email='chigwel@gmail.com',
    description='A Python package for executing graph generation from textual inputs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chigwell/eknowledge',
    packages=find_packages(),
    install_requires=[
        'faiss-cpu==1.8.0.post1',
        'huggingface-hub==0.23.4',
        'langchain==0.2.6',
        'langchain-community==0.2.6',
        'langchain-core==0.2.10',
        'langchain-huggingface==0.0.3',
        'langchain-text-splitters==0.2.2',
        'langsmith==0.1.82',
        'packaging==24.1',
        'pydantic==2.7.4',
        'pydantic_core==2.18.4',
        'safetensors==0.4.3',
        'scikit-learn==1.5.0',
        'scipy==1.14.0',
        'sentence-transformers==3.0.1',
        'torch==2.3.1',
        'transformers==4.42.3',
        'typing_extensions==4.12.2'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)