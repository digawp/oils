import {
  bindActionCreators,
  combineReducers,
} from 'redux'

import patronReducer from './onestop'

const rootReducer = combineReducers({
  patron: patronReducer,
});

export default rootReducer;
