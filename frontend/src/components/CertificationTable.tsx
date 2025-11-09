import { Certification } from "../types";

const API = "http://127.0.0.1:8000";

export default function CertificationTable({ certs }: { certs: Certification[] }) {
  return (
    <div className="table-wrapper">
      <h3>All Certifications</h3>
      <table className="data-table">
        <thead>
          <tr>
            <th>User ID</th>
            <th>Type</th>
            <th>State</th>
            <th>Expiry</th>
            <th>Status</th>
            <th>Document</th>
          </tr>
        </thead>
        <tbody>
          {certs.map((c) => (
            <tr key={c.id}>
              <td>{c.user_id}</td>
              <td>{c.type}</td>
              <td>{c.state}</td>
              <td>{c.expiry_date}</td>
              <td>
                <span
                  className={`tag ${
                    c.status === "Active"
                      ? "active"
                      : c.status === "Expiring Soon"
                      ? "soon"
                      : "expired"
                  }`}
                >
                  {c.status}
                </span>
              </td>
              <td>
                {c.document_path ? (
                  <a href={`${API}/${c.document_path}`} target="_blank" rel="noreferrer">
                    View
                  </a>
                ) : (
                  "—"
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}