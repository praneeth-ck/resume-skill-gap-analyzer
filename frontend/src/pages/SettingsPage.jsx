import { useAuth } from "../context/AuthContext.jsx";

export default function SettingsPage() {
  const { user, logout } = useAuth();
  return (
    <div>
      <h1>Profile and settings</h1>
      <div className="card">
        <p><strong>Name:</strong> {user.name}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Member since:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
        <p className="muted">Passwords are hashed with Argon2. Resume files are stored privately on the server and are never publicly linked.</p>
        <button className="btn btn-dark" onClick={logout}>Log out</button>
      </div>
    </div>
  );
}
