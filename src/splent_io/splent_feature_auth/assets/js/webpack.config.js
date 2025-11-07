const path = require('path');
const fs = require('fs');

module.exports = {
  entry: path.resolve(__dirname, './scripts.js'),
  output: {
    filename: 'auth.bundle.js',
    path: path.resolve(__dirname, '../dist')
  },
  resolve: {
    fallback: {
      fs: false,
    },
  },
  mode: 'development',
};
