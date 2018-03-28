from TransHelp import app, db


@app.cli.command()
def initdb():
    db.create_all()


@app.cli.command()
def rmdb():
    db.drop_all()


@app.cli.command()
def reinitdb():
    rmdb()
    initdb()
