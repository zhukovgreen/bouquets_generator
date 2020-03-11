# Bouquets generator

This is a Cli tool

```
Usage: bouquets [OPTIONS] SRC TARGET
  Bouquets design stream as input -> boquets as output.
  This tool takes file as input. Generates two input stream 
   - bouquet designs stream 
   -  flowers stream
  Based on these two streams the utility generates an output stream:
   - bouquet stream

Options:  -v, --verbose  Verbosity of the tool
  --help         Show this message and exit.
```

# Demo
![gif](./gif.gif)

# Development environment

Run tests:

- [docker] docker-compose run tests
- [local] poetry run pytest


Play with the cli

[in docker]
- docker-compose run cli
- poetry run bouquets --help

[in local]
- poetry install
- poetry shell
- bouquets --help