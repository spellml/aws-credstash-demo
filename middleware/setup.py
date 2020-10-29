from setuptools import setup, find_packages

setup(
    name='middleware',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['click', 'credstash'],
    entry_points='''
        [console_scripts]
        middleware=middleware.cli:cli
    ''',
)
