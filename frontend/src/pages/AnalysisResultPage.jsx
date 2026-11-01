import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api, { getErrorMessage } from "../api/client.js";
import ErrorMessage from "../components/ErrorMessage.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import RecommendationCard from "../components/RecommendationCard.jsx";
import ScoreCard from "../components/ScoreCard.jsx";
import SkillList from "../components/SkillList.jsx";
import SkillsChart from "../components/SkillsChart.jsx";

export default function AnalysisResultPage() {
  const { analysisId } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get(`/api/analyses/${analysisId}`)
      .then((response) => setAnalysis(response.data))
      .catch((err) => setError(getErrorMessage(err)));
  }, [analysisId]);

  if (!analysis && !error) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      <h1>Analysis results</h1>
      <p className="muted">{analysis.resume_filename} · {analysis.job_title} {analysis.job_company ? `at ${analysis.job_company}` : ""}</p>
      <p className="muted">This match estimate is not a probability of getting hired. Missing skills were not detected in the resume; they may still exist.</p>
      <div className="grid grid-3" style={{ margin: "18px 0" }}>
        <ScoreCard label="Overall match estimate" value={analysis.match_score} hint="70% weighted coverage + 30% text similarity" />
        <ScoreCard label="Skill coverage" value={analysis.skill_coverage} />
        <ScoreCard label="Weighted skill coverage" value={analysis.weighted_skill_coverage} />
      </div>
      <ScoreCard label="Text similarity (TF-IDF cosine)" value={analysis.text_similarity} />
      {analysis.score_notes?.map((note) => <p key={note} className="muted">{note}</p>)}
      <div style={{ margin: "18px 0" }}>
        <SkillsChart
          matched={analysis.matched_skills}
          missing={analysis.missing_skills}
          additional={analysis.additional_skills}
          categories={analysis.category_breakdown}
        />
      </div>
      <div className="grid grid-3">
        <SkillList title="Matching skills" skills={analysis.matched_skills} variant="matched" />
        <SkillList title="Missing skills" skills={analysis.missing_skills} variant="missing" />
        <SkillList title="Additional skills" skills={analysis.additional_skills} variant="additional" />
      </div>
      <h2>Recommendations</h2>
      <div className="grid">
        {analysis.recommendations.map((item) => <RecommendationCard key={item.skill} recommendation={item} />)}
      </div>
    </div>
  );
}
