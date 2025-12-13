import { useNavigate } from "react-router";
import { useState } from "react";


export default function AddDomainForm() {
  const [domain, setDomain] = useState("");
  const [message, setMessage] = useState("");
  const [messageColor, setMessageColor] = useState("green");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!domain.trim()) {
      setMessage("Please enter a domain.");
      setMessageColor("red");
      return;
    }

    try {
      const response = await fetch("http://localhost/api/add_domain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ domain }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Domain added successfully!");
        setMessageColor("green");
        setDomain("");
        navigate("/");
      } else {
        setMessage(data.detail || "Error adding domain");
        setMessageColor("red");
      }
    } catch (error) {
      console.error(error);
      setMessage("Failed to connect to server.");
      setMessageColor("red");
    }
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit} className="form">
        <h2 className="title">Add Domain</h2>
        <input
          type="text"
          placeholder="Enter URL http://www.example.com"
          value={domain}
          onChange={(e) => setDomain(e.target.value)}
          className="input"
        />
        <button type="submit" className="button">
          Add Domain
        </button>
        {message && (
          <div className="message" style={{ color: messageColor }}>
            {message}
          </div>
        )}
      </form>
    </div>
  );
};
