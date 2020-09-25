function createPost(e) {

    // Get content and token
    const content = document.querySelector('#post-content').value;
    const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    // Preven submision if content is empty
    if (content === "") {
        e.preventDefault;
    } else {
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
            console.log(result.post_id);
    
            // Fetch new post
            fetch(`/posts/${result.post_id}`)
            .then(response => response.json())
            .then(post => {
                console.log(post)
            });
        }); //then
    }
}


function toggleEditBtn(id) {

    // Get post editor element and card-text element
    var cardBody = document.getElementById(`${id}`).getElementsByClassName('card-body')[0];
    var textArea = cardBody.getElementsByClassName('edit-post')[0];
    var cardText = document.getElementById(`${id}`).getElementsByClassName('card-text')[0];

    // Toggle post editor  
    if (textArea.style.display === 'none') {
        textArea.style.display = 'block';
        cardText.style.display = 'none';
    } else {
        textArea.style.display = 'none';
        cardText.style.display = 'block';
    }

}


function editPost(id) {
    
    // Get elements that contains new post content
    var cardBody = document.getElementById(`${id}`).getElementsByClassName('card-body')[0];
    var content = cardBody.getElementsByClassName('edit-content')[0].value;
    const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    // Update post content in the database
    fetch(`/posts/${id}`, {
        method: 'PUT',
        credentials: 'same-origin',
        headers: {"X-CSRFToken": token},
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json())
    .then(result => {

        // Print success message 
        console.log(result)

        // Update post content on the webpage
        var cardText = document.getElementById(`${id}`).getElementsByClassName('card-text')[0];
        cardText.innerHTML = content;

        // Hide post editor and show post content
        toggleEditBtn(id);
    });
}


function toggleFollow(btn, id) {

    const token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    // Follow / unfollow user 
    fetch(`/follow/${id}`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {"X-CSRFToken": token}
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)

        // Update followers count
        var followersCount = document.querySelector('#followers-count');
        followersCount.innerHTML = `Followers: ${result.followers_count}`

        // Change button
        if (btn.classList.contains("btn-primary")) {
            btn.innerHTML = "Unfollow";
            btn.classList.remove("btn-primary")
            btn.classList.add("btn-danger")
    
        } else {
            btn.innerHTML = "Follow";
            btn.classList.remove("btn-danger")
            btn.classList.add("btn-primary")
        }

    }) // then

}