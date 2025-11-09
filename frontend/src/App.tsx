import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import Dashboard from "./components/Dashboard";
import UserForm from "./components/UserForm";
import CertificationForm from "./components/CertificationForm";
import CertificationTable from "./components/CertificationTable";
import API from "./api";
import { Certification, Stats } from "./types";

function App() {
  const [certs, setCerts] = useState<Certification[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async (): Promise<void> => {
    setLoading(true);
    try {
      // --- Fetch Certifications ---
      const certRes = await API.get<Certification[]>("/certifications/");
      setCerts(certRes.data);
      console.log("Fetched certifications:", certRes.data);

      // --- Fetch Stats (optional) ---
      try {
        const statsRes = await API.get<Stats>("/certifications/stats", { params: {} });
        setStats(statsRes.data);
        console.log("Fetched stats:", statsRes.data);
      } catch (statsErr: unknown) {
        if (axios.isAxiosError(statsErr)) {
          console.warn(
            "⚠️ Failed to load stats:",
            statsErr.response?.data || statsErr.message
          );
        } else {
          console.warn("⚠️ Unknown error loading stats:", statsErr);
        }
        setStats(null);
      }
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        console.error(
          "API Error fetching data:",
          err.response?.data || err.message
        );
      } else {
        console.error("Unknown error fetching data:", err);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <p className="loading">Loading data...</p>;

  return (
    <div className="container">
      <h1 className="title">CertifyPro Dashboard</h1>

      {/* Dashboard Section */}
      {stats ? (
        <Dashboard stats={stats} />
      ) : (
        <p className="note">Dashboard data unavailable (check /certifications/stats)</p>
      )}

      {/* User + Certification Forms */}
      <div className="form-section">
        <UserForm />
        <CertificationForm onRefresh={fetchData} />
      </div>

      {/* Certification Table */}
      <CertificationTable certs={certs} />
    </div>
  );
}

export default App;