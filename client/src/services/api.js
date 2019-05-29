// eslint-disable-next-line
import axios, * as others from 'axios';

function arduinoAPI() {
    let baseURL = 'http://192.168.5.18/arduino/digital'
    if (localStorage.getItem('settings')) baseURL = JSON.parse(localStorage.getItem('settings')).arduinoUrl;
    return axios.create({
        baseURL: baseURL,
        responseType: 'text'
    })
}

export const arduino = arduinoAPI

function cloudAPI() {
    let baseURL = 'http://localhost:5000'
    if (localStorage.getItem('settings')) baseURL = JSON.parse(localStorage.getItem('settings')).cloudUrl;
    return axios.create({
        baseURL: baseURL
    })
}

export const cloud = cloudAPI
