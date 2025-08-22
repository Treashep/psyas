const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,

  // 开发环境跨域配置（解决前端调用 Flask API 跨域问题）
  devServer: {
    proxy: {
      // 所有以 '/api' 开头的请求都会被代理到 Flask 后端
      '/api': {
        target: 'http://localhost:5000',  // Flask 运行地址（默认端口 5000）
        changeOrigin: true,               // 开启跨域
        pathRewrite: { '^/api': '' }      // 去掉请求路径中的 '/api' 前缀
      }
    }
  },

  // 生产环境打包配置（将 Vue 打包到 Flask 静态目录）
  outputDir: '../psyas/static/dist',  // 打包后的文件输出到 Flask 的 static/dist 目录
  assetsDir: 'assets',                // 静态资源（css、js、图片等）存放目录
  indexPath: 'index.html',            // 入口 HTML 文件名称（默认即可）

  // 关键配置：设置相对路径，确保资源加载正确
  publicPath: './'
})