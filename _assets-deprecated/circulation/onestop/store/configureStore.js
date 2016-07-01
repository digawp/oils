import { createStore, applyMiddleware } from 'redux'
import createLogger from 'redux-logger'
import thunkMiddleware from 'redux-thunk'
import rootReducer from '../reducers'
import promiseMiddleware from 'redux-promise'
import api from '../middleware/api'

const loggerMiddleware = createLogger();

export default function configureStore(initialState) {
  
  const store = createStore(
    rootReducer,
    applyMiddleware(
      thunkMiddleware,
      promiseMiddleware,
      api,
      loggerMiddleware
    ));

  return store;
};
