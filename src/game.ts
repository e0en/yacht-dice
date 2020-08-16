import * as dice from './dice';

class ScoreBoard {
    fields: Array<dice.Field> = [
        new dice.Aces(),
        new dice.Deuces(),
        new dice.Threes(),
        new dice.Fours(),
        new dice.Fives(),
        new dice.Sixes(),
        new dice.Choice(),
        new dice.FullHouse(),
        new dice.FourOfAKind(),
        new dice.SmallStraight(),
        new dice.LargeStraight(),
        new dice.Yacht(),
    ];
    upper_idx: Array<number> = [0, 1, 2, 3, 4, 5];
    lower_idx: Array<number> = [6, 7, 8, 9, 10, 11];
    bonus: number = 0;

    register(dices: Array<number>, field_idx: number): void {
        this.fields[field_idx].register_dice(dices);
        this.bonus = this.calc_bonus();
    }

    calc_bonus(): number {
        const upper_sum = this.upper_idx.map(i => this.fields[i].score)
                                        .reduce((sum, d) => sum + d);
        if (upper_sum >= 63) {
            return 35;
        }
        return 0;
    }
}
