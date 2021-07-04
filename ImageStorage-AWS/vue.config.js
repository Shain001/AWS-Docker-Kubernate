// vue.config.js
module.exports = {
    devServer: {
        overlay: {
            warnings: false, 
            errors: false
        }
    },
    lintOnSave: false, 
    devServer: {
        proxy: {
            // set CORS
            '/test': {
                target: 'https://daf10kstc5.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true
            }
        },
        open: true
    }
}