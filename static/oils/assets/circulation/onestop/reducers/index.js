import {
  bindActionCreators,
  combineReducers,
} from 'redux'
import * as ActionTypes from '../constants/ActionTypes'

//import patronReducer from './onestop'

function entityReducer(state={patron:{}}, action) {
  if (action.response) {
    return {
      ...state,
      ...action.response,
    };
  }
  return state;
}

const INITIAL_PATRON = {
  profile: {},
}

function patronReducer(state=INITIAL_PATRON, action){
  switch (action.type) {
    case ActionTypes.PATRON_SUCCESS:
      return {
        profile: {
          ...state,
          ...action.response
        },
      }
    default:
      return state;
  }
}

const rootReducer = combineReducers({
  patron: patronReducer,
});

export default rootReducer;
