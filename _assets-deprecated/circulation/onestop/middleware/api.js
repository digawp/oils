function callApi(request) {
  return fetch(request)
    .then(response=>response.json()
      .then(json=>({json, response})))
    .then(({json, response})=>{
      if (!response.ok) {
        return Promise.reject(json);
      }

      return {
        ...json,
      };
    });

}

export const CALL_API = Symbol('Call API');


export default store => next => action => {

  const callAPI = action[CALL_API];
  if (typeof callAPI === 'undefined') {
    return next(action);
  }

  const { request, types } = callAPI;

  function actionWith(data) {
    const finalAction = {
      ...action,
      ...data
    };
    delete finalAction[CALL_API];
    return finalAction;
  }

  next(actionWith({
    type: types.request,
  }));

  return callApi(request).then(
    response=>next(actionWith({
      response,
      type: types.success,      
    })),
    error => next(actionWith({
      type: types.failure,      
      error,
    })));
};
