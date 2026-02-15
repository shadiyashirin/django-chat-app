import { useEffect, useRef, useState } from "react";
import { logout } from "./api";

function Chat({ token, roomId }) {
  const [messages, setMessages] = useState([]);
  const socketRef = useRef(null);

  useEffect(() => {
    const socket = new WebSocket(
      `ws://127.0.0.1:8000/ws/chat/${roomId}/?token=${token}`
    );

    socket.onopen = () => {
      console.log("WebSocket Connected");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prev) => [...prev, data]);
    };

    socket.onclose = () => {
      console.log("WebSocket Closed");
    };

    socket.onerror = (error) => {
      console.error("WebSocket Error:", error);
    };

    socketRef.current = socket;

    return () => {
      socket.close();
    };
  }, [roomId, token]);

  const sendMessage = (text) => {
    if (socketRef.current) {
      socketRef.current.send(JSON.stringify({ text }));
    }
  };

  return (
    <div>
      <h2>Chat Room {roomId}</h2>

      <div style={{ border: "1px solid gray", height: "300px", overflowY: "scroll" }}>
        {messages.map((msg, index) => (
          <div key={index}>
            <strong>{msg.sender}:</strong> {msg.message}
          </div>
        ))}
      </div>

      <button onClick={() => sendMessage("Hello from React!")}>
        Send Test Message
      </button>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

export default Chat;
