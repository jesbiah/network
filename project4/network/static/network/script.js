// To batch posts
let counter = 1;
const quantity = 10;

document.addEventListener('DOMContentLoaded', () => {

    // Add event listeners
    if (document.querySelector('#submit-new-post')) {
        document.querySelector('#submit-new-post').addEventListener('click', () => {
            addNewPost();
        });
        document.querySelector('#new-post-form').addEventListener('submit', function(event) {
            event.preventDefault();
        });
    }        

    fetchPosts();

})

// Add new post
function addNewPost() {
    
    // Get post text
    const postText = document.querySelector('#new-post').value;
    document.querySelector('#new-post').value = '';

    // CSRF token
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
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
            console.log('fetchPosts about to be called');
            counter = 1;
            fetchPosts();
            console.log('fetchPosts called');

            // Check for error message
            if (result.error) {
                let message = document.querySelector('#new-post-message');
                message.style.display = 'block';
                message.innerHTML = result.error;
            }
        })
        .catch(error => {
            console.log(error);
            let message = document.querySelector('#new-post-message');
            message.style.display = 'block';
            message.innerHTML = error;
        });
}

// Add a new post with given contents to DOM
function addPost(contents) {

    // Create new post
    const post = document.createElement('div');
    post.className = 'post';
    post.innerHTML = `<div class="card mt-3">
        <div class="card-body">
            <h4 class="card-title fg-3">${contents.poster}</h4>
            <p class="card-subtitle fg-3">${contents.timestamp}</p>
            <p class="card-text fg-3 post-text">${contents.text}</p>
            <p class="card-text fg-3">${contents.likes} likes</p>
        </div>
        </div>`;

    // Add post to DOM
    document.querySelector('#posts').append(post);
};

function fetchPosts() {
    console.log('fetchPosts is running')

    // Show all posts div and hide the other views

    if (document.querySelector('#new-post-message')) {
        let message = document.querySelector('#new-post-message');
        message.style.display = 'none';
        message.innerHTML = '';
    }
        
    // Set start and end post numbers, and update counter
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;

    // Fetch posts
    fetch(`/posts?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(data => {
            // Print posts
            console.log(data.posts);

            // Clear posts
            document.querySelector('#posts').innerHTML = ''

            // Add div for each post
            data.posts.forEach(addPost);
        })
        .catch(error => {
            console.log(error);
        });
}