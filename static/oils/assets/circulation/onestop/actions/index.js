import * as ActionTypes from '../constants/ActionTypes'
import { CALL_API } from '../middleware/api'



function requestPatron(patron) {
  return { type: ActionTypes.REQUEST_PATRON, patron };
}

function receivePatron(patron, json) {
  return { type: ActionTypes.RECEIVE_PATRON, patron: json};
}

function failPatronLookup(json) {
  return {
    type: ActionTypes.FAIL_PATRON_LOOKUP,
    json,
  };
}


export function lookupPatron(patron) {
  return {
    [CALL_API]: {
      request: `/api/patrons/${patron}/`,
      types: {
        request: ActionTypes.PATRON_REQUEST,
        success: ActionTypes.PATRON_SUCCESS,
        failure: ActionTypes.PATRON_FAILURE
      },
    },
  }
};


export function selectLoanAction(loan, action) {
  return {
    type: '',
  }
};

function requestCheckout(patron, resource) {
  return { type: ActionTypes.CHECKOUT_RESOURCE, patron, resource };
};

function failCheckout(json) {
  return { type: ActionTypes.FAIL_CHECKOUT, json };
}

function successCheckout(json) {
  return { type: ActionTypes.SUCCESS_CHECKOUT, json };
}

export function checkoutResource(patron, resource) {
  const request = new Request(`/api/loans/`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      patron,
      resource,
    })
  });

  return async function(dispatch) {
    let action = await dispatch({
      [CALL_API]: {
        request,
        types: {
          request: ActionTypes.CHECKOUT_REQUEST,
          success: ActionTypes.CHECKOUT_SUCCESS,
          failure: ActionTypes.CHECKOUT_FAILURE,
        }
      }
    });
    if (action.type === ActionTypes.CHECKOUT_SUCCESS) {
      action = await dispatch(lookupPatron(patron));
    }
    return action;
  }
};

export function returnResource(identifier) {
  return { type: ActionTypes.RETURN_RESOURCE, identifier };
};

export function renewResource(identifier) {
  return { type: ActionTypes.RENEW_RESOURCE, identifier };
};
