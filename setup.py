from setuptools import setup, find_packages

setup(
    name="hangman-game",
    version="1.0.0",
    description="A Python-based Hangman game with fullscreen support and parallax background",
    author="Jerald Mathews Jomy",
    author_email="jeraldmathewsjomy@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.2",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
