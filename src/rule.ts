abstract class Field {
    score: number;
    is_filled: boolean;
    name: string;
    abstract calc_score(dices: Array<number>): number;

    register_dice(dices: Array<number>): void {
        if (this.is_filled) {
            throw new Error("Cannot register dice more than once");
        }
        this.is_filled = true;
        this.score = this.calc_score(dices);
    }
}

abstract class Upper extends Field {
    protected face: number;

    calc_score(dices: Array<number>): number {
        return dices.filter(d => d == this.face).reduce((sum, d) => sum + d);
    }
}

class Aces extends Upper {
    face: number = 1;
    name: string = "Aces";
}

class Deuces extends Upper {
    face: number = 2;
    name: string = "Deuces";
}

class Threes extends Upper {
    face: number = 3;
    name: string = "Threes";
}

class Fours extends Upper {
    face: number = 4;
    name: string = "Fours";
}

class Fives extends Upper {
    face: number = 5;
    name: string = "Fives";
}

class Sixes extends Upper {
    face: number = 6;
    name: string = "Sixes";
}

class Choice extends Field {
    name = "Choice";
    calc_score(dices: Array<number>): number {
        return dices.reduce((sum, d) => sum + d);
    }
}

class FullHouse extends Field {
    name = "FullHouse";
    calc_score(dices: Array<number>): number {
        let counts: number[] = [0, 0, 0, 0, 0, 0];
        for (const x of dices) {
            counts[x - 1] += 1;
        }

        if (counts.includes(2) && counts.includes(3)) {
            return dices.reduce((sum, d) => sum + d);
        }
        return 0;
    }
}

class FourOfAKind extends Field {
    name = "Four of a kind";
    calc_score(dices: Array<number>): number {
        let counts: number[] = [0, 0, 0, 0, 0, 0];
        for (const x of dices) {
            counts[x - 1] += 1;
        }
        if (Math.max(...counts) >= 4) {
            return dices.reduce((sum, d) => sum + d);
        }
        return 0;
    }
}

class SmallStraight extends Field {
    name = "Small straight";
    calc_score(dices: Array<number>): number {
        const straights = [
            [1, 2, 3, 4],
            [2, 3, 4, 5],
            [3, 4, 5, 6],
        ]
        for (const straight of straights) {
            if (straight.every(n => dices.includes(n))) {
                return 15;
            }
        }
        return 0;
    }
}

class LargeStraight extends Field {
    name = "Small straight";
    calc_score(dices: Array<number>): number {
        const sorted_dices = dices.sort();
        if (sorted_dices == [1, 2, 3, 4, 5] || sorted_dices == [2, 3, 4, 5, 6]) {
            return 30;
        }
        return 0;
    }
}

class Yacht extends Field {
    name = "Yacht";
    calc_score(dices: Array<number>): number {
        const first_dice = dices[0];
        if (dices.every(d => d == first_dice)) {
            return 50;
        }
        return 0;
    }
}

export {
    Field, Aces, Deuces, Threes, Fours, Fives, Sixes,
    Choice, FullHouse, FourOfAKind, SmallStraight, LargeStraight, Yacht
};
