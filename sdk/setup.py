from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README
this_directory = Path(__file__).parent.parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="ai-cost-observatory",
    version="1.0.0",
    description="Open-source AI observability layer for agentic systems - Track, analyze, and optimize LLM costs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sabyasachi Ghosh",
    author_email="ghoshsabyasachi0@gmail.com",
    url="https://github.com/Sabyasachig/ai-cost-observatory",
    project_urls={
        "Bug Tracker": "https://github.com/Sabyasachig/ai-cost-observatory/issues",
        "Documentation": "https://github.com/Sabyasachig/ai-cost-observatory#readme",
        "Source Code": "https://github.com/Sabyasachig/ai-cost-observatory",
    },
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
    ],
    extras_require={
        "langchain": ["langchain>=0.1.0", "langchain-openai>=0.0.2"],
        "llamaindex": ["llama-index>=0.9.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: OS Independent",
    ],
    keywords="ai llm observability cost-tracking openai anthropic langchain monitoring analytics",
    license="MIT",
)
