# Real-Time-chat-application
Real time chat application with features like instant messaging, user profile and group chats.

# Real-Time Python Chat App

A real-time chat application built with FastAPI, WebSockets, and SQLAlchemy.

## How to Run
1. **Clone the repo:**
   ```git clone <your-github-link>```
   ```cd Real-Time-chat-application```

pip install -r requirements.txt
Run server: ```uvicorn chat_app.main:app --reload```

---

### 3. How to Chat with someone on the SAME Wi-Fi
If you and your friend are on the same Wi-Fi, they don't even need to clone the code! You can host it, and they can join:

1.  Find your Local IP address (Run `ipconfig` on Windows, look for IPv4). It usually looks like `192.168.1.XX`.
2.  Run your server like this:
    ```bash
    uvicorn chat_app.main:app --host 0.0.0.0 --port 8000
    ```
3.  Tell your friend to go to `http://192.168.1.XX:8000` on their browser.
4.  **Boom!** You are now chatting across two different computers on the same network.



---

### 4. Summary of what happens
* **Username:** Allows the app to label who said what.
* **Room ID:** This is the "Secret Key." Only people with the exact same Room ID will be piped into the same `active_connections` list in your `manager.py`.

**Would you like me to help you write the final `requirements.txt` and the `README.md` file so your GitHub profile looks professional?**
