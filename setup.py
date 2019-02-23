from setuptools import setup, find_packages

setup(
    name='sqla-views',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/spitfiredd/sqla-views.git',
    author='Daniel Donovan',
    author_email='spitfiredd@gmail.com',
    include_package_data=True,
    install_requires=[
        'sqlalchemy',
    ],
)
