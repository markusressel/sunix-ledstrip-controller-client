from setuptools import setup, find_packages

setup(
    name='sunix_ledstrip_controller_client',
    version='1.1.0',
    description='A library for controlling the Sunix RGB / RGBWWCW WiFi LED Strip controller',
    license='GPLv3+',
    author='Markus Ressel',
    author_email='mail@markusressel.de',
    url='https://www.markusressel.de',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'construct',
    ]
)
