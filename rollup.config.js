import typescript from "@rollup/plugin-typescript";
import autoPreprocess from 'svelte-preprocess';
import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';

const production = !process.env.ROLLUP_WATCH;


function serve() {
  let server;

  function toExit() {
    if (server) server.kill(0);
  }

  return {
    writeBundle() {
      if (server) return;
      server = require('child_process').spawn('npm', ['run', 'start', '--', '--dev'], {
        stdio: ['ignore', 'inherit', 'inherit'],
        shell: true
      });

      process.on('SIGTERM', toExit);
      process.on('exit', toExit);
    }
  };
}



export default {
  input: 'src/index.ts',
  output: {
    sourcemap: true,
    format: 'iife',
    name: 'yacht_dice',
    file: 'dist/index.js'
  },
  plugins: [
    svelte({
      dev: !production,
      preprocess: autoPreprocess(),
    }),
    resolve({
      browser: true,
      dedupe: ['svelte']
    }),
    !production && serve(),
    typescript({ sourceMap: !production })
  ]
}
