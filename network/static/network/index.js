// function edit_post() {

// }
function post_comment(e, id) {
    e.preventDefault();
    let post_id = id.split('-').pop();
    let path = '/comment/';
    path = path.concat(post_id);
    console.log(path)
    fetch(path, {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        mode: 'same-origin',
        body: JSON.stringify({
            comment_content: document.querySelector('#commentcontent-'+post_id).value
        })
      })
      .then(response => response.json())
      .then(result => {
        console.log(result)
        document.querySelector('#commentcontent-'+post_id).value = '';
        load_comments(id);
      });
}

function like_post(id) {
    let post_id = id.split('-').pop()
    document.querySelector('#post-'+post_id).innerHTML = "fuck you";
}

function load_comments(id) {
    let post_id = id.split('-').pop();
    let path = '/comment/';
    path = path.concat(post_id);
    fetch(path)
    .then(response => response.json())
    .then(result => {
        document.querySelector('#comment-'+post_id).innerHTML = '';
        result.forEach(comment => {
            const element_div = document.createElement('div');
            const author = document.createElement('h3');
            const comment_content = document.createElement('p');
            author.innerHTML = comment.author;
            comment_content.innerHTML = comment.content;
            element_div.appendChild(author);
            element_div.appendChild(comment_content);
            document.querySelector('#comment-'+post_id).append(element_div);
        });
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}