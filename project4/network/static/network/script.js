document.addEventListener('DOMContentLoaded', () => {

    // Add event listeners
    document.querySelector('#submit-new-post').addEventListener('click', () => {
        addNewPost();
    });
    document.querySelector('#new-post-form').addEventListener('submit', function(event) {
        event.preventDefault();
    });

})

// Add new post
function addNewPost() {
    
    // Get post text
    postText = document.querySelector('#new-post').value;

    // CSRF token
    csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const myHeaders = new Headers();
    myHeaders.append('X-CSRFToken', csrfToken);

    // Send to server
    fetch('/new', {
        method: 'POST',
        headers: myHeaders,
        body: postText
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);

            // Refresh posts
            fetchPosts();
        })
        .catch(error => {
            console.log(error);
        });
}

function fetchPosts() {

    // Show all posts div and hide the other views

    // Fetch posts

    fetch(`/all?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(posts => {
            // Print posts
            console.log(posts);

            // Add div for each post up to 10
            posts.forEach(post => {})

            // If more than 10
        })
        .catch(error => {
            console.log(error);
        });
}