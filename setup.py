from setuptools import setup, find_packages

setup(
    name="chunking",
    version="0.1",
    description="A library for text chunking and embedding strategies.",
    author="Your Name",
    packages=find_packages(),  # Automatically finds 'chunking' and submodules
    install_requires=[
        "python-dotenv","tiktoken","nltk","openai","transformers","torch","requests","pyyaml"
    ],
    python_requires=">=3.8",
)