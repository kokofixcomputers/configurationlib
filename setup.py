from setuptools import setup, find_packages

setup(
    name='configurationlib',
    version='1.1.0',
    author='kokodev',
    author_email='koko@kokodev.cc',
    description='A simple configuration manager',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pyyaml',  # Specify PyYAML as a dependency
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)