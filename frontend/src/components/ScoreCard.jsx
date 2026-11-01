export default function ScoreCard({ label, value, hint }) {
  const display = value == null ? "—" : `${Number(value).toFixed(1)}%`;
  return (
    <div className="stat">
      <p className="muted">{label}</p>
      <h2>{display}</h2>
      {hint ? <p className="muted">{hint}</p> : null}
    </div>
  );
}
