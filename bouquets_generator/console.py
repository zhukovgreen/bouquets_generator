import asyncio
import pathlib

import click

from bouquets_generator import app


@click.command()
@click.option("-v", "--verbose", count=True, help="Verbosity of the tool")
@click.argument("src", type=click.Path(exists=True))
@click.argument("target", type=click.Path())
def main(verbose, src, target):
    """Bouquets design stream as input -> boquets as output.

    This tool takes file as two input stream
    - bouquet designs stream
    - flowers stream

    Based on these two streams the utility generates a stream:
    - bouquet stream
    """
    asyncio.run(
        app(
            src=pathlib.Path(src),
            target=pathlib.Path(target),
            verbose=verbose,
        )
    )
