
from setuptools import setup, find_packages

setup(
    name='light_server',
    version='0.1',
    author='alexlexx',
    author_email='alexlexx1@gmail.com',
    packages=find_packages(),
    license='GPL',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'light_server = light_server.server:main'
    	],
    },
    package_data={
        'light_server': [
            'templates/*.*'
	]
    },
)
