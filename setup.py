from setuptools import setup, find_packages

setup(
    name="phishing-content-generator",
    version="1.0.0",
    description="Phishing content generation system for awareness training using Claude API",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "anthropic>=0.34.2",
        "click>=8.1.7",
        "python-dotenv>=1.0.1",
        "colorama>=0.4.6",
        "pydantic>=2.8.2",
        "requests>=2.32.3",
    ],
    entry_points={
        "console_scripts": [
            "phishing-generator=main:cli",
        ],
    },
    python_requires=">=3.8",
    keywords=["phishing", "security", "training", "claude", "gophish"],
    author="",
    license="MIT",
)