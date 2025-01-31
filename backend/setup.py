"""
Setup file for the Agentique backend package.
"""
from setuptools import setup, find_packages

setup(
    name="agentique",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "telethon",
        "python-dotenv",
        "fastapi",
        "uvicorn[standard]",
        "pinecone-client",
        "openai>=1.0.0",
    ],
) 