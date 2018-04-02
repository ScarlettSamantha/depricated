from TransHelp import app, db
from helpers.guide import compile_all, clear_cache


@app.cli.command()
def recompile():
    clear_cache()
    compile_all()

