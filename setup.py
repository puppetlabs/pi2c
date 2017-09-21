from setuptools import setup, find_packages


setup(
    name='pi2c',
    version='0.1.18',
    packages=find_packages(),
    install_requires=[
        'python-icinga2api>=0.3.0.1',
        'requests',
        ],
    entry_points={
        'console_scripts': [
            'pi2c = pi2c.__main__:main',
            'verify_down = pi2c.verify_down:main',
        ]
    },
    author='Matt Kirby',
    author_email='kirby@puppet.com',
    description='A CLI tool for icinga2 api interactions',
    license='Apache License 2.0',
    url='github.com:mattkirby/pi2c'
)
