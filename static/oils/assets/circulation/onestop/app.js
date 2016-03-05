import React, { Component, PropTypes } from 'react'
import ReactDOM from 'react-dom'
import { connect, Provider } from 'react-redux'
import { bindActionCreators, combineReducers, createStore } from 'redux'

// Constant ActionTypes
const LOOKUP_PATRON = 'LOOKUP_PATRON';
const CHECKOUT_RESOURCE = 'CHECKOUT_RESOURCE';
const RETURN_RESOURCE = 'RETURN_RESOURCE';
const RENEW_RESOURCE = 'RENEW_RESOURCE';

// Actions

let OneStopActions = {
  lookupPatron(patron) {
    return { type: LOOKUP_PATRON, patron };
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
}


// Reducers
const initialPatronProfile = {
  id: '',
  name: '',
};
const initialPatron = {
  profile: initialPatronProfile,
  circulation: undefined,
};

const patronProfileReducer = (state=initialPatronProfile, action) => {
  switch (action.type) {
    case LOOKUP_PATRON:
      return Object.assign({}, state, {
        id: action.patron,
        name: action.patron + 'World' 
      });
    default:
      return state;
  }
};

const circulationReducer = (state, action) => { state };

const patronReducer = (state=initialPatron, action) => {
  switch (action.type) {
    case LOOKUP_PATRON:
      return {
        profile: patronProfileReducer(state.profile, action),
        circulation: circulationReducer(undefined, action),
      };
    default:
      return state;
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

class LoanTable extends Component {
  render(){
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
          <tr>
            <td>1</td>
            <td>9871234567890</td>
            <td>Hello World</td>
            <td>1 April 2016</td>
            <td>-</td>
          </tr>
          <tr>
            <td>2</td>
            <td>9871234567890</td>
            <td>Big World</td>
            <td>1 April 2016</td>
            <td>-</td>
          </tr>
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
    return (
      <div>
        <CheckoutForm></CheckoutForm>
        <LoanTable></LoanTable>
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

let store = createStore(rootReducer);

ReactDOM.render(
  <Provider store={store}>
    <OneStopApp />
  </Provider>,
  document.getElementById('circulation-os')    
);
