import path from 'path';

module.exports = {

    entry: {
        main: "./asset/main",
        circulation_issue: "./asset/circulation/issue",
        circulation_issue_return: "./asset/circulation/issue_return",
        circulation_issue_renewal: "./asset/circulation/issue_renewal"
    },
    output: {
        path: path.join(__dirname, '../static/assets'),
        filename: "[name].js"
    },
    module: {
        loaders: [
            {
                test: /\.less$/,
                loader: "style-loader!css-loader!less-loader"
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
    }
}
