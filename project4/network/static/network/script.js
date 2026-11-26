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

function loadProfile(username) {

    // Hide other divs and display profile div
    console.log(`document.querySelector('#all-posts'): ${document.querySelector('#all-posts')}`);
    console.log(`document.querySelector('#all-posts').tagName: ${document.querySelector('#all-posts').tagName}`);
    console.log(`typeof document: ${typeof document}`);
    document.querySelector('#all-posts-div').style.display = 'none';
    document.querySelector('#profile').style.display = 'block';

    console.log(`FETCHING PROFILE: ${username}`)
    fetch(`/profile/${username}`)
        .then(response => response.json())
        .then(data => {
            document.querySelector('#profile-username').innerHTML = data.username;

            // Display the number of followers the user has,
            document.querySelector('#followers').innerHTML = `${data.followers} follower(s)`;

            // as well as the number of people that the user follows.
            document.querySelector('#following').innerHTML = `Following ${data.following}`;
            
            // Display all of the posts for that user, in reverse chronological order.
            // Clear posts
            document.querySelector('#profile-posts').innerHTML = ''

            // Add div for each post
            data.posts.forEach(function(post) {
                addPost(post, 'profile-posts');
            });

            // For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. 
            // Note that this only applies to any “other” user: a user should not be able to follow themselves.
            // If user signed in - handled by template
                // If profile not user's
                if (data.username !== data.visitor){
                    
                    // If user not following profile
                        // Button to follow 
                    // Else button to unfollow
                    document.querySelector('#follow-button').innerHTML = !data.is_following ? 'Follow' : 'Unfollow';
                    }
            // Else don't display button
            
        })
        .catch();
}

// Add a new post with given contents to DOM
function addPost(contents, div) {

    // Create new post
    const post = document.createElement('div');
    post.className = 'post';
    post.innerHTML = `<div class="card mt-3">
        <div class="card-body">
            <h4 class="card-title fg-3 post-username">${contents.poster}</h4>
            <p class="card-subtitle fg-3 post-timestamp">${contents.timestamp}</p>
            <p class="card-text fg-3 post-text">${contents.text}</p>
            <p class="card-text fg-3 post-likes">${contents.likes} like(s)</p>
        </div>
        </div>`;

    // Add link to poster's profile
    const username = post.querySelector('.post-username');
    username.addEventListener('click', function(event) {
        console.log('clicked!');
        loadProfile(username.innerHTML);
    });

    // Add post to DOM
    document.querySelector(`#${div}`).append(post);
};

function fetchPosts() {
    console.log('fetchPosts is running')

    // Show all posts div and hide the other views
    document.querySelector('#all-posts').style.display = 'block';
    document.querySelector('#profile').style.display = 'none';

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
    console.log(`FETCHING POSTS ${start} to ${end}`)
    fetch(`/posts?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(data => {
            // Print posts
            console.log(data.posts);

            // Clear posts
            document.querySelector('#posts').innerHTML = ''

            // Add div for each post 
            data.posts.forEach(function(post) {
                addPost(post, 'posts');
            });
        })
        .catch(error => {
            console.log(error);
        });
}