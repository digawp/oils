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
const FAIL_PATRON_LOOKUP = 'FAIL_PATRON_LOOKUP';
const FAIL_CHECKOUT = 'FAIL_CHECKOUT';
const SUCCESS_CHECKOUT = 'SUCCESS_CHECKOUT';
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
        .then(response =>{
            return response.json().then(json=>({json, response}));
        })
        .then(({json, response}) => {
          if (!response.ok){
            dispatch(OneStopActions.failPatronLookup(json));
          } else {
            dispatch(OneStopActions.receivePatron(patron, json))
          }
        });
    };
  },

  failPatronLookup(json) {
    return {
      type: FAIL_PATRON_LOOKUP,
      json,
    };
  },

  selectLoanAction(loan, action) {
    return {
      type: '',
    }
  },

  checkoutResource(patron, resource) {
    return (dispatch) => {
      dispatch(OneStopActions.requestCheckout(patron, resource));
      fetch(`/api/loans/`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patron,
          resource,
        })})
      .then(response=>response.json().then(json=>({json, response})))
      .then(({json, response}) => {
        if (!response.ok){
          dispatch(OneStopActions.failCheckout(json));
        } else {
          dispatch(OneStopActions.successCheckout(json));
          dispatch(OneStopActions.lookupPatron(patron));
        }
      });
    };
  },

  requestCheckout(patron, resource) {
    return { type: CHECKOUT_RESOURCE, patron, resource };
  },

  failCheckout(json) {
    return { type: FAIL_CHECKOUT, json };
  },

  successCheckout(json) {
    return { type: SUCCESS_CHECKOUT, json };
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
        profile: patronProfileReducer(state.profile, action),
        circulation: circulationReducer(state.circulation, action),
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
    if (e.key === 'Enter' && patron !== '') {
      this.props.onLookup(patron);
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
        {
          patronProfile.id ? (
            <PatronDetail
              patronProfile={patronProfile} />
          ) : null
        }
      </div>
    );
  }
}

class LoanActions extends Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      value: ''
    };
  }

  handleChange(e) {
    this.setState({value: e.target.value });
    this.props.onSelect(this.props.loan, this.state.value);
    this.setState({value: ''});
  }

  render() {
    return (
      <select onChange={this.handleChange.bind(this)} value={this.state.value}>
        <option value='' disabled>--Actions--</option>
        <option value='renew'>Renew</option>
        <option value='return'>Return</option>
        <option value='lost'>Lost</option>
      </select>
    );
  }
}

class LoanRow extends Component {
  render(){
    const { num, loan, actions } = this.props;
    return (
      <tr>
        <td><input type='checkbox' /></td>
        <td>{ num }</td>
        <td>{loan.resource.code}</td>
        <td>{loan.resource.title}</td>
        <td>{loan.loan_at}</td>
        <td><LoanActions loan={loan.id} onSelect={actions.selectLoanAction}/></td>
      </tr>
    );
  }
}

class LoanTable extends Component {
  render(){
    const { loans, actions } = this.props;

    return (
      <table>
        <thead>
          <tr>
            <th><input type='checkbox' /></th>
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
                <LoanRow key={i} loan={obj} num={i+1} actions={actions}/>
              );
            })
          }
        </tbody>
      </table>
    );
  }
}


class CheckoutForm extends Component {

  constructor(props, context) {
    super(props, context);
    this.state = {
      resource: '',
    };
  }

  handleSubmit(e){
    e.preventDefault();
    this.props.onCheckout(this.props.patron, this.state.resource);
    this.setState({ resource : '' });
  }

  handleChange(e) {
    this.setState({
      resource: e.target.value,
    });
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit.bind(this)}>
          <label htmlFor="checkout-input">Resource Code:</label>
          <input
            type="text"
            id="checkout-input"
            value={this.state.resource}
            onChange={this.handleChange.bind(this)} />
          <button>Checkout</button>
        </form>
      </div>
    );
  }
}

class CirculationPanel extends Component {
  render(){
    const { patron, circulation, actions } = this.props;
    return (
      <div>
        <CheckoutForm patron={patron} onCheckout={actions.checkoutResource} />
        <LoanTable loans={circulation.loans} actions={actions}></LoanTable>
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
        {
          patron.profile.id ? (
          <CirculationPanel
            patron={patron.profile.id}
            circulation={patron.circulation}
            actions={actions} />
            ) : null
        }
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
