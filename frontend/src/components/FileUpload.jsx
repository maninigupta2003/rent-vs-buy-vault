// Drag and drop file upload
import { useState } from "react";
import { uploadFile } from "../services/api";

export default function FileUpload({ onExtracted }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const extracted = await uploadFile(file);
      onExtracted(extracted);
    } catch (err) {
      console.error(err);
      setError("Failed to extract salary data");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "12px" }}>
      <input type="file" accept="image/*,.pdf" onChange={handleUpload} />

      {loading && <p> Extracting salary data…</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
