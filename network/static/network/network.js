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
