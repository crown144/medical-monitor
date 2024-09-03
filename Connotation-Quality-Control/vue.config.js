const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  //-----------------------Axios跨域请求-----------------------------------------
  devServer:{
    port:8080,//vue网页访问的端口
    host:"127.0.0.1",//vue网页访问的地址
    https:false,
    open:false,
    proxy: {
        '/api': {  //为用于替换的的标识字符串
            target: 'http://127.0.0.1/:5000',//Axios跨域请求的IP
            changeOrigin: true, 
            ws: true,
            pathRewrite: {
                '^/api': '' //不改变
            }
        },
        
      
    }
  }
  //----------------------------------------------------------------------------

})