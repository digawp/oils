import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import _ from 'underscore'
import thunk from 'redux-thunk'
import promise from 'redux-promise';
import createLogger from 'redux-logger';
import { createStore, applyMiddleware } from 'redux'
import { Provider, connect } from 'react-redux'

import { PatronInformation } from 'patron/components/patron-information'
import { ItemInformation } from 'holding/components/item-information'

const logger = createLogger();

// Fallback initialState, used only when server does not provide initialData
const initialState = {
    isFetching: {
        patron: false,
        item: false,
    },
    didInvalidate: {
        patron: false,
        item: false,
    },
    patron: {},
    item: {},
}

function loanApp(state=initialState, action){
    switch (action.type) {
        case CHANGE_ITEM:
            return {...state, item: action.item}
        case CHANGE_PATRON:
            return {...state, patron: action.patron}
        default:
            return state
    }
    return state;
}

/* Expecting server hydration : `initialData.loan` */
let store = createStore(loanApp, window.initialData.loan,
    applyMiddleware(thunk, promise, logger)
)

// Action
const CHANGE_ITEM = 'CHANGE_ITEM'
const CHANGE_PATRON = 'CHANGE_PATRON'

// Action Creator
function changeItem(item){
    return {
        type: CHANGE_ITEM,
        item
    }
}

function changePatron(patron){
    return {
        type: CHANGE_PATRON,
        patron
    }
}


/**
 * Presentation component
 * an input field for item
 */
class ItemInput extends Component {
    constructor(props){
        super(props);
        this.handleChange = this.handleChange.bind(this)
    }

    handleChange(){
        this.props.onItemChange(this.inputField.value);
    }
    render(){
        return (
          <div>
            <label htmlFor="id_item">Item Code</label>
            <input type="text" name="item" id="id_item"
                   ref={ ref => this.inputField = ref }
                   onChange={this.handleChange}/>
          </div>
        )
    }
}

/**
 * Presentation component
 * an input field for patron
 */
class PatronInput extends Component {
    constructor(props){
        super(props);
        this.handleChange = this.handleChange.bind(this)
    }

    handleChange(){
        this.props.onPatronChange(this.inputField.value);
    }

    render(){
        return (
          <div>
            <label htmlFor="id_patron">Patrons Code</label>
            <input type="text" name="patron" id="id_patron"
                   ref={ ref => this.inputField = ref }
                   onChange={this.handleChange}/>
          </div>
        )
    }
}
PatronInput.propTypes = {};
PatronInput.defaultProps = {};

async function callApi(request){
    try {
        let apiResponse = await fetch(request);
        let apiData = await apiResponse.json();
        return apiData
    } catch (e) {
        console.log(e);
    }
}

const mapDispatchToItemInputProps = (dispatch) => {
    let delayChangeItem = _.debounce(async (item)=> {
        let itemApiData = {}
        if (item !== '') {
            let request = new Request(`/api/holdings/items/${item}/`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
            });
            itemApiData = await callApi(request);
        }
        dispatch(changeItem(itemApiData))
    }, 1000);

    return {
        onItemChange: function(item) {
            delayChangeItem(item);
        },
    }
};
const mapDispatchToPatronInputProps = (dispatch) => {
    let delayChangePatron = _.debounce(async (patron)=> {
        let patronApiData = {}
        if (patron !== '') {
            let request = new Request(`/api/memberships/patrons/${patron}/`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
            });
            patronApiData = await callApi(request);
        }
        dispatch(changePatron(patronApiData))
    }, 1000);

    return {
        onPatronChange: function(patron){
            delayChangePatron(patron);
        },
    }
};


PatronInput = connect(null, mapDispatchToPatronInputProps)(PatronInput)
ItemInput = connect(null, mapDispatchToItemInputProps)(ItemInput)


const mapStateToPatronInfoProps = (state) => {
    return {
        patron: state.patron,
    }
}
const mapStateToItemInfoProps = (state) => {
    return {
        item: state.item,
    }
}

const LoanPatronInformation = connect(mapStateToPatronInfoProps)(PatronInformation)
const LoanItemInformation = connect(mapStateToItemInfoProps)(ItemInformation)


/**
 * Presentation component
 * a button to confirm the loan
 */

class LoanButton extends Component {
    render(){
        return (
            <button>Confirm Loan</button>
        )
    }
}


/**
 * Presentation Component
 * root component that render everything
 */
class LoanApp extends Component {
    constructor(props){
        super(props);
        this.handlePatronChange = this.handlePatronChange.bind(this);
        this.handleItemChange = this.handleItemChange.bind(this);
    }

    handlePatronChange(e){
        let patron_value = e.target.value;
        this.setState({patron: patron_value});
    }

    handleItemChange(e){
        let item_value = e.target.value;
        this.setState({item: item_value});
    }

    render(){
        return (
            <div className="row">
              <div className="col-xs-12 col-sm-6">
                <PatronInput />
                <LoanPatronInformation />
              </div>
              <div className="col-xs-12 col-sm-6">
                <ItemInput />
                <LoanItemInformation />
              </div>

              <LoanButton />
            </div>
        )
    }
}

ReactDOM.render(
    <Provider store={store}>
      <LoanApp />
    </Provider>,
    document.getElementById('loan-form')
)
