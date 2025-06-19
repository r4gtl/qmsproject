import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

// Theme Bootswatch (es: Flatly)
import 'bootswatch/dist/flatly/bootstrap.min.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
