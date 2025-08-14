# File: src/sesh/cli.py
#
# Description: This file contains the main CLI application. It handles
# user input, processes it and passes it on to the appropriate handlers.

import click

@click.group()
def main():
    pass

@main.command()
def start():
    click.echo("start sesh")

@main.command()
def stop():
    click.echo("stop sesh")

@main.command()
def status():
    click.echo("show sesh status")

