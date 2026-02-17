const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: ['vuetify'],

  devServer: {
    host: "0.0.0.0",
    port: 8080,
    client: {
      webSocketURL: {
        hostname: "localhost",
        port: 8080,
        protocol: "ws",
      },
    },
  },
})
