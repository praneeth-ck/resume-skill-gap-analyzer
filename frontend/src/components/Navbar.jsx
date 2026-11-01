import { Menu } from "lucide-react";
import { useAuth } from "../context/AuthContext.jsx";

export default function Navbar({ onMenu }) {
  const { user } = useAuth();
  return (
    <header className="navbar">
      <button className="btn btn-dark mobile-toggle" onClick={onMenu} aria-label="Open menu">
        <Menu size={18} />
      </button>
      <strong>Workspace</strong>
      <span className="muted">{user?.name}</span>
    </header>
  );
}
