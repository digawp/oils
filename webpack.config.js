import path from 'path';
import webpack from 'webpack';

module.exports = {

    entry: {
        main:
          "./static/oils/assets/main",
        "dashboard/circulation/issue":
          "./static/oils/assets/circulation/issue",
        "dashboard/circulation/issue_return":
          "./static/oils/assets/circulation/issue_return",
        "dashboard/circulation/issue_renewal":
          "./static/oils/assets/circulation/issue_renewal"
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
      new webpack.optimize.UglifyJsPlugin(),
      new webpack.optimize.CommonsChunkPlugin(
          "dashboard/circulation/common.js", [
              "dashboard/circulation/issue",
              "dashboard/circulation/issue_return",
              "dashboard/circulation/issue_renewal"
          ],
      ),
      new webpack.optimize.CommonsChunkPlugin(
          "dashboard/catalogue/common.js", [
          ],
      ),
      new webpack.optimize.CommonsChunkPlugin(
          "dashboard/common.js", [
              "dashboard/circulation/common.js"
          ],
      ),
      new webpack.optimize.CommonsChunkPlugin(
          "common.js", [
              "dashboard/common.js"
          ],
      )
    ]
}
