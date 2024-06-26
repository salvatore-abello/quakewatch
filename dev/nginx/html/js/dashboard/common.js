let loggedIn = false;

function getCSRFToken(){
    let csrf = document.cookie.match(/csrf_access_token=([^;]+)/);
    return csrf ? csrf[1] : null;
}

async function rfetch(url, options) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            window.location.href = '/login';
        }
        if(!loggedIn){
            loggedIn = true;
            $("#navbar-list").append('<li class="nav-item mx-2"><a class="nav-link" href="/logout">Logout</a></li>');
        }
        return response;
 
    } catch (error) {
        console.log(error);
    }
}

