var path = require('path');
var webpack = require('webpack');

const config = {
    resolve: {
        root: [
            path.resolve('./oils/core/assets'),
            path.resolve('./oils/apps/catalog/assets'),
            path.resolve('./oils/apps/circulation/assets'),
            path.resolve('./oils/apps/account/assets'),
            path.resolve('./oils/apps/shelving/assets'),
            path.resolve('./oils/apps/dashboard/assets'),
        ],
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
                loaders: ['babel'],
            },
            {
                test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "url",
                query: {
                    name: "/static/dist/[name].[ext]",
                    limit: "10000",
                    mimetype: "application/font-woff"
                }
            },
            {
                test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "file?name=/static/dist/[name].[ext]"
            }
        ]
    },
    postcss: function (){
        return [require('autoprefixer'),];
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            "window.jQuery": "jquery"
        })
    ],
};

const dashboardConfig = Object.assign({}, config, {
    entry: {
        "dashboard/app": "./oils/apps/dashboard/assets/app",
        "dashboard/menu": "./oils/apps/dashboard/assets/menu",
    },
    output: {
        path: path.join(__dirname, './oils/apps/dashboard'),
        filename: "static/dist/[name].js"
    },
})

const circulationConfig = Object.assign({}, config, {
    entry: {
        "dashboard/circulation/loan": [
            "babel-polyfill",
            "./oils/apps/circulation/assets/dashboard/circulation/loan.js",
            "./oils/apps/circulation/assets/dashboard/circulation/loan.less",
        ],
        "dashboard/circulation/return": [
            "babel-polyfill",
            "./oils/apps/circulation/assets/dashboard/circulation/loan_return.js",
        ],
        "dashboard/circulation/renewal": [
            "babel-polyfill",
            "./oils/apps/circulation/assets/dashboard/circulation/loan_renewal.js",
        ]
    },
    output: {
        path: path.join(__dirname, "./oils/apps/circulation"),
        filename: "static/dist/[name].js"
    }
})

const accountConfig = Object.assign({}, config, {
    entry: {
        "account/registration": [
            "./oils/apps/account/assets/account/registration.js",
        ]
    },
    output: {
        path: path.join(__dirname, "./oils/apps/account"),
        filename: "static/dist/[name].js"
    }
})

const coreConfig = Object.assign({}, config, {
    entry: {
    },
    output: {
        path: path.join(__dirname, "./oils/core/static/dist"),
        filename: "[name].js",
    }
})

module.exports = [
    coreConfig,
    dashboardConfig,
    circulationConfig,
    accountConfig,
];
