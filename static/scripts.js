class Chatbox {
    constructor() {
        this.args = {
            chatBox: document.querySelector('.chatbox'),
            sendButton: document.querySelector('.send__button')
        };

        this.messages = [];
        this.initializeMessages();
    }

    initializeMessages() {
        this.messages.push({
            name: "Sam",
            message: "Hi there 👋. How can I assist you today?"
        });

        this.updateChatText(this.args.chatBox);
    }

    display() {
        const { chatBox, sendButton } = this.args;

        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const input = chatBox.querySelector('input');
        input.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    async onSendButton(chatbox) {
        const textField = chatbox.querySelector('input');
        const text = textField.value.trim();
        textField.value = ''; // Clear the input field immediately

        if (text === "") {
            return;
        }

        this.messages.push({ name: "User", message: text });
        this.updateChatText(chatbox);

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                body: JSON.stringify({ query: text }),
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            this.messages.push({ name: "Sam", message: data.message });
        } catch (error) {
            console.error('Error:', error);
            this.messages.push({ name: "Sam", message: "An error occurred. Please try again." });
        } finally {
            this.updateChatText(chatbox);
        }
    }

    updateChatText(chatbox) {
        const chatMessages = chatbox.querySelector('.chatbox__body');

        chatMessages.innerHTML = this.messages.map(item => `
            <div class="message ${item.name === 'Sam' ? 'bot-message' : 'user-message'}">
                <div class="avatar">
                    ${item.name === 'Sam' ? '<img src="https://img.icons8.com/color/48/000000/circled-user-female-skin-type-5--v1.png" alt="bot">' : ''}
                </div>
                <div class="text">
                    ${item.message}
                </div>
            </div>
        `).join('');

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

const chatbox = new Chatbox();
chatbox.display();
