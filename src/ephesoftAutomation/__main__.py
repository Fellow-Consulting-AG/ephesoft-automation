#!/usr/bin/env python3
import logging
import os.path
import click
import ephesoftAutomation as ea

# TODO update to use multi modules log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")


@click.group()
def main():
    """General section\n
    Please see the documentation on https://data-management-via-infor-ion.readthedocs.io/
    """

    pass


@click.command(
    name="compare",
    help="Section to register a flow on prefect",
)
@click.option(
    "--basedir",
    "-b",
    required=True,
    prompt="Please enter the path for the directory containing configuration files, original values csv files and extraction results",
    help="Base directory path is required."
)
@click.option(
    "--config",
    "-c",
    required=True,
    prompt="Please enter the file name for yml file containing configurations",
    help="File name for .yml file containing configurations"
)
def compare(
        basedir,
        config
):
    is_valid, message = ea.main_compare(
        basedir, config
    )

    if is_valid is False:
        click.secho("Error: ", fg="red", nl=False)
        click.echo(message)


main.add_command(compare)

if __name__ == "__main__":
    main()
