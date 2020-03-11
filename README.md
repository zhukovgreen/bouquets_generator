# Bouquets generator

This is a Cli tool

```
Usage: bouquets [OPTIONS] SRC TARGET
  Bouquets design stream as input -> boquets as output.
  This tool takes file as two input stream
  - bouquet designs stream
  - flowers stream
  Based on these two streams the utility generates a stream:
  - bouquet stream
  Examples:     - input item (bouquet design: `A L 5d 6a 15`
      This reads as:
      A - bouquet name
      L - means large size (might be S - small)
      5d 6a ... - {number_of_flowers}{type_of_a_flower}
      15 - total number of flowers to be in the bouquet. If bigger than
      sum of flowers, this means any flower of the given size can be added
      - input item (flowers stream): `aL`
      This reads as:
      a - flower of type `a`      L - large size (should match to the bouquet design

      - output item (bouquet):
      `A L 5d 6a 4c`
      the same as bouquet design without total number of flowers, but      flowers     sum still should be equal to 15 (total number of flowers)

  Common abbreviations:
  - bd - bouquets designs
  - fl - flowers

  - b - bouquets

Options:
  -v, --verbose  Verbosity of the tool
  --help         Show this message and exit.
```

# Demo
![gif](./gif.gif)

# Development environment

Run tests:

- [docker] docker-compose run tests
- [local] poetry run pytest


Play with the cli

[docker]
- docker-compose run cli
- poetry run bouquets --help

[local]
- poetry install
- poetry shell
- bouquets --help