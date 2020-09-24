function toggleEditBtn(id) {
    console.log(`You are editing post ${id}`)

    var cardBody = document.getElementById(`${id}`).getElementsByClassName('card-body')[0];
    var textArea = cardBody.getElementsByClassName('edit-post')[0];
    var cardText = document.getElementById(`${id}`).getElementsByClassName('card-text')[0];

    // Toggle TextArea 
    if (textArea.style.display === 'none') {
        textArea.style.display = 'block';
        cardText.style.display = 'none';
    } else {
        textArea.style.display = 'none';
        cardText.style.display = 'block';
    }

}

function editPost(id) {

    const content = document.getElementById(`${id}`).getElementsByClassName('card-body')[0].getElementsByClassName('edit-post')[0].value;
    
    // Get requested post
    fetch(`/posts/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
    });
}

function createPost() {
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
        console.log(result.post_id);

        // Fetch new post
        fetch(`/posts/${result.post_id}`)
        .then(response => response.json())
        .then(post => {
            console.log(post)

            addPost(post);
        });

        
    }); //then
}

// function addPost(post) {

//     // Create post item
//     var postItem = document.createElement('div');
//     postItem.innerHTML = `
//     <div id="{{ ${post.id} }}" class="card mb-3">
//     <!-- Post Header -->
//     <div class="card-header pb-1 pt-2">
//         <div class="row">
//             <div class="col-10">
//                 <a href="{% url 'profile' post.creator %}">
//                     <h5 class=" post-creator">{{ ${post.creator} }}</h5>
//                 </a>
//             </div>
//             <!-- Edit Button -->
//             {% if user == post.creator %}
//             <div class="col-2 text-right">
//                 <i class="fas fa-edit" onclick="editPost('{{ ${post.id} }}')"></i>
//             </div>
//             {% endif %}
//         </div>
//     </div>
//     <!-- Post Body -->
//     <div class="card-body">
//         <p class="card-text">{{ ${post.content} }}</p>
//     </div>
//     <!-- Post Footer -->
//     <div class="card-footer">
//         <div class="row">
//             <div class="col-6">
//                 <i class="fa fa-thumbs-up"> {{ ${post.like_count} }} likes</i>
//             </div>
//             <div class="col-6 text-right">{{ ${post.timestamp} }}</div>
//         </div>
//     </div>
//     </div>
//     `

//     // Insert postItem
//     var postSection = document.querySelector('#posts');
//     postSection.insertAdjacentElement("afterbegin", postItem);      
// }