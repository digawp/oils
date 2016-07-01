import 'babel-polyfill'
import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import App from './containers/App'
import configureStore from './store/configureStore'

import 'react-select/less/select.less'
import './app.less'

const store = configureStore(window.initial_data);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('catalog-os')    
);
