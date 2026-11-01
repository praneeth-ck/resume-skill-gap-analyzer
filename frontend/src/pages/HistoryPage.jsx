import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import api, { getErrorMessage } from "../api/client.js";
import ErrorMessage from "../components/ErrorMessage.jsx";

export default function HistoryPage() {
  const [items, setItems] = useState([]);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");

  const load = () => {
    api.get("/api/analyses").then((response) => setItems(response.data.items)).catch((err) => setError(getErrorMessage(err)));
  };

  useEffect(() => { load(); }, []);

  const filtered = useMemo(() => {
    const needle = query.toLowerCase();
    return items.filter((item) =>
      `${item.resume_filename} ${item.job_title}`.toLowerCase().includes(needle)
    );
  }, [items, query]);

  const remove = async (id) => {
    await api.delete(`/api/analyses/${id}`);
    load();
  };

  return (
    <div>
      <h1>Analysis history</h1>
      <ErrorMessage message={error} />
      <input className="field" placeholder="Search by resume or job title" value={query} onChange={(e) => setQuery(e.target.value)} />
      <table className="table">
        <thead>
          <tr>
            <th>Resume</th>
            <th>Job title</th>
            <th>Match estimate</th>
            <th>Date</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((item) => (
            <tr key={item.id}>
              <td>{item.resume_filename}</td>
              <td>{item.job_title}</td>
              <td>{item.match_score.toFixed(1)}%</td>
              <td>{new Date(item.created_at).toLocaleString()}</td>
              <td>
                <Link to={`/app/analyses/${item.id}`}>View</Link>
                {" · "}
                <button className="btn btn-danger" onClick={() => remove(item.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
