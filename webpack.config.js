var path = require('path');
var webpack = require('webpack');

module.exports = {

    entry: {
        "base":
          "./static/oils/assets/oils/app",
        "dashboard/app":
          "./static/oils/assets/dashboard/app",
        "dashboard/catalog/onestop":
          "./static/oils/assets/catalog/onestop/app",
        "dashboard/catalog/lookup":
          "./static/oils/assets/catalog/lookup",
        "dashboard/circulation/onestop":
          "./static/oils/assets/circulation/onestop/app",
    },
    output: {
        path: path.join(__dirname, './static/oils/dist'),
        filename: "[name].js"
    },
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
    plugins: [
      //new webpack.optimize.UglifyJsPlugin(),
      new webpack.optimize.CommonsChunkPlugin(
          "dashboard/circulation/common.js", [
              "dashboard/circulation/loan",
              "dashboard/circulation/loan_return",
              "dashboard/circulation/loan_renewal"
          ]
      ),
      new webpack.optimize.CommonsChunkPlugin(
          "dashboard/catalog/common.js", [
          ]
      ),
      new webpack.optimize.CommonsChunkPlugin(
          "dashboard/common.js", [
              "dashboard/circulation/common.js"
          ]
      ),
      new webpack.optimize.CommonsChunkPlugin(
          "common.js", [
              "dashboard/common.js"
          ]
      )
    ]
}
