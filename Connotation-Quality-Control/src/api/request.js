import axios from "axios";

const request = axios.create({
    baseURL: 'http://localhost:43210',
    timeout: 10000000
})

request.interceptors.request.use(config => {
    config.headers['Content-Type'] = 'application/json;charset=utf-8'; // 此处应返回 config
    return config; // 返回 config 对象，以允许请求继续进行
}, error => {
    console.log(error);
    return Promise.reject(error);
});

request.interceptors.response.use(response => {
    let res = response.data;
    return res; // 返回响应数据
}, error => {
    console.log(error);
    return Promise.reject(error);
});

export default request;
