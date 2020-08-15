#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from collections import namedtuple
from typing import Iterable, List, Dict, Tuple

import dice


ScoreItem = namedtuple('ScoreItem', ['score', 'is_filled'])


class ScoreBoard:
    def __init__(self):
        self.scores: Dict[str, ScoreItem] = {
            'aces': ScoreItem(0, False),
            'deuces': ScoreItem(0, False),
            'threes': ScoreItem(0, False),
            'fours': ScoreItem(0, False),
            'fives': ScoreItem(0, False),
            'sixes': ScoreItem(0, False),
            'choice': ScoreItem(0, False),
            'four_of_a_kind': ScoreItem(0, False),
            'full_house': ScoreItem(0, False),
            'small_straight': ScoreItem(0, False),
            'large_straight': ScoreItem(0, False),
            'yacht': ScoreItem(0, False),
        }
        self.upper_names = \
            ['aces', 'deuces', 'threes', 'fours', 'fives', 'sixes']
        self.field_names = list(self.scores.keys())
        self.bonus: int = 0

    def register_score(self, dices: List[int], name: str):
        if self.scores[name].is_filled:
            raise RuntimeError(f'Field {name} is already filled')
        score = self.calc_score(dices, name)
        self.scores[name] = ScoreItem(score, True)
        self.bonus = self.calc_bonus()

    def calc_bonus(self) -> int:
        bonus_fields = ['aces', 'deuces', 'threes', 'fours', 'fives', 'sixes']
        upper_sum = sum([self.scores[x].score for x in bonus_fields])
        if upper_sum >= 63:
            return 35
        return 0

    @staticmethod
    def calc_score(dices: List[int], name: str) -> int:
        if name == 'aces':
            return dice.calc_upper_score(1, dices)
        elif name == 'deuces':
            return dice.calc_upper_score(2, dices)
        elif name == 'threes':
            return dice.calc_upper_score(3, dices)
        elif name == 'fours':
            return dice.calc_upper_score(4, dices)
        elif name == 'fives':
            return dice.calc_upper_score(5, dices)
        elif name == 'sixes':
            return dice.calc_upper_score(6, dices)
        elif name == 'choice':
            return sum(dices)
        elif name == 'full_house':
            return int(dice.is_full_house(dices)) * sum(dices)
        elif name == 'four_of_a_kind':
            return(dice.is_four_of_a_kind(dices)) * sum(dices)
        elif name == 'small_straight':
            return int(dice.is_small_straight(dices)) * 15
        elif name == 'large_straight':
            return int(dice.is_large_straight(dices)) * 30
        elif name == 'yacht':
            return int(dice.is_yacht(dices)) * 50
        else:
            raise ValueError(f'Unknown name {name}')

    def to_str(self):
        lines = list()

        upper_sum = 0
        for name in self.upper_names:
            s = self.scores[name]
            upper_sum += s.score
            lines.append(f'{name}\t{s.score}')
        lines.append('----------------------------')
        lines.append(f'upper sum = {upper_sum}')
        lines.append(f'bonus = {self.bonus}')
        lines.append('----------------------------')
        for name, s in self.scores.items():
            if name not in self.upper_names:
                lines.append(f'{name}\t{s.score}')
        lines.append('----------------------------')
        lines.append(f'total = {self.calc_total_score()}')
        return '\n'.join(lines)

    def calc_total_score(self):
        return self.bonus + sum([s.score for s in self.scores.values()])


def show_dices(dices: List[int], fix_idx: List[int]) -> str:
    result = list()
    for i, x in enumerate(dices):
        if i in fix_idx:
            result.append(f'[{x}]')
        else:
            result.append(f' {x} ')
    return ' '.join(result)


def choose_fix_dices(dices: List[int], fix_idx: List[int]) -> List[int]:
    result = list(fix_idx)
    while True:
        print(show_dices(dices, result))
        idx = input('choose dice index to toggle ([1~5], q to finish): ')
        idx = idx.lower().strip()
        if len(idx) != 1 or idx not in '12345q':
            print('wrong input')
            continue
        if idx == 'q':
            break
        elif idx in '12345':
            idx = int(idx) - 1
            if idx in result:
                result = [i for i in result if i != idx]
            else:
                result = sorted(result + [idx])
    return result


def ask_re_roll() -> bool:
    while True:
        answer = input('Re-roll? [y/n]: ')
        answer = answer.lower()
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print('wrong input')


def choose_name(board: ScoreBoard, dices: List[int]) -> str:
    scores = list()
    for name in board.field_names:
        if not board.scores[name].is_filled:
            scores.append((name, board.calc_score(dices, name)))

    for i, (n, s) in enumerate(scores):
        print(f'{i + 1}) {n} ({s} points)')

    while True:
        idx = input(f'Choose a field name ([1~{len(scores)}]): ')
        idx = int(idx.lower().strip())
        if not (1 <= idx <= len(scores)):
            print('wrong input')
        else:
            return scores[idx - 1][0]


if __name__ == '__main__':
    board = ScoreBoard()
    for i_turn in range(12):
        print(f'# Turn {i_turn + 1}')
        print(board.to_str())
        fix_idx = list()
        dices = [dice.roll() for _ in range(5)]
        for i_draw in range(3):
            dices = [x if i in fix_idx else dice.roll() for i, x in enumerate(dices)]
            print(f'\n## draw {i_draw + 1}')
            print(show_dices(dices, fix_idx))
            if i_draw == 2 or not ask_re_roll():
                break
            fix_idx = choose_fix_dices(dices, fix_idx)
        name = choose_name(board, dices)
        print(dices, name)
        board.register_score(dices, name)
    print(board.to_str())
