import { CSRF_TOKEN } from "./csrf_token";
import axios from 'axios'

async function getJSON(response) {
    if (response.status === 204) return '';
    return response.json()
}

function apiService(endpoint, method, data) {
    const config = {
        method: method || "GET",
        body: data !== undefined ? JSON.stringify(data) : null,
        Headers: {
            'content-type': 'application/json',
            'X_CSRFTOKEN': CSRF_TOKEN
        }
    };
    return fetch(endpoint, config).then(getJSON).catch(error => console.log(error)) 
}

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";
function postAxios(endpoint, data) {
    return axios.post(endpoint, data, {
        Headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': CSRF_TOKEN
            }
        })

}

function patchAxios(endpoint, data) {
    return axios.patch(endpoint, data, {
        Headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': CSRF_TOKEN
        }
    })
}



export {apiService, postAxios, patchAxios};