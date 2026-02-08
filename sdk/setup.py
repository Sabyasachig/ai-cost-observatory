from setuptools import setup, find_packages

setup(
    name="ai-cost-observatory",
    version="0.1.0",
    description="Open-source AI observability layer for agentic systems",
    author="Sabyasachi Ghosh",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
    ],
    extras_require={
        "langchain": ["langchain>=0.1.0", "langchain-openai>=0.0.2"],
        "llamaindex": ["llama-index>=0.9.0"],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
