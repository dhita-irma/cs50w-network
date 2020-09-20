document.addEventListener('DOMContentLoaded', function() {

    // Show sections
    document.querySelector('#all').addEventListener('click', () => load_post('all'));
    document.querySelector('#following').addEventListener('click', () => load_post('following'));

    // By deafult, load all posts 
    load_post('all');

});

function load_post(feed) {
    
    // Show feed title
    document.querySelector('#title').innerHTML = `${feed.toUpperCase()}`


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
                        <div class="card-header">
                            ${posts[i].creator}
                        </div>
                        <div class="card-body">
                        <blockquote class="blockquote mb-0">
                            <p>${posts[i].content}</p>
                            <footer class="blockquote-footer">${posts[i].timestamp}</footer>
                        </blockquote>
                        </div>
                    </div>
                `

                // Append postItem to #post
                postSection.appendChild(postItem);

            } // for
        }); // .then

} // func load_post