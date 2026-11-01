import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import ErrorMessage from "../components/ErrorMessage.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export default function RegisterPage() {
  const { register, error } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [localError, setLocalError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const onSubmit = async (event) => {
    event.preventDefault();
    if (form.name.trim().length < 2 || !form.email.includes("@") || form.password.length < 8) {
      setLocalError("Name, a valid email, and an 8+ character password are required.");
      return;
    }
    setSubmitting(true);
    try {
      await register(form.name, form.email, form.password);
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
        <h1>Create your account</h1>
        <ErrorMessage message={localError || error} />
        <label className="field">Name
          <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        </label>
        <label className="field">Email
          <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
        </label>
        <label className="field">Password
          <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
        </label>
        <button className="btn btn-primary" disabled={submitting}>{submitting ? "Creating..." : "Register"}</button>
        <p>Already have an account? <Link to="/login">Log in</Link></p>
      </form>
    </div>
  );
}
