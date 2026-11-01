import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import ErrorMessage from "../components/ErrorMessage.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export default function LoginPage() {
  const { login, error } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [localError, setLocalError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async (event) => {
    event.preventDefault();
    if (!form.email.includes("@") || form.password.length < 8) {
      setLocalError("Enter a valid email and a password with at least 8 characters.");
      return;
    }
    setSubmitting(true);
    try {
      await login(form.email, form.password);
      navigate("/app");
    } catch {
      setLocalError("");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-wrap page">
      <form className="card" style={{ maxWidth: 420, margin: "80px auto" }} onSubmit={onSubmit}>
        <h1>Welcome back</h1>
        <p className="muted">Sign in to continue your skill-gap analysis.</p>
        <ErrorMessage message={localError || error} />
        <label className="field">Email
          <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
        </label>
        <label className="field">Password
          <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
        </label>
        <button className="btn btn-primary" disabled={submitting}>{submitting ? "Signing in..." : "Log in"}</button>
        <p>New here? <Link to="/register">Create an account</Link></p>
      </form>
    </div>
  );
}
