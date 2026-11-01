import { ArrowRight, ScanSearch, ShieldCheck, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";

export default function LandingPage() {
  return (
    <div className="landing">
      <nav className="landing-nav">
        <strong>Resume Skill Gap Analyzer</strong>
        <div style={{ display: "flex", gap: 12 }}>
          <Link className="btn btn-ghost" to="/login">Log in</Link>
          <Link className="btn btn-primary" to="/register">Create account</Link>
        </div>
      </nav>
      <section className="hero" style={{ margin: "0 48px", borderRadius: 28 }}>
        <p className="muted" style={{ color: "#d7e3ff" }}>AI-assisted resume analysis for students and job seekers</p>
        <h1>See how your resume maps to a real job description.</h1>
        <p>Upload a resume, add a posting, and get matching skills, gaps, a transparent match estimate, and learning recommendations.</p>
        <div style={{ display: "flex", gap: 12, marginTop: 24 }}>
          <Link className="btn btn-primary" to="/register">Start analyzing <ArrowRight size={16} /></Link>
          <Link className="btn btn-ghost" to="/login">I already have an account</Link>
        </div>
      </section>
      <section className="features">
        <article className="card"><ScanSearch /> <h3>NLP skill extraction</h3><p className="muted">spaCy PhraseMatcher plus a curated dictionary with aliases such as ReactJS → React.</p></article>
        <article className="card"><Sparkles /> <h3>Transparent scoring</h3><p className="muted">Skill coverage, weighted coverage, and TF-IDF similarity. Not a hiring probability.</p></article>
        <article className="card"><ShieldCheck /> <h3>Private by design</h3><p className="muted">JWT auth, hashed passwords, and resumes that stay limited to your account.</p></article>
      </section>
      <section className="page">
        <h2>How it works</h2>
        <ol>
          <li>Create an account and upload a PDF or DOCX resume.</li>
          <li>Save the job description you care about.</li>
          <li>Run analysis to compare detected skills and review recommendations.</li>
          <li>Revisit history or compare two analyses later.</li>
        </ol>
      </section>
    </div>
  );
}
