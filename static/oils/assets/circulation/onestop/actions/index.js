import * as ActionTypes from '../constants/ActionTypes'
import { CALL_API } from '../middleware/api'



export function lookupPatron(patron_id) {
  return (dispatch, getState)=>{
    let patron = patron_id
    if (patron === undefined) {
      patron = getState().patron.profile.id;
    }

    return dispatch({
      [CALL_API]: {
        request: `/api/patrons/${patron}/`,
        types: {
          request: ActionTypes.PATRON_REQUEST,
          success: ActionTypes.PATRON_SUCCESS,
          failure: ActionTypes.PATRON_FAILURE
        },
      },
    });
  }
};


export function selectLoanAction(loan, action) {
  return {
    type: '',
  }
};

export function checkoutResource(resource) {

  return async function(dispatch, getState) {
    let patron = getState().patron.profile.id;

    let request = new Request(`/api/loans/`, {
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
      action = await dispatch(lookupPatron());
    }
    return action;
  }
};

export function returnResource(loan) {
  const request = new Request(`/api/loans-returns/`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      loan
    })
  });

  return async function(dispatch) {
    let action = await dispatch({
      [CALL_API]: {
        request,
        types: {
          request: ActionTypes.RETURN_REQUEST,
          success: ActionTypes.RETURN_SUCCESS,
          failure: ActionTypes.RETURN_FAILURE
        }
      }
    });
    action = await dispatch(lookupPatron());
    return action;
  };
};

export function renewResource(loan) {
  const request = new Request(`/api/loans-renewals/`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      loan
    })
  });

  return async function(dispatch) {
    let action = await dispatch({
      [CALL_API]: {
        request,
        types: {
          request: ActionTypes.RENEWAL_REQUEST,
          success: ActionTypes.RENEWAL_SUCCESS,
          failure: ActionTypes.RENEWAL_FAILURE
        }
      }
    });
    action = await dispatch(lookupPatron());
    return action;
  };
};

export function selectLoanAction(loan, value) {
  return (dispatch) => {
    switch (value) {
      case 'return':
        return dispatch(returnResource(loan));
      case 'renew':
        return dispatch(renewResource(loan));
      default:
        return null;
    }
  }
}
