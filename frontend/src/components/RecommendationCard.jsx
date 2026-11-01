export default function RecommendationCard({ recommendation }) {
  return (
    <article className="card">
      <h3>{recommendation.skill}</h3>
      <p className="muted">{recommendation.category} · {recommendation.priority} priority</p>
      <p><strong>Why it matters:</strong> {recommendation.why_it_matters}</p>
      <p><strong>What to learn:</strong> {recommendation.what_to_learn}</p>
      <p><strong>Suggested project:</strong> {recommendation.suggested_project}</p>
      <ul>
        {recommendation.next_steps.map((step) => <li key={step}>{step}</li>)}
      </ul>
    </article>
  );
}
