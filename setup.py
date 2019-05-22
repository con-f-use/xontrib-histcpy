from setuptools import setup

setup(
    name='xontrib-histcpy',
    version='0.1',
    url='https://github.com/con-f-use/xontrib-histcpy',
    license='GPLv3',
    author='con-f-use',
    author_email='con-f-use@gmx.net',
    description="Useful aliases and shortcuts for extracting links and text from command output history in xonsh",
    packages=['xontrib'],
    package_dir={'xontrib': 'xontrib'},
    package_data={'xontrib': ['*.xsh']},
    platforms='any',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Desktop Environment',
        'Topic :: System :: Shells',
        'Topic :: System :: System Shells',
    ]
)
