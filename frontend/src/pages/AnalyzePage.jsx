import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api, { getErrorMessage } from "../api/client.js";
import ErrorMessage from "../components/ErrorMessage.jsx";

export default function AnalyzePage() {
  const [resumes, setResumes] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [resumeId, setResumeId] = useState("");
  const [jobId, setJobId] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([api.get("/api/resumes"), api.get("/api/jobs")])
      .then(([resumeRes, jobRes]) => {
        setResumes(resumeRes.data.items);
        setJobs(jobRes.data.items);
      })
      .catch((err) => setError(getErrorMessage(err)));
  }, []);

  const submit = async (event) => {
    event.preventDefault();
    setBusy(true);
    try {
      const response = await api.post("/api/analyses", { resume_id: Number(resumeId), job_id: Number(jobId) });
      navigate(`/app/analyses/${response.data.id}`);
    } catch (err) {
      setError(getErrorMessage(err, "Analysis failed."));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div>
      <h1>New analysis</h1>
      <ErrorMessage message={error} />
      <form className="card" onSubmit={submit}>
        <label className="field">Resume
          <select value={resumeId} onChange={(e) => setResumeId(e.target.value)} required>
            <option value="">Select a resume</option>
            {resumes.map((resume) => <option key={resume.id} value={resume.id}>{resume.filename}</option>)}
          </select>
        </label>
        <label className="field">Job description
          <select value={jobId} onChange={(e) => setJobId(e.target.value)} required>
            <option value="">Select a job</option>
            {jobs.map((job) => <option key={job.id} value={job.id}>{job.title}</option>)}
          </select>
        </label>
        <button className="btn btn-primary" disabled={busy}>{busy ? "Analyzing..." : "Run analysis"}</button>
      </form>
    </div>
  );
}
