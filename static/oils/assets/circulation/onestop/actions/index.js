import * as types from '../constants/ActionTypes'


function requestPatron(patron) {
  return { type: types.REQUEST_PATRON, patron };
}

function receivePatron(patron, json) {
  return { type: types.RECEIVE_PATRON, patron: json};
}

function failPatronLookup(json) {
  return {
    type: types.FAIL_PATRON_LOOKUP,
    json,
  };
}

export function lookupPatron(patron) {
  return (dispatch) => {
    dispatch(requestPatron(patron));
    fetch(`/api/patrons/${patron}/`)
      .then(response =>{
          return response.json().then(json=>({json, response}));
      })
      .then(({json, response}) => {
        if (!response.ok){
          dispatch(failPatronLookup(json));
        } else {
          dispatch(receivePatron(patron, json))
        }
      });
  };
};


export function selectLoanAction(loan, action) {
  return {
    type: '',
  }
};

function requestCheckout(patron, resource) {
  return { type: types.CHECKOUT_RESOURCE, patron, resource };
};

function failCheckout(json) {
  return { type: types.FAIL_CHECKOUT, json };
}

function successCheckout(json) {
  return { type: types.SUCCESS_CHECKOUT, json };
}

export function checkoutResource(patron, resource) {
  return (dispatch) => {
    dispatch(requestCheckout(patron, resource));
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
        dispatch(failCheckout(json));
      } else {
        dispatch(successCheckout(json));
        dispatch(lookupPatron(patron));
      }
    });
  };
};

export function returnResource(identifier) {
  return { type: types.RETURN_RESOURCE, identifier };
};

export function renewResource(identifier) {
  return { type: types.RENEW_RESOURCE, identifier };
};
