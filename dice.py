#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from typing import Iterable, List, Dict, Tuple, Optional


class Field:
    def __init__(self):
        self.score: int = 0
        self.is_filled: bool = False
        self.name: str

    def calc_score(self, dices: List[int]) -> int:
        raise NotImplementedError

    def register_dice(self, dices: List[int]):
        if self.is_filled:
            raise RuntimeError('Cannot register dice more than once')
        self.is_filled = True
        self.score = self.calc_score(dices)


class Upper(Field):
    def __init__(self):
        Field.__init__(self)
        self.face: int

    def calc_score(self, dices: List[int]) -> int:
        return sum([x for x in dices if x == self.face])


class Aces(Upper):
    def __init__(self):
        Field.__init__(self)
        self.face: int = 1
        self.name = 'Aces'


class Deuces(Upper):
    def __init__(self):
        Upper.__init__(self)
        self.face: int = 2
        self.name = 'Deuces'


class Threes(Upper):
    def __init__(self):
        Upper.__init__(self)
        self.face: int = 3
        self.name = 'Threes'


class Fours(Upper):
    def __init__(self):
        Upper.__init__(self)
        self.face: int = 4
        self.name = 'Fours'


class Fives(Upper):
    def __init__(self):
        Upper.__init__(self)
        self.face: int = 5
        self.name = 'Fives'


class Sixes(Upper):
    def __init__(self):
        Upper.__init__(self)
        self.face: int = 6
        self.name = 'Sixes'


class Choice(Field):
    def __init__(self):
        Field.__init__(self)
        self.name = 'Choice'

    def calc_score(self, dices: List[int]) -> int:
        return sum(dices)


class FullHouse(Field):
    def __init__(self):
        Field.__init__(self)
        self.name = 'Full house'

    def calc_score(self, dices: List[int]) -> int:
        counts = [0 for _ in range(6)]
        for x in dices:
            counts[x - 1] += 1
        if set(counts) > {2, 3}:
            return sum(dices)
        return 0


class FourOfAKind(Field):
    def __init__(self):
        Field.__init__(self)
        self.name = '4 of a kind'

    def calc_score(self, dices: List[int]) -> int:
        counts = [0 for _ in range(6)]
        for x in dices:
            counts[x - 1] += 1
        if max(counts) >= 4:
            return sum(dices)
        return 0


class SmallStraight(Field):
    def __init__(self):
        Field.__init__(self)
        self.name = 'Small straight'

    def calc_score(self, dices: List[int]) -> int:
        dice_set = set(dices)
        is_matched = (
            {1, 2, 3, 4} <= dice_set or
            {2, 3, 4, 5} <= dice_set or
            {3, 4, 5, 6} <= dice_set
        )
        if is_matched:
            return 15
        return 0


class LargeStraight(Field):
    def __init__(self):
        Field.__init__(self)
        self.name = 'Large straight'

    def calc_score(self, dices: List[int]) -> int:
        sorted_dices = sorted(dices)
        if sorted_dices == [1, 2, 3, 4, 5] or sorted_dices == [2, 3, 4, 5, 6]:
            return 30
        return 0


class Yacht(Field):
    def __init__(self):
        Field.__init__(self)
        self.name = 'Yacht'

    def calc_score(self, dices: List[int]) -> int:
        first_dice = dices[0]
        if all([x == first_dice for x in dices]):
            return 50
        return 0


def roll() -> int:
    return randint(1, 6)
