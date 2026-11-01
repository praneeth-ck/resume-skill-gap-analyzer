import { useEffect, useState } from "react";
import api, { getErrorMessage } from "../api/client.js";
import ErrorMessage from "../components/ErrorMessage.jsx";
import SkillBadge from "../components/SkillBadge.jsx";

const empty = { title: "", company: "", description: "" };

export default function JobPage() {
  const [form, setForm] = useState(empty);
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState("");

  const load = () => api.get("/api/jobs").then((response) => setJobs(response.data.items));

  useEffect(() => { load(); }, []);

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      await api.post("/api/jobs", form);
      setForm(empty);
      load();
    } catch (err) {
      setError(getErrorMessage(err, "Could not save this job description."));
    }
  };

  return (
    <div>
      <h1>Job descriptions</h1>
      <ErrorMessage message={error} />
      <form className="card" onSubmit={submit}>
        <label className="field">Job title
          <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required minLength={2} />
        </label>
        <label className="field">Company (optional)
          <input value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} />
        </label>
        <label className="field">Description
          <textarea rows={10} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} required minLength={20} />
        </label>
        <button className="btn btn-primary">Save job</button>
      </form>
      <div className="grid" style={{ marginTop: 18 }}>
        {jobs.map((job) => (
          <article className="card" key={job.id}>
            <h3>{job.title}</h3>
            <p className="muted">{job.company || "No company listed"}</p>
            <p>{job.description.slice(0, 220)}...</p>
            <div>{job.required_skills.map((skill) => <SkillBadge key={skill.name} skill={skill} />)}</div>
            <button className="btn btn-danger" onClick={() => api.delete(`/api/jobs/${job.id}`).then(load)}>Delete</button>
          </article>
        ))}
      </div>
    </div>
  );
}
