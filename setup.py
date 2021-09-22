from setuptools import setup

setup(
    name='GMS-uploader',
    version='0.1.1',
    packages=[''],
    install_requires=[
        'PySide6',
        'pyqtdarktheme',
        'HCPInterface',
        'pandas',
        'pandas-schema',
        'python-dateutil',
        'setuptools',
        'PyYAML'
    ],
    url='',
    license='MIT',
    author='parlar',
    author_email='par.larsson@umu.se',
    description='utility collate and upload metadata and sequences to hcp'
)
