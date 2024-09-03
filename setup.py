from setuptools import setup, find_packages

setup(
    name='weather-cli',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-daemon',
    ],
    entry_points={
        'console_scripts': [
            'weather-cli=weather_cli:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple weather CLI tool',
    url='https://github.com/yourusername/weather-cli',
)