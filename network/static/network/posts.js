document.addEventListener('DOMContentLoaded', function() {

    const current_user = JSON.parse(document.getElementById('current-user').textContent);
    console.log(`Current logged in user: ${current_user}`);

    // Show sections
    document.querySelector('#all').addEventListener('click', () => load_post('all'));
    document.querySelector('#following').addEventListener('click', () => load_post('following'));
    document.querySelector('#logged-user').addEventListener('click', () => load_post(current_user));
    

    // Submit Post 
    document.querySelector('#create-post-btn').addEventListener('click', () => send_post());

    // By deafult, load all posts 
    load_post('all');


});

function load_post(feed) {
    
    if (feed === 'all' || feed === 'following') {
        // Show feed title
        document.querySelector('#title').innerHTML = `${feed.toUpperCase()}`;
        
        // Hide Profile section
        document.querySelector('#profile-view').style.display = 'none';
    } else {
        profile(feed);
    }

    // Clear post textarea
    document.querySelector('#post-content').value = "";

    fetch(`/posts/${feed}`)
        .then(response => response.json())
        .then(posts => {

            console.log(posts);

            // Clear inner HTML
            var postSection = document.querySelector('#posts');
            postSection.innerHTML = "";

            // Add post items
            for (var i = 0; i < posts.length; i++) {

                // Create div for each post 
                var postItem = document.createElement('div');
                postItem.className = 'post-item';

                postItem.innerHTML = `
                <div class="card mb-3">
                    <h5 class="card-header">${posts[i].creator}</h5>
                    <div class="card-body">
                        <p class="card-text">${posts[i].content}</p>
                    </div>
                    <div class="card-footer">${posts[i].timestamp}</div>
                </div>
                `

                // Append postItem to #post
                postSection.appendChild(postItem);

            } // for
        }); // .then

} // func load_post

function send_post() {

    const content = document.querySelector('#post-content').value;
    var token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    // Send post 
    fetch('/posts/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {"X-CSRFToken": token},
        body: JSON.stringify({
            content: content,
        }) 
    }) // fetch
    .then(response => response.json())
    .then(result => {
        console.log(result);
        load_post('all');
    }); //then

} // func send_post

function profile(username) {
    // Show user title & Profile section
    document.querySelector('#title').innerHTML = username;
    document.querySelector('#profile-view').style.display = 'block';

    // If requested user is not current_user, hide create post section
    const current_user = JSON.parse(document.getElementById('current-user').textContent);
    if (username !== current_user) {
        document.querySelector('#create-post').style.display = 'none';
    }

    // Show User profile detail 
    fetch(`/profile/${username}`)
        .then(response => response.json())
        .then(data => {

            console.log(data);

            // Show user data 
            var detailSection = document.querySelector('#user-detail');
            detailSection.innerHTML = `
                <h5>Following: ${data.following.length}</h5>
                <h5>Followers: ${data.followers.length}</h5>
            `
        }); // then

} // func profile 
