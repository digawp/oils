import EventEmitter from 'events'
import OneStopAppDispatcher from '../dispatcher/OneStopAppDispatcher'
import OneStopConstants from '../constants/OneStopConstants'

var ActionTypes = OneStopConstants.ActionTypes;

var _patron = {};

const CHANGE_EVENT = 'change';


class PatronStore extends EventEmitter {
  emitChange(){
    this.emit(CHANGE_EVENT);
  }

  addChangeListener(callback){
    this.on(CHANGE_EVENT, callback);
  }

  removeChangeListener(callback){
    this.removeListener(CHANGE_EVENT, callback);
  }

  get(){
    return _patron;
  }

}

const patronStore = new PatronStore();

function fetchPatronDetail(patron_id){
  _patron.id = patron_id;
  fetch(`/api/patrons/${patron_id}/`, {
    accept: 'application/json', 
  }).then((response)=>{
    return response.json();
  }).then((json)=>{
    _patron.name = json.username;
    _patron.address = json.address;
    _patron.loan_limit = json.loan_limit;
    patronStore.emitChange();
  });
}

function fetchLoanList(patron_id){

}

patronStore.dispatchToken = OneStopAppDispatcher.register(action => {
  switch (action.type){
    case ActionTypes.LOOKUP_PATRON:
      fetchPatronDetail(action.patron_id);
      fetchLoanList(action.patron_id);
      patronStore.emitChange();
      break;
    default:
  }
});

export default patronStore;
