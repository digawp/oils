import {
  bindActionCreators,
  combineReducers,
} from 'redux'

const INITIAL_ROOT = {
  item: {
    bibliographic: {
      identifiers: undefined,
      title: undefined,
      holdings: undefined,
      classifications: undefined,
      subjects: undefined,
      authors: undefined,
      publishers: undefined,
    },
  },
}

const rootReducer = (state=INITIAL_ROOT, action) => {
  return state;
};

export default rootReducer;
