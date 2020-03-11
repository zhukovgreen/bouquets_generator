import pathlib

import pytest

from bouquets_generator import app, BouquetDesign, Flower
from bouquets_generator.structs import FSize, FType

TEST_DIR = pathlib.Path(__file__).parent


@pytest.mark.asyncio
async def test_basic():
    await app(TEST_DIR / "sample_simple.txt", TEST_DIR / "output.txt")


def test_bouquet_design():
    assert BouquetDesign.from_str("AL8d10r5t30") == BouquetDesign(
        name="A",
        flowers={
            Flower(size=FSize.large, type=FType.d): 8,
            Flower(size=FSize.large, type=FType.r): 10,
            Flower(size=FSize.large, type=FType.t): 5,
            Flower(size=FSize.large, type=FType.any): 7,
        },
        total_num_of_flowers=30,
    )
    with pytest.raises(ValueError):
        BouquetDesign.from_str("")
