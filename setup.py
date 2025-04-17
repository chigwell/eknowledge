from setuptools import setup, find_packages


setup(
    name='eknowledge',
    version='2025.4.171239',
    author='Eugene Evstafev',
    author_email='chigwel@gmail.com',
    description='A Python package for executing graph generation from textual inputs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chigwell/eknowledge',
    packages=find_packages(),
    install_requires=[
        'langchain-core==0.3.51',
        'langchain-ollama==0.3.0'
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