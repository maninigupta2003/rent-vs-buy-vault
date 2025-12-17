import { useState } from "react";
import { chat } from "../services/api";

export default function ChatInterface({ analysis }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    const response = await chat({ analysis });
    setMessages([...messages, response.message]);
    setLoading(false);
  };

  return (
    <div style={{ marginTop: "30px" }}>
      <button onClick={sendMessage}>
        Explain My Situation
      </button>

      {loading && <p>Thinking…</p>}

      {messages.map((m, i) => (
        <p key={i} style={{ marginTop: "10px" }}>
           {m}
        </p>
      ))}
    </div>
  );
}
