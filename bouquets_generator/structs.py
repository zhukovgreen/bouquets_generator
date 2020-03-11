import logging
import re
from copy import copy
from enum import Enum
from typing import Dict

import attr

logger = logging.getLogger(__file__)

FLOWERS_REG = re.compile(r"(\d+)([a-z])")
BD_REG = re.compile(r"([A-Z])([L|S])((?:\d+[a-z])+)(\d+)")


class FSize(Enum):
    small: str = "small"
    large: str = "large"

    @classmethod
    def from_str(cls, s: str) -> "FSize":
        if s not in ("S", "L"):
            raise ValueError(
                f"Bouquet should be either `S` or `L`." f" Got {repr(s)}"
            )
        return cls.large if s == "L" else cls.small


class FType(Enum):
    a: str = "a"
    b: str = "b"
    c: str = "c"
    d: str = "d"
    r: str = "r"
    t: str = "t"
    any: str = "any"

    @classmethod
    def from_str(cls, s: str) -> "FType":
        try:
            return cls(s)
        except ValueError:
            raise ValueError(
                f"Flower type can be any of"
                f" {repr(list(cls))}, got {repr(s)} instead."
            )


@attr.dataclass(frozen=True)
class Flower:
    size: FSize = attr.ib()
    type: FType = attr.ib()

    @classmethod
    def from_str(cls, s: str) -> "Flower":
        return cls(size=FSize.from_str(s[1]), type=FType.from_str(s[0]))


@attr.dataclass
class BouquetDesign:
    name: str = attr.ib()
    flowers: Dict[Flower, int] = attr.ib()
    total_num_of_flowers: int = attr.ib()

    @classmethod
    def from_str(cls, s: str) -> "BouquetDesign":
        bd_match = BD_REG.match(s)
        if not bd_match:
            raise ValueError(
                f"Incompatible string repr. Should be of form"
                f" AL8d10r5t30, got {repr(s)}"
            )
        name = bd_match.group(1)
        flowers = {
            Flower.from_str(fl_match.group(2) + bd_match.group(2)): int(
                fl_match.group(1)
            )
            for fl_match in FLOWERS_REG.finditer(bd_match.group(3))
        }
        total_num = int(bd_match.group(4))
        any_flowers_num = total_num - sum(flowers.values())
        if any_flowers_num:
            flowers[
                Flower(size=FSize.from_str(bd_match.group(2)), type=FType.any)
            ] = any_flowers_num
        return cls(name=name, flowers=flowers, total_num_of_flowers=total_num,)


@attr.dataclass
class Bouquet:
    name: str = attr.ib()
    design: BouquetDesign = attr.ib()
    flowers: Dict[Flower, int] = attr.ib(factory=dict)
    _required_flowers: Dict[Flower, int] = attr.ib(init=False)

    def __attrs_post_init__(self):
        self._required_flowers = copy(self.design.flowers)

    async def use(self, flower: Flower) -> None:
        try:
            origin_flower = flower
            if flower not in self._required_flowers:
                flower = Flower(size=flower.size, type=FType.any)
            self._required_flowers[flower] -= 1
        except KeyError:
            logger.debug(
                f"Flower {repr(flower)} is incompatible with the"
                f" bouquet design {self.design}"
            )
            raise
        else:
            self.flowers[origin_flower] = (
                self.flowers.get(origin_flower, 0) + 1
            )
            logger.debug(f"Flower matched: {repr(origin_flower)}")
            if not self._required_flowers[flower]:
                del self._required_flowers[flower]
                logger.debug(f"Flowers of type {repr(flower)} completed")

    @property
    def is_ready(self):
        return not self._required_flowers

    def to_str(self):
        return (
            self.name
            + ("L" if next(iter(self.flowers)).size == FSize.large else "S")
            + "".join(str(v) + f.type.value for f, v in self.flowers.items())
        )
