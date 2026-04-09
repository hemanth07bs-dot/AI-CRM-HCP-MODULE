import React, { useState } from "react";
import "./App.css";

function App() {
  const [hcp, setHcp] = useState("");
  const [type, setType] = useState("");
  const [date, setDate] = useState("");
  const [notes, setNotes] = useState("");
  const [outcome, setOutcome] = useState("");
  const [followup, setFollowup] = useState("");

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const send = async () => {
    if (!input) return;

    // user bubble
    setMessages(prev => [...prev, { role: "user", text: input }]);

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/chat?input=" + encodeURIComponent(input)
      );

      const data = await res.json();
      const r = data.response.response;

      // clear tool
      if (r.clear) {
        setHcp("");
        setType("");
        setDate("");
        setNotes("");
        setOutcome("");
        setFollowup("");

        setMessages(prev => [
          ...prev,
          { role: "bot", text: "Form cleared" }
        ]);

        setInput("");
        return;
      }

      // update form
      if (r.hcp) setHcp(r.hcp);
      if (r.type) setType(r.type);
      if (r.date) setDate(r.date);
      if (r.notes) setNotes(r.notes);
      if (r.sentiment) setOutcome(r.sentiment);
      if (r.followup) setFollowup(r.followup);

      setMessages(prev => [
        ...prev,
        { role: "bot", text: "Form updated using AI tool" }
      ]);

    } catch {
      setMessages(prev => [
        ...prev,
        { role: "bot", text: "Backend not running" }
      ]);
    }

    setInput("");
  };

  const logInteraction = () => {
    setMessages(prev => [
      ...prev,
      { role: "bot", text: "Interaction logged successfully" }
    ]);
  };

  return (
    <div className="app">

      <h2 className="title">AI CRM HCP</h2>

      <div className="container">

        {/* LEFT PANEL */}
        <div className="card left">

          <div className="form-title">Log HCP Interaction</div>

          <input
            placeholder="HCP Name"
            value={hcp}
            readOnly
          />

          <input
            placeholder="Interaction Type"
            value={type}
            readOnly
          />

          <input
            placeholder="Date"
            value={date}
            readOnly
          />

          <textarea
            placeholder="Topics discussed"
            value={notes}
            readOnly
          />

          <div className="radio-group">
            <label>
              <input
                type="radio"
                checked={outcome === "Positive"}
                readOnly
              />
              Positive
            </label>

            <label>
              <input
                type="radio"
                checked={outcome === "Neutral"}
                readOnly
              />
              Neutral
            </label>

            <label>
              <input
                type="radio"
                checked={outcome === "Negative"}
                readOnly
              />
              Negative
            </label>
          </div>

          <input
            placeholder="Follow up"
            value={followup}
            readOnly
          />

          <button onClick={logInteraction}>
            Log Interaction
          </button>

        </div>


        {/* RIGHT PANEL */}
        <div className="card right">

          <div className="chat-header">
            AI Assistant
          </div>

          <div className="chat-box">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`msg ${m.role === "user" ? "user" : "bot"}`}
              >
                {m.text}
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              placeholder="Describe interaction..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
            />
            <button onClick={send}>
              Send
            </button>
          </div>

        </div>

      </div>
    </div>
  );
}

export default App;