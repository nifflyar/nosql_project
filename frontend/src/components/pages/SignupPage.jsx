import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
export


function SignupPage() {
  const { register, setErr, err } = useAuth();
  const nav = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("Astana, KZ");
  const [password, setPassword] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      setErr("");
      await register({
        name,
        email,
        password,
        address,
        role: "customer",
      });
      nav("/shop");
    } catch (e2) {
      setErr(e2?.response?.data?.detail || "Failed to register");
    }
  };

  return (
    <div className="authwrap">
      <div className="container">
        <div className="card">
          <h2>Signup</h2>
          <p>Create an account and start shopping.</p>

          {err ? <div className="error">{err}</div> : null}

          <form className="form" onSubmit={submit}>
            <div className="field">
              <div className="label">Name</div>
              <input className="input" value={name} onChange={(e) => setName(e.target.value)} placeholder="Monika" />
            </div>

            <div className="field">
              <div className="label">Email</div>
              <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="user123@example.com" />
            </div>

            <div className="field">
              <div className="label">Address</div>
              <input className="input" value={address} onChange={(e) => setAddress(e.target.value)} placeholder="City, street..." />
            </div>

            <div className="field">
              <div className="label">Password</div>
              <input className="input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
            </div>

            <button className="btn" type="submit">
              Create account
            </button>

            <div style={{ marginTop: 10, color: "#666" }}>
              Already have an account? <Link to="/login" style={{ textDecoration: "underline" }}>Login</Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}