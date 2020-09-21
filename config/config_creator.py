from configparser import ConfigParser

config = ConfigParser()

config.add_section('main')
config.set('main', 'KEY', '')
config.set('main', 'SECRET', '')
config.set('main', 'BASE', '')

with open('config.ini', 'w') as f:
    config.write(f)