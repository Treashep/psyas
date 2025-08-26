const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: [],
  // 跨域代理（对接 Flask）
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        pathRewrite: { '^/api': '' }
      }
    }
  },
  // 打包路径（对接 Flask 静态目录）
  outputDir: '../psyas/static/dist',
  assetsDir: 'assets',
  publicPath: './'
})