import axios from 'axios';
import Vue from 'vue';
import 'materialize-css';

import dashPictures from './components/dash_pictures';


window.axios = axios.create({
    baseURL: '/dash_pictures/api/',
    timeout: 1000,
    withCredentials: true,
    headers: {
        'xsrfCookieName': 'csrftoken',
        'xsrfHeaderName': 'X-CSRFToken',
    }
});


window.Event = new Vue();


new Vue({
    el: '#app',
    components: {
        dashPictures
    }
});
