import EventEmitter from 'events'
import OneStopAppDispatcher from '../dispatcher/OneStopAppDispatcher'
import OneStopConstants from '../constants/OneStopConstants'

var ActionTypes = OneStopConstants.ActionTypes;

var _loans = {};

const CHANGE_EVENT = 'change';

class LoanStore extends EventEmitter {
  emitChange(){
    this.emit(CHANGE_EVENT);
  }

  addChangeListener(callback){
    this.on(CHANGE_EVENT, callback);
  }

  removeChangeListener(callback){
    this.removeListener(CHANGE_EVENT, callback);
  }

  get(id){
    return _loans[id];
  }

  getAll(){
    return _loans;
  }

}

const loanStore = new LoanStore();

loanStore.dispatchToken = OneStopAppDispatcher.register(action => {
  switch (action.type){
    case ActionTypes.RENEW_ISSUE:
      console.log(action.issue_id);
      patronStore.emitChange();
      break;
    case ActionTypes.RETURN_ISSUE:
      break;
    case ActionTypes.NEW_ISSUE:
      console.log(action.resource_code);
      break;
    default:
  }
});

export default loanStore;
