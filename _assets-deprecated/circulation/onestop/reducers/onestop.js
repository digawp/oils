import * as types from '../constants/ActionTypes'

const initialPatronProfile = {
  id: '',
  name: '',
};
const initialCirculation = {
  loans: [],
};
const initialPatron = {
  profile: undefined,
  circulation: undefined,
};

const patronProfileReducer = (state=initialPatronProfile, action) => {
  switch (action.type) {
    case types.RECEIVE_PATRON:
      return Object.assign({}, state, action.patron);
    default:
      return state;
  }
};

const circulationReducer = (state=initialCirculation, action) => {
  switch (action.type) {
    case types.RECEIVE_PATRON:
      return Object.assign({}, state, {
        loans: action.patron.loans
      });
    default:
      return state;
  }
};

export default function patronReducer(state=initialPatron, action) {
  switch (action.type) {
    case types.REQUEST_PATRON:
      return Object.assign({}, state, {
        isFetching: true,
      });
    case types.RECEIVE_PATRON:
      return Object.assign({}, state, {
        isFetching: false,
        profile: patronProfileReducer(state.profile, action),
        circulation: circulationReducer(state.circulation, action),
      });
    default:
      return Object.assign({}, state, {
        profile: patronProfileReducer(state.profile, action),
        circulation: circulationReducer(state.circulation, action),
      });
  }
};
