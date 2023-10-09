import axios from "axios"

export const getRequest = (url, data= {}, json = true) =>{
    return new Promise((resolve, reject) =>{
        const token = localStorage.getItem("adminInfor") ? JSON.parse(localStorage.getItem("adminInfor")).token : null
        axios.get(url, {
            params: data,
            headers: {
                "Authorization": `Bearer ${token}`,
                'Accept':'application/json',
                'Content-Type':'application/json',
            }
        })
        .then(function (response) {
            resolve(response)
        })
        .catch(error=>{
            if (error.response && error.response.status == 401) {
                logout();

                return;
            }
            reject(error.response)
        });
    });
}


export const logout = () =>{
    localStorage.removeItem("adminInfo");
    window.location = `/`

    return;
}