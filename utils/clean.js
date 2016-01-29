import del from 'del';

async function clean(){
  console.log("Cleaning");
  await del(['static/oils/dist/*']);
}

export default clean;
