// eslint-disable-next-line
import axios, * as others from 'axios';

function arduinoAPI() {
    let baseURL = 'http://192.168.5.18/arduino/digital'
    if (localStorage.getItem('settings')) baseURL = JSON.parse(localStorage.getItem('settings')).arduinoUrl;
    return axios.create({
        baseURL: baseURL,
        headers: {
            'Content-Type': 'text/html'
        },
        responseType: 'text'
    })
}

export const arduino = arduinoAPI

function clodudAPI() {
    let baseURL = 'http://192.168.5.18'
    if (localStorage.getItem('settings')) baseURL = JSON.parse(localStorage.getItem('settings')).arduinoUrl;
    return axios.create({
        baseURL: baseURL
    })
}

export const cloud = clodudAPI
