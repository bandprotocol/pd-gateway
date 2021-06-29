from setuptools import find_packages, setup

setup(
    name='pdgateway',
    packages=find_packages(include=['pdgateway']),
    version='0.1.0',
    description='Gateway for Band Protocol\'s Premium Data Source',
    author='Nathachai Jaiboon',
    license='Apache License 2.0',
    install_requires=[
        'flask',
        'requests',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.4'],
    test_suite='tests',
)