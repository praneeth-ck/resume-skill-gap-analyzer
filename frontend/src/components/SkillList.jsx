import SkillBadge from "./SkillBadge.jsx";

export default function SkillList({ title, skills, variant }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      <p className="muted">{skills.length} detected</p>
      <div>
        {skills.length === 0 ? <p className="muted">None detected.</p> : skills.map((skill) => (
          <SkillBadge key={skill.name || skill} skill={skill} variant={variant} />
        ))}
      </div>
    </div>
  );
}
