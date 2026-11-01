export default function SkillBadge({ skill, variant = "matched" }) {
  const name = typeof skill === "string" ? skill : skill.name;
  const extra = typeof skill === "object" && skill.priority ? ` · ${skill.priority}` : "";
  return <span className={`badge ${variant}`}>{name}{extra}</span>;
}
