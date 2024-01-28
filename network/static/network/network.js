// Global Variables
let like_count = 0;

function getCookie(name) {
    if (!document.cookie) {
      return null;
    }
  
    const xsrfCookies = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));
  
    if (xsrfCookies.length === 0) {
      return null;
    }
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
  }

// Whitespace message charactere count validation
function msgValidation(msg, target) {
    const newpost_msg = document.querySelector(`#${target}`);
    length = msg.replace(/^\s+|\s+$/gm,'').length;
    if (length === 0) {
        newpost_msg.innerHTML = 'Enter at least 15 characters';
        reset_animation(target);
        return false;
    }
    if (length < 15) {
        newpost_msg.innerHTML = `${15 - length} more to go...`;
        reset_animation(target);
        return false;
    }
    return true;
}

  function reset_animation(elem) {
    const el = document.querySelector(`#${elem}`);
    el.style.animation = 'none';
    el.offsetHeight; /* trigger reflow */
    el.style.animation = null; 
  }

  function stop_animation(elem) {
    console.log(elem);
    let el = document.querySelector(`#${elem}`);
    el.style.animation = 'none';
  }

document.addEventListener('DOMContentLoaded', ()=> {
    document.querySelectorAll('.areaEdition').forEach(textarea => {
        textarea.style.display="none";
    });
    document.querySelectorAll('.edition_post_button').forEach(button => {
        button.style.display="none";
    });
    // Athenticated users menu event listener
    if (user !== "AnonymousUser"){
        document.querySelector('#nav_user').addEventListener('click', ()=> {
            profile("Profile");
        });
        document.querySelector('#nav_following').addEventListener('click', ()=> {
            posts("Following");
        });
        
        // Post Edition
        document.querySelectorAll('.post_edit').forEach(edit_button => {
            edit_button.addEventListener('click', postEdit);
        });

        // Post Like/Unlike
        document.querySelectorAll('[title=like]').forEach(like_div => {
            like_div.addEventListener('click', like_unlike);
        });
    }
    document.querySelector('#nav_allposts').addEventListener('click', ()=> {
        posts("All Posts");
    });
    
    // Navigation menu choosen
    switch(group) {
        case "All Posts":
            posts(group);
            break;
        case "Following":
            posts(group);
            break;
        case "Profile":
            profile(group);
            break;
        default:
            posts("All Posts");
            break;
    }

});

// Show Posts
function posts(group) {
    document.querySelector('#title').innerHTML=group;
    document.querySelector('#posts').style.display = 'block';
    document.querySelector('#profile').style.display = 'none';
    if (user !== "AnonymousUser"){
        document.querySelector('#newpost').onsubmit = ()=> {
            const msg = document.querySelector('#textareaPost').value;
            // Whitespace handling
            if (!msgValidation(msg, "newpost_msg")) {
                return false;
            }
            dateTime = new Date().toLocaleString();
            csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
            // let csrftoken = getCookie('csrftoken');
            fetch('/msg', {
                method: 'POST',
                body: JSON.stringify({
                    post: msg
                }),
                headers: { "X-CSRFToken": csrftoken },
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
                document.querySelector('#textareaPost').value = "";
                document.querySelector('#newpost_msg').innerHTML = `Post sent successfully. (${dateTime})`;
                reset_animation('newpost_msg');
            });

            return false;
        }
    }
}

// Show profile
function profile(group) {
    document.querySelector('#title').innerHTML=group;
    document.querySelector('#posts').style.display = 'none';
    document.querySelector('#profile').style.display = 'block';
}

// Edit post
function postEdit(event) {
    const post_id = this.dataset.post_id;
    const post_p_id = this.dataset.post_p_id;
    const textarea_id = this.dataset.textarea_id;
    const post_button_id = this.dataset.edition_button_id;
    const post_form_id = this.dataset.post_form_id;
    const newpost_msg_eddition_id = this.dataset.newpost_msg_eddition_id;
    const button = event.target;

    const post = document.querySelector(`#${post_p_id}`);
    const textarea = document.querySelector(`#${textarea_id}`);
    const post_button = document.querySelector(`#${post_button_id}`);
    const newpost_msg = document.querySelector(`#${newpost_msg_eddition_id}`);
    const newpost_msg_eddition = document.querySelector(`#${newpost_msg_eddition_id}`);

    // Pressing Edit Button
    if (button.value === "edit") {
        if (textarea.style.display === "none") {
            if(textarea.value === ""){textarea.value = post.innerHTML;}
            post.style.display = "none";
            textarea.style.display = "block";
            button.innerHTML = "Cancel";
            post_button.style.display="block";
            document.querySelector(`#${post_form_id}`).onsubmit = () => {
                const msg = textarea.value;
                // Witespace Handling
                if(!msgValidation(msg, newpost_msg_eddition_id)) {
                    return false;
                }
                if( msg == post.innerHTML) {
                    newpost_msg_eddition.innerHTML = 'No changes found!';
                    reset_animation(newpost_msg_eddition_id);
                    return false;
                } else {
                    newpost_msg_eddition.innerHTML = '';
                }

                dateTime = new Date().toLocaleString();
                csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
                fetch(`/posts/edit?id=${post_id}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        post: msg
                    }),
                    headers: { "X-CSRFToken": csrftoken },
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                    post.innerHTML = textarea.value;
                    textarea.value = "";
                    button.innerHTML = "Edit";
                    post.style.display = "block";
                    textarea.style.display = "none";
                    post_button.style.display="none";
                    newpost_msg_eddition.innerHTML = `Update Post sent successfully. (${dateTime})`;
                    reset_animation(newpost_msg_eddition_id);
                });
                return false;
            }
        } else {
            button.innerHTML = "Edit";
            post.style.display = "block";
            // textarea.innerHTML = "";
            textarea.style.display = "none";
            post_button.style.display="none";
            newpost_msg.innerHTML = "";
        }
    }
}

function like_unlike(event) {
    // Initialize
    let likestyle = this.className;
    const post_id = this.dataset.post_id;
    const like_count_id = this.dataset.like_count_id;
    const post_user_id = this.dataset.user_id;

    const like_count = document.querySelector(`#${like_count_id}`);

    if(user_id != post_user_id) {
        if(likestyle === "like no") {
            this.title = "Unlike";
            this.className = "like yes";

            csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
            fetch(`/posts/like?post_id=${post_id}`, {
                method: "PUT",
                body: JSON.stringify({
                    like: true
                }),
                headers: { "X-CSRFToken": csrftoken },
            })
            .then(response => like_count.innerHTML = parseInt(like_count.innerHTML) + 1)
        } else if (likestyle === "like yes") {
            this.title = "Like";
            this.className = "like no";

            csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
            fetch(`/posts/like?post_id=${post_id}`, {
                method: "PUT",
                body: JSON.stringify({
                    like: false
                }),
                headers: { "X-CSRFToken": csrftoken },
            })
            .then(response => like_count.innerHTML = parseInt(like_count.innerHTML) - 1)
        }
    }
}
