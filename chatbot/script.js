document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // !!! IMPORTANT: PASTE YOUR N8N PRODUCTION WEBHOOK URL HERE !!!
    const N8N_WEBHOOK_URL = 'http://localhost:5678/webhook/7c4a9a0f-af89-469a-81fe-e35d0c854fdd'; 

    const botAvatarSvg = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,2C6.486,2,2,6.486,2,12s4.486,10,10,10c5.514,0,10-4.486,10-10S17.514,2,12,2z M12,20c-4.411,0-8-3.589-8-8 s3.589-8,8-8s8,3.589,8,8S16.411,20,12,20z"></path>
            <path d="M12,5c-3.859,0-7,3.141-7,7s3.141,7,7,7s7-3.141,7-7S8.141,5,12,5z M12,17c-2.757,0-5-2.243-5-5s2.243-5,5-5 s5,2.243,5,5S14.757,17,12,17z"></path>
            <path d="M12,9c-1.626,0-3,1.374-3,3s1.374,3,3,3s3-1.374,3-3S13.626,9,12,9z"></path>
        </svg>`;

    // Add a message to the chat window
    const addMessage = (text, sender) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);

        let messageContentHtml = '';
        if (sender === 'bot') {
            messageContentHtml = `
                <div class="avatar">${botAvatarSvg}</div>
                <div class="message-content">${text}</div>
            `;
        } else {
            messageContentHtml = `<div class="message-content">${text}</div>`;
        }
        
        messageElement.innerHTML = messageContentHtml;
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    };

    // Add the typing indicator
    const showTypingIndicator = () => {
        const typingIndicator = document.createElement('div');
        typingIndicator.id = 'typing-indicator';
        typingIndicator.classList.add('message', 'bot-message');
        typingIndicator.innerHTML = `
            <div class="avatar">${botAvatarSvg}</div>
            <div class="message-content">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        `;
        chatMessages.appendChild(typingIndicator);
        scrollToBottom();
    };

    // Remove the typing indicator
    const hideTypingIndicator = () => {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    };
    
    // Auto-scroll to the latest message
    const scrollToBottom = () => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    // Send message to n8n and get response
    const sendMessage = async () => {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        addMessage(messageText, 'user');
        userInput.value = '';
        showTypingIndicator();

        try {
            const response = await fetch(N8N_WEBHOOK_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: messageText }),
            });

            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

            const data = await response.json();
            
            hideTypingIndicator();
            if (data.response) {
                addMessage(data.response, 'bot');
            } else {
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }

        } catch (error) {
            console.error('Error sending message to n8n:', error);
            hideTypingIndicator();
            addMessage('Could not connect to the AI. Please check the connection.', 'bot');
        }
    };

    // Event Listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') sendMessage();
    });

    // Initial disclaimer message
    const disclaimer = `Hello! I'm a supportive AI companion here to listen. <br><br>
        <strong>IMPORTANT DISCLAIMER:</strong> I am an AI and not a substitute for a human therapist or medical professional. My purpose is to be a listening ear, not to provide diagnosis, treatment, or medical advice. <br><br>
        If you are in a crisis or feel you are a danger to yourself or others, please contact a local emergency service immediately. <br><br>
        You can start by telling me what's on your mind.`;
    
    addMessage(disclaimer, 'bot');
});