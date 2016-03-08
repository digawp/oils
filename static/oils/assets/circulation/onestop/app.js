import React, { Component, PropTypes } from 'react'
import ReactDOM from 'react-dom'
import { connect, Provider } from 'react-redux'
import createLogger from 'redux-logger'
import {
  bindActionCreators,
  combineReducers,
  createStore,
  applyMiddleware,
} from 'redux'
import thunkMiddleware from 'redux-thunk'

const loggerMiddleware = createLogger();

// Constant ActionTypes
const LOOKUP_PATRON = 'LOOKUP_PATRON';
const CHECKOUT_RESOURCE = 'CHECKOUT_RESOURCE';
const RETURN_RESOURCE = 'RETURN_RESOURCE';
const RENEW_RESOURCE = 'RENEW_RESOURCE';
const REQUEST_PATRON = 'REQUEST_PATRON';
const RECEIVE_PATRON = 'RECEIVE_PATRON';

// Actions

let OneStopActions = {
  lookupPatron(patron) {
    return (dispatch) => {
      dispatch(OneStopActions.requestPatron(patron));
      fetch(`/api/patrons/${patron}/`)
        .then(response =>
            response.json()
            .then(json=>({json, response}))
        )
        .then(({json, response}) => {
          if (!response.ok){
            Promise.reject(json);
          }
          dispatch(OneStopActions.receivePatron(patron, json))
        });
    };
  },

  checkoutResource(identifier) {
    return { type: CHECKOUT_RESOURCE, identifier };
  },

  returnResource(identifier) {
    return { type: RETURN_RESOURCE, identifier };
  },

  renewResource(identifier) {
    return { type: RENEW_RESOURCE, identifier };
  },

  requestPatron(patron) {
    return { type: REQUEST_PATRON, patron };
  },

  receivePatron(patron, json) {
    return { type: RECEIVE_PATRON, patron: json};
  },
}


// Reducers
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
    case RECEIVE_PATRON:
      return Object.assign({}, state, action.patron);
    default:
      return state;
  }
};

const circulationReducer = (state=initialCirculation, action) => {
  switch (action.type) {
    case RECEIVE_PATRON:
      return Object.assign({}, state, {
        loans: action.patron.loans
      });
    default:
      return state;
  }
};

const patronReducer = (state=initialPatron, action) => {
  switch (action.type) {
    case REQUEST_PATRON:
      return Object.assign({}, state, {
        isFetching: true,
      });
    case RECEIVE_PATRON:
      return Object.assign({}, state, {
        isFetching: false,
        profile: patronProfileReducer(state.profile, action),
        circulation: circulationReducer(state.circulation, action),
      });
    default:
      return Object.assign({}, state, {
        profile: patronProfileReducer(undefined, action),
        circulation: circulationReducer(undefined, action),
      });
  }
};


const rootReducer = combineReducers({
  patron: patronReducer,
});


// Components
class PatronLookupForm extends Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      patron: this.props.patron || '',
    };
  }

  handleChange(e) {
    this.setState({ patron: e.target.value });
  }

  handleSubmit(e) {
    const patron = e.target.value.trim();
    if (e.key === 'Enter') {
      this.props.onLookup(patron);
      this.setState({ patron: '' });
    }
  }

  render() {
    return (
      <div>
        <label htmlFor="patron-lookup">Patron</label>
        <input
          type="text"
          id="patron-lookup"
          value={this.state.patron}
          onChange={this.handleChange.bind(this)}
          onKeyDown={this.handleSubmit.bind(this)} />
      </div>
    );
  }
}

PatronLookupForm.propTypes = {
  onLookup: PropTypes.func.isRequired,
  patron: PropTypes.string,
}

class PatronDetail extends Component {
  render() {
    const { patronProfile } = this.props;
    return (
      <div>
        ID: {patronProfile.id} <br />
        Name: {patronProfile.name} <br/>
        Email: {patronProfile.email} <br/>
        Loan Limit: {patronProfile.loan_limit} <br/>
      </div>
    );
  }
}

class PatronPanel extends Component {
  render(){
    const { patronProfile, onLookup } = this.props;
    return (
      <div>
        <PatronLookupForm
          patronId={patronProfile.id}
          onLookup={onLookup} />
        <PatronDetail
          patronProfile={patronProfile} />
      </div>
    );
  }
}

class LoanRow extends Component {
  render(){
    const { num, loan } = this.props;
    return (
      <tr>
        <td>{ num }</td>
        <td>{loan.resource.code}</td>
        <td>{loan.resource.title}</td>
        <td>{loan.loan_at}</td>
        <td>-</td>
      </tr>
    );
  }
}

class LoanTable extends Component {
  render(){
    const { loans } = this.props;

    return (
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Identifier</th>
            <th>Title</th>
            <th>Due Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {
            loans.map((obj, i) => {
              return (
                <LoanRow key={i} loan={obj} num={i+1} />
              );
            })
          }
        </tbody>
      </table>
    );
  }
}


class CheckoutForm extends Component {
  render() {
    return (
      <div>
        Checkout Form
      </div>
    );
  }
}

class CirculationPanel extends Component {
  render(){
    const { circulation, actions } = this.props;
    return (
      <div>
        <CheckoutForm></CheckoutForm>
        <LoanTable loans={circulation.loans}></LoanTable>
      </div>
    );
  }
}

// Containers App
class App extends Component {
  render(){
    const { patron, actions } = this.props;

    return (
      <div>
        <PatronPanel
          patronProfile={patron.profile}
          onLookup={actions.lookupPatron} /> 
        <CirculationPanel
          circulation={patron.circulation} actions={actions} />
      </div>
    );
  }
}

App.propTypes = {
  patron: PropTypes.object.isRequired,
  actions: PropTypes.object.isRequired,
}

function mapStateToProps(state) {
  return {
    patron: state.patron,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(OneStopActions, dispatch)
  }
}

var OneStopApp = connect(mapStateToProps, mapDispatchToProps)(App);

let store = createStore(
  rootReducer,
  applyMiddleware(
    thunkMiddleware,
    loggerMiddleware
  ));

ReactDOM.render(
  <Provider store={store}>
    <OneStopApp />
  </Provider>,
  document.getElementById('circulation-os')    
);
