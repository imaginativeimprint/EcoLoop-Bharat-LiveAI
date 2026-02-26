from setuptools import setup, find_packages

setup(
    name="ecoloop-bharat",
    version="1.0.0",
    author="Team TechnoForge",
    author_email="team@technoforge.com",
    description="Real-time Circular Economy Tracker for Bharat",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pathway>=0.11.0",
        "streamlit>=1.28.1",
        "pandas>=2.0.3",
        "plotly>=5.17.0",
    ],
    python_requires=">=3.11",
)
