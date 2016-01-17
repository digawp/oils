import webpack from 'webpack';
import webpackConfig from '../webpack.config';

async function bundle(){
    console.log("Bundling");
    var compiler = webpack(webpackConfig);
    compiler.run((err, stats)=>{});
}

export default bundle;
