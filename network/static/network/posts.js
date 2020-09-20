document.addEventListener('DOMContentLoaded', function() {

    // Show sections
    document.querySelector('#all').addEventListener('click', () => load_post('all'));
    document.querySelector('#following').addEventListener('click', () => load_post('following'));

    // Submit Post 
    document.querySelector('#create-post-btn').addEventListener('click', () => send_post());

    // By deafult, load all posts 
    load_post('all');

});

function load_post(feed) {
    
    // Show feed title
    document.querySelector('#title').innerHTML = `${feed.toUpperCase()}`

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