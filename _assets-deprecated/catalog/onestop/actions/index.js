

export function lookupItem(value){
  return async function (dispatch, getState) {
    let request = new Request(`/api/catalog/books/`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    });

    let action = await dispatch({
      [CALL_API]: {
        request,
        types: {
          request: ActionTypes.ITEM_LOOKUP_REQUEST,
          success: ActionTypes.ITEM_LOOKUP_SUCCESS,
          failure: ActionTypes.ITEM_LOOKUP_FAILURE,
        }
      }
    });
    return {
      type: 'LOOKUP_ITEM',
      value,    
    }
  }
}
