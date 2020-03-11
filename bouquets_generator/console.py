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

    This tool takes file as two input stream\n

    - bouquet designs stream\n
    - flowers stream\n

    Based on these two streams the utility generates a stream:\n
    - bouquet stream

    Examples:
        - input item (bouquet design: `A L 5d 6a 15`\n
        This reads as:\n
        A - bouquet name\n
        L - means large size (might be S - small)\n
        5d 6a ... - {number_of_flowers}{type_of_a_flower}\n
        15 - total number of flowers to be in the bouquet. If bigger than
        sum of flowers, this means any flower of the given size can be added\n

        - input item (flowers stream): `aL`\n
        This reads as:\n
        a - flower of type `a`\n
        L - large size (should match to the bouquet design

        - output item (bouquet):\n
        `A L 5d 6a 4c`\n
        the same as bouquet design without total number of flowers, but flowers
        sum still should be equal to 15 (total number of flowers)

    Common abbreviations:\n
    - bd - bouquets designs\n
    - fl - flowers\n
    - b - bouquets\n



    """
    asyncio.run(
        app(
            src=pathlib.Path(src),
            target=pathlib.Path(target),
            verbose=verbose,
        )
    )
