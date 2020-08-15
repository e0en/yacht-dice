#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from collections import namedtuple
from typing import Iterable, List, Dict, Tuple

import dice


class ScoreBoard:
    def __init__(self):
        self.fields: List[dice.Field] = [
            dice.Aces(),
            dice.Deuces(),
            dice.Threes(),
            dice.Fours(),
            dice.Fives(),
            dice.Sixes(),
            dice.Choice(),
            dice.FullHouse(),
            dice.FourOfAKind(),
            dice.SmallStraight(),
            dice.LargeStraight(),
            dice.Yacht(),

        ]
        self.upper_idx = [0, 1, 2, 3, 4, 5]
        self.lower_idx = [6, 7, 8, 9, 10, 11]
        self.bonus: int = 0

    def register(self, dices: List[int], field_idx: int):
        field = self.fields[field_idx]
        if field.is_filled:
            raise RuntimeError(f'Field {field.name} is already filled')
        field.register_dice(dices)
        self.bonus = self.calc_bonus()

    def calc_bonus(self) -> int:
        upper_sum = sum([self.fields[i].score for i in self.upper_idx])
        if upper_sum >= 63:
            return 35
        return 0

    def to_str(self):
        lines = list()

        upper_sum = 0
        for i in self.upper_idx:
            f = self.fields[i]
            upper_sum += f.score
            lines.append(f'{f.name}\t{f.score}')
        lines.append('----------------------------')
        lines.append(f'upper sum = {upper_sum}')
        lines.append(f'bonus = {self.bonus}')
        lines.append('----------------------------')
        for i in self.lower_idx:
            f = self.fields[i]
            lines.append(f'{f.name}\t{f.score}')
        lines.append('----------------------------')
        lines.append(f'total = {self.calc_total_score()}')
        return '\n'.join(lines)

    def calc_total_score(self):
        return self.bonus + sum([f.score for f in self.fields])


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


def choose_field(board: ScoreBoard, dices: List[int]) -> int:
    scores = list()
    for i, f in enumerate(board.fields):
        if not f.is_filled:
            scores.append((i, f.calc_score(dices)))

    for i_score, (i, s) in enumerate(scores):
        print(f'{i_score + 1}. {board.fields[i].name} ({s} points)')

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
        field_idx = choose_field(board, dices)
        print(dices)
        board.register(dices, field_idx)
    print(board.to_str())
