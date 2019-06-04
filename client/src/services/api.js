// eslint-disable-next-line
import axios, * as others from 'axios';

function arduinoAPI() {
    let baseURL = 'http://192.168.5.18/arduino/digital'
    if (localStorage.getItem('settings')) baseURL = JSON.parse(localStorage.getItem('settings')).arduinoUrl;
    return axios.create({
        baseURL: `${baseURL}/arduino/digital`,
        responseType: 'text'
    })
}

export const arduino = arduinoAPI

let id = 1
function cloudAPI() {
    let baseURL = 'http://localhost:5000'
    id = 1
    if (localStorage.getItem('settings')) {
        baseURL = JSON.parse(localStorage.getItem('settings')).cloudUrl
        id = JSON.parse(localStorage.getItem('settings')).arduinoID
    }
    return axios.create({
        baseURL: baseURL
    })
}

export const cloud = cloudAPI
export const arduinoID = id
