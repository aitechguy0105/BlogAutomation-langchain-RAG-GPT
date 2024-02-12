import axios from "axios";

export const setAuthToken = (token:string):void => {
    if(token) {
        axios.defaults.headers.common["api-token"] = `${token}`;
    }
    else
        delete axios.defaults.headers.common["api-token"];
}