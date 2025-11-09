import { Stats } from "../types";

export default function Dashboard({ stats }: { stats: Stats }) {
  return (
    <div className="stats-grid">
      <Card label="Total" value={stats.total} color="#555" />
      <Card label="Active" value={stats.active} color="green" />
      <Card label="Expiring Soon" value={stats.expiring_soon} color="orange" />
      <Card label="Expired" value={stats.expired} color="red" />
    </div>
  );
}

function Card({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="card" style={{ borderLeft: `4px solid ${color}` }}>
      <p className="card-label">{label}</p>
      <p className="card-value" style={{ color }}>
        {value}
      </p>
    </div>
  );
}