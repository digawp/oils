async function callApi(request){
    response = await fetch(request)
    data = await response.json()
    return data
}

export const CALL_API = Symbol('CALL_API')

export default store => next => action {
    const callAPI = action[CALL_API]
    if (typeof callAPI === 'undefined'){
        let result = next(action)
    }
    return result
}
