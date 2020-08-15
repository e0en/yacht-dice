#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from typing import Iterable, List, Dict, Tuple

def calc_upper_score(face: int, dices: List[int]) -> int:
    return sum([x for x in dices if x == face])


def is_full_house(dices: List[int]) -> bool:
    counts = [0 for _ in range(6)]
    for x in dices:
        counts[x - 1] += 1
    return set(counts) > {2, 3}


def is_four_of_a_kind(dices: List[int]) -> bool:
    counts = [0 for _ in range(6)]
    for x in dices:
        counts[x - 1] += 1
    return max(counts) >= 4


def is_small_straight(dices: List[int]) -> bool:
    dice_set = set(dices)
    return (
        {1, 2, 3, 4} <= dice_set or
        {2, 3, 4, 5} <= dice_set or
        {3, 4, 5, 6} <= dice_set
    )


def is_large_straight(dices: List[int]) -> bool:
    sorted_dices = sorted(dices)
    return sorted_dices == [1, 2, 3, 4, 5] or sorted_dices == [2, 3, 4, 5, 6]


def is_yacht(dices: List[int]) -> bool:
    first_dice = dices[0]
    return all([x == first_dice for x in dices])


def roll() -> int:
    return randint(1, 6)
