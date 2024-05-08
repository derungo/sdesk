from setuptools import setup, find_packages

setup(
    name='sdesk',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sdesk = sdesk.main:main', 
        ],
    },
    author='Your Name',
    author_email='patrick.aiken@gmail.com',
    description='A utility to manage Snap desktop files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/sdesk',
    install_requires=[
        # no third-party dependencies
    ],
    classifiers=[
        
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)