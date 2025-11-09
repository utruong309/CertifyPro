import { useState } from "react";
import API from "../api";
import { Certification } from "../types";

export default function CertificationForm({ onRefresh }: { onRefresh: () => void }) {
  const [cert, setCert] = useState<Certification>({
    type: "",
    number: "",
    issue_date: "",
    expiry_date: "",
    state: "",
    user_id: 0,
  });
  const [file, setFile] = useState<File | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setCert({ ...cert, [e.target.name]: e.target.value });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await API.post("/certifications/", cert);
      if (file) {
        const formData = new FormData();
        formData.append("file", file);
        await API.post(`/certifications/${res.data.id}/upload`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      }
      alert("Certification added successfully!");
      setCert({
        type: "",
        number: "",
        issue_date: "",
        expiry_date: "",
        state: "",
        user_id: 0,
      });
      setFile(null);
      onRefresh();
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (err) {
      alert("Error creating certification");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-box">
      <h3>Add Certification</h3>
      <input name="type" placeholder="Type (CPA, EA, etc.)" onChange={handleChange} required />
      <input name="number" placeholder="Number" onChange={handleChange} required />
      <input name="issue_date" type="date" onChange={handleChange} required />
      <input name="expiry_date" type="date" onChange={handleChange} required />
      <input name="state" placeholder="State" onChange={handleChange} required />
      <input name="user_id" type="number" placeholder="User ID" onChange={handleChange} required />
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
      <button type="submit">Add Certification</button>
    </form>
  );
}