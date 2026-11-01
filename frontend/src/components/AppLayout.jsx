import { useState } from "react";
import { Outlet } from "react-router-dom";
import Footer from "./Footer.jsx";
import Navbar from "./Navbar.jsx";
import Sidebar from "./Sidebar.jsx";

export default function AppLayout() {
  const [open, setOpen] = useState(false);
  return (
    <div className="app-shell">
      <Sidebar open={open} onClose={() => setOpen(false)} />
      <div className="content">
        <Navbar onMenu={() => setOpen((value) => !value)} />
        <main className="page">
          <Outlet />
        </main>
        <Footer />
      </div>
    </div>
  );
}
