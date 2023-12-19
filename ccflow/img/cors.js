function axiosWithInterceptor (accountId){

    const axiosInstance = axios.create({
        timeout: 10000,
    });

    // Add a request interceptor
    axiosInstance.interceptors.request.use(function (config) {
        // setLoading()

        // Set the "Accept-Language" header in the request
        config.headers['ACCOUNT_ID'] = accountId;
        return config;
    }, function (error) {
        console.error(error)
        return Promise.reject(error);
    });

    // Add a response interceptor
    axiosInstance.interceptors.response.use(function (response) {
        return response.data;
    }, function (error) {
        console.error(error)
        return Promise.reject(error);
    });
    return axiosInstance;
}

window.sendRequest = axiosWithInterceptor;