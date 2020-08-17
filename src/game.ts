import * as rule from './rule';

class ScoreBoard {
    fields: Array<rule.Field> = [
        new rule.Aces(),
        new rule.Deuces(),
        new rule.Threes(),
        new rule.Fours(),
        new rule.Fives(),
        new rule.Sixes(),
        new rule.Choice(),
        new rule.FullHouse(),
        new rule.FourOfAKind(),
        new rule.SmallStraight(),
        new rule.LargeStraight(),
        new rule.Yacht(),
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


function roll_a_dice(): number {
    return Math.floor(Math.random() * 6) + 1;
}

