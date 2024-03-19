function edit_post(id) {
    let post_id = id.split('-').pop();
    const post_content = document.querySelector('#post-' + post_id);
    const edit_form = document.createElement('form');
    const textarea = document.createElement('textarea');
    textarea.setAttribute("rows", "4");
    textarea.innerHTML = post_content.innerHTML;
    const submit = document.createElement('input');
    submit.setAttribute("type", "submit");
    edit_form.appendChild(textarea);
    edit_form.appendChild(submit);
    post_content.innerHTML = '';
    document.querySelector('#' + id).style.display = 'none';
    post_content.append(edit_form);
    edit_form.addEventListener('submit', (e) => {
        e.preventDefault();
        let path = '/editpost/';
        path = path.concat(post_id);
        fetch(path, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            mode: 'same-origin',
            body: JSON.stringify({
                post_content: textarea.value
            })
        })
            .then(response => response.json())
            .then(result => {
                console.log(result);
                fetch(path)
                    .then(response => response.json())
                    .then(result => {
                        post_content.innerHTML = result.content;
                        document.querySelector('#' + id).style.display = 'block';
                    })
            });
    });
}
function post_comment(e, id) {
    e.preventDefault();
    let post_id = id.split('-').pop();
    let path = '/postcomment/';
    path = path.concat(post_id);
    fetch(path, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        mode: 'same-origin',
        body: JSON.stringify({
            comment_content: document.querySelector('#commentcontent-' + post_id).value
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
            document.querySelector('#commentcontent-' + post_id).value = '';
            load_comments(id);
        });
}

function like_post(id) {
    let post_id = id.split('-').pop();
    let path = '/like/';
    path = path.concat(post_id);
    fetch(path, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        mode: 'same-origin'
    })
        .then(response => response.json())
        .then(result => {
            document.querySelector('#' + id).innerHTML = result.btn_status;
            document.querySelector('#likecount-' + post_id).innerHTML = result.like_count + ' likes';
        })
}

function load_comments(id) {
    let post_id = id.split('-').pop();
    let path = '/getcomment/';
    path = path.concat(post_id);
    fetch(path)
        .then(response => response.json())
        .then(result => {
            document.querySelector('#allcomments-' + post_id).innerHTML = '';
            result.forEach(comment => {
                const element_div = document.createElement('div');
                const author = document.createElement('h5');
                author.className = "fw-bold";
                const profile_url = document.createElement('a');
                profile_url.className = "text-decoration-none";
                profile_url.setAttribute("href", "/profile/"+comment.author);
                const comment_content = document.createElement('p');
                author.innerHTML = comment.author;
                profile_url.appendChild(author);
                comment_content.innerHTML = comment.content;
                element_div.appendChild(profile_url);
                element_div.appendChild(comment_content);
                target_element = document.querySelector('#allcomments-' + post_id);
                target_element.append(element_div);
            });
        });
    if (document.querySelector('#comment-' + post_id).style.display == 'block') {
        document.querySelector('#comment-' + post_id).style.display = 'none';
        document.querySelector('#loadcomment-' + post_id).innerHTML = 'show comments';
    }
    else {
        document.querySelector('#comment-' + post_id).style.display = 'block';
        document.querySelector('#loadcomment-' + post_id).innerHTML = 'hide comments';
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}