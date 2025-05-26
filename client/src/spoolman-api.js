import { sendRequest } from "./utilities";

var apiendpoint = import.meta.env.VITE_SPOOLMAN_API_ENDPOINT.trim();
apiendpoint += '/api/v1';

export async function getSpools(){
    var response = {success:false, spools:[], error:null};
    try{
        let data = await sendRequest(apiendpoint + '/spool?allow_archived=false');
        response.success = true;
        response.spools = data
    }
    catch(error){
        response.error = error;
    }
    return response;
}

export async function getFilaments(){
    var response = {success:false, filaments:[], error:null};
    try{
        let data = await sendRequest(apiendpoint + '/filament');
        response.success = true;
        response.filaments = data
    }
    catch(error){
        response.error = error;
    }
    return response;
}