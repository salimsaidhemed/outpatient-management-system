import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import './styles/app.css'

import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import App from './App.vue'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'admissionsTheme',
    themes: {
      admissionsTheme: {
        dark: false,
        colors: {
          background: '#f7f8fa',
          surface: '#ffffff',
          primary: '#19647e',
          secondary: '#4f6f52',
          accent: '#b65f30',
          error: '#b42318',
          info: '#2662d9',
          success: '#157f3b',
          warning: '#b7791f',
        },
      },
    },
  },
})

createApp(App).use(vuetify).mount('#app')
