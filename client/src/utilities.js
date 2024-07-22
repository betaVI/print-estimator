var apiendpoint = import.meta.env.VITE_API_ENDPOINT.trim();

export const sendRequest = async function(path, method, data = null){
    let requestInit = { method: method };
    if (data){
        requestInit.headers = { 'content-type': 'application/json' }
        requestInit.body = JSON.stringify(data);
    }

    let response = await fetch(apiendpoint + path, requestInit)
    return data = await response.json();
}