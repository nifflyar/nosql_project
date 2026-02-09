import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export function LoginPage() {
  const { login } = useAuth();
  const nav = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      setErr("");
      await login(email, password);
      nav("/");
    } catch {
      setErr("Invalid email or password");
    }
  };

  return (
    <div className="authwrap">
      <div className="container">
        <div className="card">
          <h2>Login</h2>
          <p>Sign in to continue shopping.</p>

          {err && <div className="error">{err}</div>}

          <form className="form" onSubmit={submit}>
            <div className="field">
              <div className="label">Email</div>
              <input
                className="input"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="field">
              <div className="label">Password</div>
              <input
                className="input"
                placeholder="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <button className="btn" type="submit">
              Login
            </button>

            <div style={{ marginTop: 10, color: "#666" }}>
              No account?{" "}
              <Link to="/signup" style={{ textDecoration: "underline" }}>
                Sign up
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
