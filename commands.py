import click
from flask.cli import with_appcontext

from app import db
from app.models import User


@click.group()
def cli():
    pass


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    click.echo('Tables have been created')

@click.command(name='create_admin')
@with_appcontext
def create_admin():
    username = 'superadmin'
    email = 'superadmin@gmail.com'
    is_admin = True
    admin = User(username=username, email=email, admin=is_admin)
    db.session.add(admin)
    db.session.commit()
    click.echo('Admin has been created')


cli.add_command(create_tables)
cli.add_command(create_admin)

if __name__ == "__main__":
    cli()