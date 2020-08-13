document.addEventListener('DOMContentLoaded', function() {
    // By default, load all
    load_all();
    // Comment click
    const comments = document.querySelectorAll(".comment")
    comments.forEach(
        function(ct) {
            ct.addEventListener('click', (event) => {
                event.preventDefault();
                console.log('Comment was clicked');
                load_comment(event.target.id);
            });
        }
    );
    // Like click
    const likes = document.querySelectorAll("i[name='heart']")
    likes.forEach(
        function(lk) {
            lk.addEventListener('click', (event) => {
                event.preventDefault();
                console.log('Like was clicked');
                update_likes(event.target.id);
            });
        }
    );
});

function load_all() {
    // Display all posts only
    document.querySelector('#posts').style.display = 'block';
    document.querySelector('#comment').style.display = 'none';
}

function load_comment(post_id) {
    // Display comment only
    document.querySelector('#posts').style.display = 'none';
    document.querySelector('#comment').style.display = 'block';

    console.log('Comment div is being loaded');
    // Comment submit click
    document.querySelector("#comment-submit").addEventListener('click', (event) => {
        event.preventDefault();
        console.log('Comment submit was clicked');
        send_comment(post_id);
    });
}

function send_comment(post_id) {
    var c = document.querySelector("#id_comment").value;
    console.log(`New comment: ${c}`);
    // PUT
    fetch(`/${post_id}`, {
        method: 'PUT',
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            comment: c,
        })
    })
    .then(response => response.json());
    console.log('Comment submitted');
    load_all();
}

function update_likes(post_id) {
    // Select current like info
    var n = $('span[class="num-like"]'+'[id=' + CSS.escape(post_id) + ']').html();
    var h = $('i[name="heart"]' + '[id=' + CSS.escape(post_id) + ']').css('color');

    console.log(`Selected id: ${post_id}, #: ${n}, color: ${h}`);

    // +1
    if (h === 'rgb(128, 128, 128)') {
        n++;
        $('span[class="num-like"]' + '[id=' + CSS.escape(post_id) + ']').html(n);
        $('i[name="heart"]' + '[id=' + CSS.escape(post_id) + ']').css('color', 'red');
    }
    // -1
    if (h === 'rgb(255, 0, 0)') {
        n--;
        $('span[class="num-like"]' + '[id=' + CSS.escape(post_id) + ']').html(n);
        $('i[name="heart"]' + '[id=' + CSS.escape(post_id) + ']').css('color', 'gray');
    }

    // PUT
    fetch(`/${post_id}`, {
        method: 'PUT',
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            likes: n,
        }),
    })
    .then(response => response.json())
    console.log(`# likes updated to ${n}`);
    load_all();
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