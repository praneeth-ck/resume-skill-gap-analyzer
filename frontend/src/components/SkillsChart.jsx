import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Tooltip,
} from "chart.js";
import { Bar, Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function SkillsChart({ matched = [], missing = [], additional = [], categories = {} }) {
  const doughnutData = {
    labels: ["Matching", "Missing"],
    datasets: [
      {
        data: [matched.length, missing.length],
        backgroundColor: ["#3b6cff", "#d64545"],
        borderWidth: 0,
      },
    ],
  };

  const barData = {
    labels: ["Matching", "Missing", "Additional"],
    datasets: [
      {
        label: "Skills",
        data: [matched.length, missing.length, additional.length],
        backgroundColor: ["#3b6cff", "#d64545", "#1f9d6a"],
      },
    ],
  };

  const categoryLabels = Object.keys(categories);
  const categoryData = {
    labels: categoryLabels,
    datasets: [
      {
        label: "Matching",
        data: categoryLabels.map((key) => categories[key].matched || 0),
        backgroundColor: "#3b6cff",
      },
      {
        label: "Missing",
        data: categoryLabels.map((key) => categories[key].missing || 0),
        backgroundColor: "#d64545",
      },
      {
        label: "Additional",
        data: categoryLabels.map((key) => categories[key].additional || 0),
        backgroundColor: "#1f9d6a",
      },
    ],
  };

  return (
    <div className="grid grid-2">
      <div className="card">
        <h3>Matching vs missing</h3>
        <Doughnut data={doughnutData} />
      </div>
      <div className="card">
        <h3>Skill comparison</h3>
        <Bar data={barData} options={{ responsive: true, plugins: { legend: { display: false } } }} />
      </div>
      <div className="card" style={{ gridColumn: "1 / -1" }}>
        <h3>Category breakdown</h3>
        {categoryLabels.length === 0 ? (
          <p className="muted">No categorized skills yet.</p>
        ) : (
          <Bar data={categoryData} options={{ responsive: true, scales: { x: { stacked: true }, y: { stacked: true } } }} />
        )}
      </div>
    </div>
  );
}
