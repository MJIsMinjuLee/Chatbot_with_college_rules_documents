
const chatContainer = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', () => {
    const message = messageInput.value;
    displayUserMessage(message);
    sendMessageToPython(message);
    messageInput.value = '';
    scrollChatToButtom();
});

function displayUserMessage(message) {
    const userMessage = document.createElement('div');
    userMessage.className = 'message user-message';
    userMessage.textContent = message;
    chatContainer.appendChild(userMessage);
}

function displayBotMessage(message) {
    const botMessage = document.createElement('div');
    botMessage.className = 'message bot-message';
    botMessage.textContent = message;
    chatContainer.appendChild(botMessage);
}

function scrollChatToButtom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

//파이썬 백엔드 연결//
function sendMessageToPython(message) {
    fetch('/process', {
        method: 'POST',
        headers : {
            'Content-Type' : 'application/json',
        },
        body : JSON.stringify({ message: message}),
    })
    .then(response => response.json())
    .then(data => {
        const botReply = data.message;
        displayBotMessage(botReply);
        scrollChatToButtom();
    })
    .catch(error => {
        console.error('Error sending message to backend : ', error);
    });
}
