from setuptools import find_packages, setup

# This setup.py is simple because we're using pyproject.toml for configuration
# It only exists to ensure compatibility with older tools

setup(
    name="technical_blog_smolagents",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=open("requirements.txt").read().splitlines(),
    python_requires=">=3.8",
)
