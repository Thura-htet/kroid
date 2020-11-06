// it's working fine but this is still a complete mess
// have to come back after having understood async-await and promises

const getData = async (url) => {
    const responseData = {
        isLoaded: false,
        data: null,
        error: null
    };
    // probably need to make error to be an object with message field

    const response = await fetch(url);

    responseData.isLoaded = true;
    if (!response.ok)
    {
        // throw an error so that the caller can use .catch
        responseData.error = `An error has occured: ${response.status}`;
    }
    responseData.data = await response.json();

    return responseData;
}

const postData = async (url, data) => {
    const responseData = {
        isLoaded: false,
        data: null,
        error: null
    }

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    responseData.isLoaded = true;
    if (!response.ok) 
    {
        // throw an error so that the caller can use .catch
        responseData.error = `An error has occured: ${response.status}`;
    }
    responseData.data = await response.json()

    return responseData;
}

export { getData, postData };

// get response => postData(url, data).then(response => response)
// get error => postData(url, data).catch(error => error.message)

// const getData = (url) => {
//     const responseData = {
//         isLoaded: false,
//         result: null,
//         error: null
//     };
//     fetch(url)
//     .then(res => res.json())
//     .then(
//         result => {
//             responseData.isLoaded = true;
//             responseData.result = result;
//         },
//         error => {
//             responseData.isLoaded = true;
//             responseData.error = error;
//         }
//     )
//     return responseData;
// }

// const postData = (url, data) => {
//     fetch(url, {
//         method: 'post',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(data)
//     });
// }
