import { useEffect, useState } from "react";
import api, { getErrorMessage } from "../api/client.js";
import ErrorMessage from "../components/ErrorMessage.jsx";
import ScoreCard from "../components/ScoreCard.jsx";
import SkillList from "../components/SkillList.jsx";

export default function ComparePage() {
  const [items, setItems] = useState([]);
  const [leftId, setLeftId] = useState("");
  const [rightId, setRightId] = useState("");
  const [left, setLeft] = useState(null);
  const [right, setRight] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/api/analyses").then((response) => setItems(response.data.items)).catch((err) => setError(getErrorMessage(err)));
  }, []);

  const loadPair = async () => {
    setError("");
    try {
      const [a, b] = await Promise.all([
        api.get(`/api/analyses/${leftId}`),
        api.get(`/api/analyses/${rightId}`),
      ]);
      setLeft(a.data);
      setRight(b.data);
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  return (
    <div>
      <h1>Compare analyses</h1>
      <ErrorMessage message={error} />
      <div className="card grid grid-2">
        <label className="field">First analysis
          <select value={leftId} onChange={(e) => setLeftId(e.target.value)}>
            <option value="">Select</option>
            {items.map((item) => <option key={item.id} value={item.id}>{item.job_title} · {item.match_score.toFixed(1)}%</option>)}
          </select>
        </label>
        <label className="field">Second analysis
          <select value={rightId} onChange={(e) => setRightId(e.target.value)}>
            <option value="">Select</option>
            {items.map((item) => <option key={item.id} value={item.id}>{item.job_title} · {item.match_score.toFixed(1)}%</option>)}
          </select>
        </label>
        <button className="btn btn-primary" onClick={loadPair} disabled={!leftId || !rightId}>Compare</button>
      </div>
      {left && right ? (
        <div className="grid grid-2" style={{ marginTop: 18 }}>
          {[left, right].map((analysis) => (
            <div key={analysis.id}>
              <h2>{analysis.job_title}</h2>
              <ScoreCard label="Match estimate" value={analysis.match_score} />
              <SkillList title="Matching" skills={analysis.matched_skills} />
              <SkillList title="Missing" skills={analysis.missing_skills} variant="missing" />
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}
