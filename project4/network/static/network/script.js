document.addEventListener('DOMContentLoaded', () => {

    // Add event listeners
    document.querySelector('#submit-new-post').addEventListener('click', () => {
        addNewPost();
    })

})

// Add new post
function addNewPost() {
    
    // Get post text
    postText = document.querySelector('#new-post').value;

    // Send to server
    fetch('/new', {
        method: 'POST',
        body: JSON.stringify({
            text: postText,
            username: document.querySelector('#username').innerHTML
        })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);

            // Refresh posts
            fetchAllPosts();
        })
        .catch(error => {
            console.log(error);
        });
}

function fetchAllPosts() {
    fetch('/all')
        .then(response => response.json())
        .then(emails => {
            // Print emails
            console.log(emails);

            // ... do something else with emails ...
        })
        .catch(error => {
            console.log(error);
        });
}