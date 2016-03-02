import OneStopAppDispatcher from '../dispatcher/OneStopAppDispatcher'
import OneStopConstants from '../constants/OneStopConstants'

var ActionTypes = OneStopConstants.ActionTypes;

module.exports = {
  lookupPatron(patron_id){
    OneStopAppDispatcher.dispatch({
      type: ActionTypes.LOOKUP_PATRON,
      patron_id: patron_id,
    });
  },
};
