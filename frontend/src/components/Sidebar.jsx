import { FileText, History, Home, LogOut, Settings, Sparkles, Upload, Briefcase } from "lucide-react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

const links = [
  { to: "/app", label: "Dashboard", icon: Home, end: true },
  { to: "/app/resumes", label: "Resumes", icon: Upload },
  { to: "/app/jobs", label: "Job descriptions", icon: Briefcase },
  { to: "/app/history", label: "History", icon: History },
  { to: "/app/compare", label: "Compare", icon: FileText },
  { to: "/app/settings", label: "Settings", icon: Settings },
];

export default function Sidebar({ open, onClose }) {
  const { logout } = useAuth();
  return (
    <aside className={`sidebar ${open ? "open" : ""}`}>
      <div className="brand">
        <div className="brand-mark"><Sparkles size={18} /></div>
        <div>
          <div>Skill Gap Analyzer</div>
          <small className="muted">Resume intelligence</small>
        </div>
      </div>
      <nav>
        {links.map((link) => (
          <NavLink key={link.to} to={link.to} end={link.end} className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`} onClick={onClose}>
            <link.icon size={18} />
            {link.label}
          </NavLink>
        ))}
      </nav>
      <button className="btn btn-ghost" onClick={logout}>
        <LogOut size={16} /> Logout
      </button>
    </aside>
  );
}
