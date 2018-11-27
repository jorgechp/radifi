from distutils.core import setup

setup(
    name='Radifi',
    version='0.1.0',
    author='Jorge Chamorro-Padial',
    author_email='jorge@jorgechp.com',
    packages=['api', 'config', 'music', 'planning', 'resources', 'scripts' , 'station', 'tests'],
    scripts=['main.py'],
    entry_points={
        'console_scripts':
            ['radifi_service = radifi_service.__main___:main'
             ]},
    license='LICENSE',
    description='Your own DIY internet radio service.',
    long_description=open('README.rst').read(),
    install_requires=[
        "python-vlc >= 3.0.4106",
        "requests == 2.20.1",
        "Flask-API == 1.0",
        "flask == 1.0.2",
        "validators == 0.12.3",
        "schedule == 0.5.0"
    ],
)