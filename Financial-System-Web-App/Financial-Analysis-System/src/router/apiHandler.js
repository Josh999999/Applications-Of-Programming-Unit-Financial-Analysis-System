export default class API_Handler {
    async getCookie(){
        let headers = new Headers();

        headers.append('Content-Type', 'application/json');
        headers.append('Accept', 'application/json');
        headers.append('Origin','http://localhost:5000/getcookie');

        let response = null;
        try {
            const fetchResponse = await fetch("http://localhost:5000/getcookie", {
            mode: 'cors',
            method: 'GET',
            headers: headers
            })
            .catch(error => console.log('Request failed : ' + error.message));
            
            response = await fetchResponse.json();
        } catch (error) {
            console.error(error);
        }

        return response;
    }

    async getJSON_Orders(start_date, end_date, user_id){
        // Format dates to %Y-%m-%d


        let headers = new Headers();
        let parameters = new URLSearchParams({
            start_date: start_date,
            end_date: end_date,
            user_id: user_id
        })

        headers.append('Authorization', 'L8hWquwn7hcSOGgYqu67KtDLxwqVTGlz') // Add API key to request for authorization

        let response = null;
        try {
            const fetchResponse = await fetch("http://localhost:5000/finas/orders?" + parameters.toString(), {
            mode: 'cors',
            method: 'GET',
            headers: headers
            })
            .catch(error => console.log('Request failed : ' + error.message));
            
            response = fetchResponse.json();
        } catch (error) {
            console.error(error);
        }

        return response;
    }

    async getJSON_OrdersGraph(start_date, end_date, user_id){
        let headers = new Headers();
        let parameters = new URLSearchParams({
            start_date: start_date,
            end_date: end_date,
            user_id: user_id
        })

        // Route returns Image and function returns blob object
        headers.append('Authorization', 'L8hWquwn7hcSOGgYqu67KtDLxwqVTGlz') // Add API key to request for authorization

        let response = null;
        try {
            const fetchResponse = await fetch("http://localhost:5000/finas/orders/graph?" + parameters.toString(), {
            mode: 'cors',
            method: 'GET',
            headers: headers
            })
            .catch(error => console.log('Request failed : ' + error.message));
            
            response = fetchResponse.blob();
        } catch (error) {
            console.error(error);
        }

        return response;
    }

    async getJSON_OrdersItems(start_date, end_date, user_id){
        let headers = new Headers();
        let parameters = new URLSearchParams({
            start_date: start_date,
            end_date: end_date,
            user_id: user_id
        })

        headers.append('Content-Type', 'application/json'); // Route returns JSON and function returns JS object
        headers.append('Accept', 'application/json');
        headers.append('Authorization', 'L8hWquwn7hcSOGgYqu67KtDLxwqVTGlz') // Add API key to request for authorization

        let response = null;
        try {
            const fetchResponse = await fetch("http://localhost:5000/finas/orders/items?" + parameters.toString(), {
            mode: 'cors',
            method: 'GET',
            headers: headers
            })
            .catch(error => console.log('Request failed : ' + error.message));
            
            response = fetchResponse.json();
        } catch (error) {
            console.error(error);
        }

        return response;
    }

    async getJSON_OrdersItemsGraph(start_date, end_date, user_id){
        let headers = new Headers();
        let parameters = new URLSearchParams({
            start_date: start_date,
            end_date: end_date,
            user_id: user_id
        })

        // Route returns Image and function returns blob object
        headers.append('Authorization', 'L8hWquwn7hcSOGgYqu67KtDLxwqVTGlz') // Add API key to request for authorization

        let response = null;
        try {
            const fetchResponse = await fetch("http://localhost:5000/finas/orders/items/graph?" + parameters.toString(), {
            mode: 'cors',
            method: 'GET',
            headers: headers
            })
            .catch(error => console.log('Request failed : ' + error.message));
            
            response = fetchResponse.blob();
        } catch (error) {
            console.error(error);
        }

        return response;
    }

    async getJSON_UserQueries(user_id){
        let headers = new Headers();
        let parameters = new URLSearchParams({
            user_id: user_id
        })

        headers.append('Authorization', 'L8hWquwn7hcSOGgYqu67KtDLxwqVTGlz') // Add API key to request for authorization

        let response = null;
        try {
            const fetchResponse = await fetch("http://localhost:5000/finas/user/queries?" + parameters.toString(), {
            mode: 'cors',
            method: 'GET',
            headers: headers
            })
            .catch(error => console.log('Request failed : ' + error.message));
            
            response = fetchResponse.json();
            console.log(response);
        } catch (error) {
            console.error(error);
        }

        return response;
    }

    async get_ExecuteUserQuery(url, start_date, end_date, user_id){
        // Used to send GET requests to any of the GET routes for the different query types

        let headers = new Headers();
        let parameters = new URLSearchParams({
            start_date: start_date,
            end_date: end_date,
            user_id: user_id
        })

        // Route and function returns response to request for receiver to deal with - Route will return Image or JSON response
        headers.append('Authorization', 'L8hWquwn7hcSOGgYqu67KtDLxwqVTGlz') // Add API key to request for authorization

        let response = null;
        try {
            const fetchResponse = await fetch("http://localhost:5000" + url + '?' + parameters.toString(), {
            mode: 'cors',
            method: 'GET',
            headers: headers
            })
            .catch(error => console.log('Request failed : ' + error.message));
            
            response = fetchResponse;
        } catch (error) {
            console.error(error);
        }

        return response;
    }
    
    async getJSON_QueriesLookupTable(){
        // Lookup which route the query type belongs too for the GET request
        let headers = new Headers();
        headers.append('Content-Type', 'application/json'); // Route returns JSON and function returns JS object
        headers.append('Accept', 'application/json');
        headers.append('Authorization', 'L8hWquwn7hcSOGgYqu67KtDLxwqVTGlz') // Add API key to request for authorization

        let response = null;
        try {
            const fetchResponse = await fetch("http://localhost:5000/finas/queries/lookup", {
            mode: 'cors',
            method: 'GET',
            headers: headers
            })
            .catch(error => console.log('Request failed : ' + error.message));
            
            response = await fetchResponse.json();
        } catch (error) {
            console.error(error);
        }

        return response;
    }

    async delete_ExecuteUserQuery(url, id, user_id){
        // Used to send DELETE requests to any of the DELETE routes for the different query types
        let headers = new Headers();
        let parameters = new URLSearchParams({
            id: id,
            user_id: user_id
        })

        
        // Route and functio returns message on the state of the request - complete or failed
        headers.append('Authorization', 'L8hWquwn7hcSOGgYqu67KtDLxwqVTGlz') // Add API key to request for authorization

        let response = null;
        try {
            const fetchResponse = await fetch("http://localhost:5000" + url + '?' + parameters.toString(), {
            mode: 'cors',
            method: 'DELETE',
            headers: headers
            })
            .catch(error => console.log('Request failed : ' + error.message));
            
            response = await fetchResponse.json();
        } catch (error) {
            console.error(error);
        }

        return response;
    }

    
    async post_Query(url, start_date, end_date){
        // Used to send POST requests to any of the POST routes for the different query types
        let headers = new Headers();
        let parameters = new URLSearchParams({
            start_date: start_date,
            end_date: end_date
        })

        // Route and functio returns message on the state of the request - complete or failed
        headers.append('Authorization', 'L8hWquwn7hcSOGgYqu67KtDLxwqVTGlz') // Add API key to request for authorization

        let response = null;
        try {
            const fetchResponse = await fetch("http://localhost:5000" + url + '?' + parameters.toString(), {
            mode: 'cors',
            method: 'POST',
            headers: headers
            })
            .catch(error => console.log('Request failed : ' + error.message));
            
            response = fetchResponse;
        } catch (error) {
            console.error(error);
        }

        return response;
    }
    
    formatDate(date) {    
        // Formats the gvien date to %Y-%m-%d - Required format for Financial analysis system API and order management system API
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        
        return `${year}-${month}-${day}`;
    }
    convertCalendarDate(date){
        // Convert to date from %d/%m/%Y 
        let date_split = date.split('/')
        let day = date_split[0]
        let month = date_split[1]
        let year = date_split[2]
        return new Date(year, month, day)
    }
}
