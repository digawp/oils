async function run(fn, opts) {
  console.log(`Starting ${fn.name}`);
  await fn(opts);
  console.log(`Terminating ${fn.name}`);
}


if (process.mainModule.children.length === 0 && process.argv.length > 2) {
  delete require.cache[__filename];
  const module = process.argv[2];
  run(require('./' + module + '.js').default).catch(err => console.error(err.stack));
}


export default run;
