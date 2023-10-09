import sqlite3

# g stores data that might be accessed by multiple functions in one request (so, our connection to the database)
import click
from flask import current_app, g


def get_db():
    # set up a database connection if it doesn't exist
    if "db" not in g:
        # connects to whatever file is pointed to by the DATABASE config key
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        # tells the connection to return rows that behave like dicts so we can access them by name
        g.db.row_factory = sqlite3.Row

    return g.db


# if a connection was created, close it
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


# allows app to read the schema file to set up database
# note: running the init function will clear any existing database
def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# creates a command line command to initialize or clear and reinitialize a database
# note: these aren't used unless they're registered with the app instance
@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    # this will tell you it worked!
    click.echo("Initialized the database.")


# this is where the command line commands are registered with the app!
def init_app(app):
    # tells Flask to call close_db every time it's cleaning up after a response
    app.teardown_appcontext(close_db)
    # adds our init-db command
    app.cli.add_command(init_db_command)
