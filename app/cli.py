import os
import click
from flask import current_app
from flask.cli import with_appcontext

@click.group()
def translate():
    """Translation and localization commands."""
    pass

@translate.command()
@with_appcontext
def update():
    """Update all languages."""
    if not os.path.exists('messages.pot'):
        os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .')
    os.system('pybabel update -i messages.pot -d app/translations')
    os.unlink('messages.pot')

@translate.command()
@with_appcontext
def compile():
    """Compile all languages."""
    os.system('pybabel compile -d app/translations') 