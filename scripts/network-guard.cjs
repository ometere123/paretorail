#!/usr/bin/env node
const cp = require('child_process');
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const local = path.join(root, 'node_modules', '.bin', process.platform === 'win32' ? 'genlayer.cmd' : 'genlayer');
if (!fs.existsSync(local)) throw new Error('Missing local genlayer@0.39.1. Run npm install. Never use global CLI.');
const pkg = require(path.join(root,'node_modules','genlayer','package.json'));
if (pkg.version !== '0.39.1') throw new Error(`WRONG_CLI ${pkg.version}`);
const r = cp.spawnSync(local, ['network', 'info'], {
  encoding: 'utf8',
  cwd: root,
  env: process.env,
  shell: process.platform === 'win32',
});
if (r.error) throw new Error(`network info failed: ${r.error.message}`);
if (r.status !== 0) throw new Error(`network info failed: ${r.stderr}`);
const output = r.stdout + r.stderr;
if (!/studionet/i.test(output) || !/61999/.test(output) || !/studio\.genlayer\.com\/api/.test(output) || /studio-dev|studio-next|61997/i.test(output)) {
  throw new Error(`WRONG_NETWORK. Must be stable studionet 61999 https://studio.genlayer.com/api. Actual: ${output}`);
}
console.log('Pinned CLI 0.39.1 + studionet 61999 + stable RPC verified.');
