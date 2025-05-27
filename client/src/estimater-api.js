import { sendRequest } from "./utilities";

var estimaterapiendpoint = import.meta.env.VITE_API_ENDPOINT.trim();

export async function getCustomers(){
    var response = {success:false,customers:[], error: null};
    try{
        let data = await sendRequest(estimaterapiendpoint + '/api/customers', 'GET');
        response.success = data.success;
        response.customers = data.customers;
    }
    catch(error){
        response.error = error;
    }
    return response;
}

export async function getCustomer(id){
    var response = {success:false, customer:{}, error: null};
    try{
        let data = await sendRequest(estimaterapiendpoint + '/api/customers/' + id, 'GET')
        response.success = data.success;
        response.customer = data.customer;
    }
    catch(error){
        response.error = error;
    }
    return response;
}

export async function upsertCustomer(id, customer){
    var response = {success:false, error: null};
    let endpoint = '/api/customers'
    let method = 'POST'
    if (id != 0){
        endpoint += '/' + id;
        method = 'PATCH';
    }
    try{
        let data = await sendRequest(estimaterapiendpoint + endpoint, method, customer);
        response.success = data.success;
        response.error = data.message;
    }
    catch(error){
        response.error = error;
    }
    return response;
}

export async function deleteCustomer(){
    var response = {success:false, error: null};
    try{
        let data = await sendRequest(estimaterapiendpoint + '/api/customers/'+ id, 'DELETE');
        response.success = data.success;
        response.error = data.error;
    }catch(error){
        response.error = error;
    }
    return response;
}

export async function getEstimates(){
    var response = {success:false,estimates:[],error:null};
    try{
        let data = await sendRequest(estimaterapiendpoint + '/api/estimates', 'GET');
        response.success = data.success;
        response.estimates = data.estimates;
    }
    catch(error){
        response.error = error;
    }
    return response;
}

export async function getEstimate(id) {
    var response = {success:false,estimate:{},error:null};
    try{
        let data = await sendRequest(estimaterapiendpoint + '/api/estimates/' + id, 'GET');
        response.success = data.success;
        response.estimate = data.estimate;
        if (!response.estimate.models){
            response.estimate.models = []
        }
    }
    catch(error){
        response.error = error;
    }
    return response;
}

export async function upsertEstimate(id, estimate, filamentsused) {
    var response = {success:false,error:null};
    let endpoint = '/api/estimates';
    let method = 'POST'
    if (id != 0){
        endpoint += '/' + id;
        method = 'PATCH';
    }
    try{
        let data = await sendRequest(estimaterapiendpoint + endpoint, method, {estimate: estimate, filamentsused: filamentsused});
        response.success = data.success;
        response.error = data.error;
    }catch(error){
        response.error = error;
    }
    return response;
}

export async function deleteEstimate(id){
    var response = {success:false,error:null};
    try{
        let data = await sendRequest(estimaterapiendpoint + '/api/estimates/' + id,'DELETE');
        response.success = data.success;
        response.error = response.error;
    }
    catch(error){
        response.error = error;
    }
    return response;
}

export async function getPrints(){
    var response = {success:false,prints:[],error:null};
    try{
        let data = await sendRequest(estimaterapiendpoint + '/api/prints', 'GET');
        response.success = data.success;
        response.prints = data.prints;
    }catch(error){
        response.error = error;
    }
    return response;
}

export async function getPrint(id){
    var response = {success:false,print:{},error:null};
    try{
        let data = await sendRequest(estimaterapiendpoint + '/api/prints/' + id, 'GET');
        response.success = data.success;
        response.print = data.print;
    }catch(error){
        response.error = error;
    }
    return response;
}

export async function deletePrint(id){
    var response = {success:false,error:null};
    try{
        let data = await sendRequest(estimaterapiendpoint + '/api/prints/' + id, 'DELETE');
        response.success = data.success;
        response.error = data.message;
    }catch(error){
        response.error = error;
    }
    return response;
}

export async function upsertPrint(id, print){
    var response = {success:false,error:null};
    let endpoint = '/api/prints';
    let method = 'POST'
    if (id != 0){
        endpoint += '/' + id;
        method = 'PATCH';
    }
    try{
        let data = await sendRequest(estimaterapiendpoint + endpoint, 'POST', print)
        response.success = data.success;
        response.error = data.message;
    }catch(error){
        response.error = error;
    }
    return response;
}

export async function getSettings(){
    var response = {success:false,settings:{}};
    try{
        let data = await sendRequest(estimaterapiendpoint + '/api/settings', 'GET');
        response.success = data.success;
        response.settings = data.settings;
    }catch(error){
        response.error = error;
    }
    return response;
}

export async function saveSettings(settings){
    var response = {success:false,error:null};
    try{
        let data = await sendRequest(estimaterapiendpoint + '/api/settings', 'PATCH', settings);
        response.success = data.success;
        response.error = data.message;
    }catch(error){
        response.error = error;
    }
}