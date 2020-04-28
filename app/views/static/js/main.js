let socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on( 'connect', function() {
    console.log('Connected')
});

let chat = {
  container: document.querySelector('.container .right'),
  current: null,
  person: null,
  name: document.querySelector('.container .right .top .name')
};

let chats = document.querySelectorAll('.chat');
for (let _chat of chats) {
    let chat_id = _chat.getAttribute('data-chat');
    socket.emit('join', chat_id);
}

window.onload = function() {
    let first_person = document.querySelector('.person');
    if (first_person) {
        setAciveChat(first_person);
    }
};

console.log(chat);
function setAciveChat(element) {
    let active_person = document.querySelector('.active');
    if (active_person) {
        active_person.classList.remove('active');
    }
    element.classList.add('active');
    chat.current = chat.container.querySelector('.active-chat');
    chat.person = element.getAttribute('data-chat');

    let active_chat = chat.container.querySelector('[data-chat="' + chat.person + '"]');
    if (chat.current) {
        chat.current.classList.remove('active-chat');
    }
    active_chat.classList.add('active-chat');
    chat.name.innerHTML = element.querySelector('.name').innerText;

    let wrapper = active_chat.querySelector('.chat_wrapper');
    for (let element of wrapper.children) {
        element.classList.remove('notransition');
    }
    wrapper.scrollTo(0,wrapper.scrollHeight);
}

function getDatetime(){
    let today = new Date();
    return today.getFullYear() + "-" +
        ('0' + (today.getMonth() + 1)) + "-" +
        ('0' + today.getDate()).slice(-2) + " " +
        ('0' + today.getHours()).slice(-2) + ":" +
        ('0' + today.getMinutes()).slice(-2) + ":" +
        ('0' + today.getSeconds()).slice(-2);
}

// Send message
let message_input = document.getElementById("send_message");
message_input.onkeypress = async function(event){
    if (event.keyCode == 13 || event.which == 13){
        let message = message_input.value;
        if (!message) {
            return;
        }
        let active_person = document.querySelector('.active');
        let preview = active_person.querySelector('.preview');
        let chat_id = active_person.getAttribute('data-chat');
        let active_chat = chat.container
            .querySelector('[data-chat="' + chat_id + '"]');
        let wrapper = active_chat.querySelector('.chat_wrapper');

        let datetime = getDatetime();
        console.log(datetime);

        socket.emit('message', datetime, message, chat_id);
        message_input.value = '';
        wrapper.classList.add('notransition');
        for (let element of wrapper.children) {
            element.classList.add('notransition');
        }
        wrapper.innerHTML += `<div class="bubble me notransition">
                                    ${message}
                              </div>`;
        preview.innerHTML = message;
        wrapper.scrollTo(0,wrapper.scrollHeight);
    }
};


// Get message
socket.on( 'render_message', function( json_data ) {
    // {
    //     'sender_id',
    //     'chat_id',
    //     'datetime',
    //     'message'
    // }
    let person = document
        .querySelector('.left')
        .querySelector('[data-chat="' + json_data['chat_id'] + '"]');
    let preview = person.querySelector('.preview');
    let user_id = document.getElementById('user_id').value;
    let sender_id = json_data['sender_id'];
    let message = json_data['message'];
    let chat = document
        .querySelector('.right')
        .querySelector('[data-chat="' + json_data['chat_id'] + '"]')
        .querySelector('.chat_wrapper');
    if (user_id !== sender_id) {
         chat.innerHTML += `<div class="bubble you notransition">
                                ${message}
                            </div>`;
    preview.innerHTML = message;
    chat.scrollTo(0,chat.scrollHeight);
    }
});


// Search users
let searchInput = document.getElementById("search");
let searchElements = document.getElementById("aftersearch");
let searchInputTimeout = null;
searchInput.addEventListener('input', function (e) {
    clearTimeout(searchInputTimeout);
    if (searchInput.value) {
        searchInputTimeout = setTimeout(function () {
            searchElements.innerHTML = '<hr>';
            console.log('Search users by:', searchInput.value);
            let url = '/search';
            function displaySearch(users) {
                users.forEach(user => {
                    let userHtml =
                        `<li class=\"person\" data-chat=\"${user.id}\" onclick="startChat(this)">

                             <img src=\"https://robohash.org/${user.email_hash}?size=200x200\" alt=\"\" />
                             <span class=\"name\">${user.username}</span>
                             <br>
                             <span class=\"preview\">Click here to start conversation.</span>
                         </li>`;
                    searchElements.innerHTML += userHtml;
                });
            }
            fetch(url,{
                method:'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: searchInput.value })
            }).then(response => response.json())
              .then(users => displaySearch(users));
        }, 1000);
    } else {
        searchElements.innerHTML = ''
    }
});


function startChat(user) {
    fetch('/chat',{
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stranger_id: user.getAttribute('data-chat') })
    }).then(_ => location.reload());
}
