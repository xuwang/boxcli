from setuptools import setup, find_packages

setup(
    name='boxcli',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'ConfigParser',
        'Click',
        'simplejson',
        'boxsdk[jwt]',
    ],
    entry_points='''
        [console_scripts]
        boxcli=boxcli:boxcli
    ''',
)
