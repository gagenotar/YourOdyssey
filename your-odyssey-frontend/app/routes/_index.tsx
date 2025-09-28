
import { useState } from "react";
import { useNavigate } from "react-router-dom";
const SLOGAN = "Your Virtual Travel Agent!";




export default function Index() {
  const [location, setLocation] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (location.trim()) {
      // Store location if needed (e.g., localStorage)
      localStorage.setItem("odyssey_location", location);
      navigate(`/plan?destination=${encodeURIComponent(location)}`);
    }
  };

  return (
    <main style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "80vh" }}>
      <h1 style={{ fontSize: "2.5rem", fontWeight: 700, marginBottom: 8, textAlign: "center" }}>
          Your<span>Ω</span>dyssey</h1>
      <p style={{ fontSize: "1.25rem", color: "#666", marginBottom: 32, textAlign: "center" }}>{SLOGAN}</p>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 16, width: "100%", maxWidth: 360 }}>
        <label htmlFor="location" style={{ fontSize: "1.1rem", marginBottom: 8 }}>Where do you want to go?</label>
        <input
          id="location"
          type="text"
          value={location}
          onChange={e => setLocation(e.target.value)}
          placeholder="Enter a destination..."
          style={{ padding: "0.75rem 1rem", fontSize: "1rem", borderRadius: 8, border: "1px solid #ccc", width: "100%" }}
          required
        />
        <button
          type="submit"
          style={{ padding: "0.75rem 1.5rem", fontSize: "1.1rem", borderRadius: 8, background: "#F44250", color: "#fff", border: "none", cursor: "pointer", fontWeight: 600 }}
        >
          Take me there!
        </button>
      </form>
    </main>
  );
}
