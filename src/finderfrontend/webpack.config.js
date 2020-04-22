const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')
const HtmlWebpackPlugin = require('html-webpack-plugin')

const DJANGO_APP_NAME = 'finderfrontend'
const production = false

module.exports = {
  context: __dirname,
  entry: "./src/index",
  target: 'web',
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.(ts|tsx)$/,
        exclude: '/node_modules/',
        use: {
          loader: 'ts-loader'
        },
      }
    ]
  },
  plugins: [
    new BundleTracker({ 
      filename: 'webpack-stats.json',
      indent: '  '
    })
  ],
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx']
  },
  output: {
    path: path.resolve(`./src/${DJANGO_APP_NAME}`, 'static', 'build'),
    filename: `[name]${production ? '-[hash]' : ''}.js`,
  }
}