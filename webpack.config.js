var path = require('path');
var webpack = require('webpack');

const config = {
    module: {
        loaders: [
            {
                test: /\.less$/,
                loaders: [
                    "style-loader",
                    "css-loader",
                    "postcss-loader",
                    "less-loader",
                ],
            },
            {
                test: /\.jsx?$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel',
                query: {
                    presets: ['react', 'es2015']
                }
            }
        ]
    },
    postcss: function (){
        return [require('autoprefixer'),];
    },
};

const dashboardConfig = Object.assign({}, config, {
    entry: {
        "dashboard/app": "./oils/apps/dashboard/assets/app",
    },
    output: {
        path: path.join(__dirname, './oils/apps/dashboard/static/dist'),
        filename: "[name].js"
    },
});

module.exports = [
    dashboardConfig,
];
