from setuptools import setup, find_packages

setup(
    name='boxcli',
    version='0.1',
    author = "Xu Wang",
    author_email = "xuwang@gmail.com",
    description = ("A command line utility for Box."),
    license = "MIT",
    keywords = "Box cli command",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'ConfigParser',
        'Click',
        'boxsdk[jwt]',
    ],
    entry_points='''
        [console_scripts]
        boxcli=boxcli:boxcli
    ''',
)
