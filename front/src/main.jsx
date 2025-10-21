import './index.css'
import { RouterProvider } from 'react-router-dom'
import { Provider } from 'react-redux'
import React from 'react'
import ReactDOM from 'react-dom/client'
import router from './router/index.jsx'
import store from './store'
import { HelmetProvider } from 'react-helmet-async'

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
  <Provider store={store}>
    <HelmetProvider>
      <RouterProvider router={router} />
    </HelmetProvider>
  </Provider>
)