<script lang="ts">
import * as game from './game';


export let board: game.ScoreBoard = new game.ScoreBoard();
export let count: number = 0;

function handleClick() {
  count += 1;
}
</script>

<button on:click={handleClick}>
  Clicked {count} {count === 1 ? 'time' : 'times'}
</button>
