import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api, { getErrorMessage } from "../api/client.js";
import ErrorMessage from "../components/ErrorMessage.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import ScoreCard from "../components/ScoreCard.jsx";

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/api/analyses/dashboard")
      .then((response) => setStats(response.data))
      .catch((err) => setError(getErrorMessage(err)));
  }, []);

  if (!stats && !error) return <LoadingSpinner />;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1>Dashboard</h1>
          <p className="muted">Your resumes, saved jobs, and recent match estimates.</p>
        </div>
        <Link className="btn btn-primary" to="/app/analyze">Start new analysis</Link>
      </div>
      <ErrorMessage message={error} />
      {stats ? (
        <>
          <div className="grid grid-3" style={{ marginTop: 20 }}>
            <div className="stat"><p className="muted">Resumes</p><h2>{stats.resume_count}</h2></div>
            <div className="stat"><p className="muted">Job descriptions</p><h2>{stats.job_count}</h2></div>
            <ScoreCard label="Average match estimate" value={stats.average_match_score} hint={`${stats.analysis_count} analyses`} />
          </div>
          <div className="card" style={{ marginTop: 20 }}>
            <h3>Recent analyses</h3>
            {stats.latest_analyses.length === 0 ? <p className="muted">No analyses yet.</p> : (
              <table className="table">
                <thead><tr><th>Resume</th><th>Job</th><th>Score</th><th></th></tr></thead>
                <tbody>
                  {stats.latest_analyses.map((item) => (
                    <tr key={item.id}>
                      <td>{item.resume_filename}</td>
                      <td>{item.job_title}</td>
                      <td>{item.match_score.toFixed(1)}%</td>
                      <td><Link to={`/app/analyses/${item.id}`}>View</Link></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      ) : null}
    </div>
  );
}
