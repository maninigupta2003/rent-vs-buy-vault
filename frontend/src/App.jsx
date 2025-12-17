import { useEffect, useState } from "react";
import { analyze } from "./services/api";

import FileUpload from "./components/FileUpload";
import ChatInterface from "./components/ChatInterface";
import PreApprovalModal from "./components/PreApprovalModal";

export default function App() {
  const [backendStatus, setBackendStatus] = useState("Checking backend...");
  const [salaryData, setSalaryData] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [showPreApproval, setShowPreApproval] = useState(false);

  // Backend health check
  useEffect(() => {
    fetch("http://127.0.0.1:5050/health")
      .then((res) => res.json())
      .then(() => setBackendStatus("Backend connected"))
      .catch(() => setBackendStatus("Backend not reachable"));
  }, []);

  // Run deterministic analysis
  const runAnalysis = async () => {
    if (!salaryData) return;

    const result = await analyze({
      monthly_income: salaryData.monthly_income ?? 25000,
      annual_rent: 140000,
    });

    setAnalysis(result);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <h1> Rent vs Buy Vault</h1>
      <p><strong>Status:</strong> {backendStatus}</p>

      {/*  File Upload */}
      <h3>Upload Salary Slip</h3>
      <FileUpload onExtracted={setSalaryData} />

      {salaryData && (
        <>
          <h4>Extracted Salary Data</h4>
          <pre>{JSON.stringify(salaryData, null, 2)}</pre>

          <button onClick={runAnalysis} style={{ marginTop: "10px" }}>
            Run Rent vs Buy Analysis
          </button>
        </>
      )}

      {/*  Deterministic Analysis */}
      {analysis && (
        <>
          <h3>Financial Analysis</h3>
          <pre>{JSON.stringify(analysis, null, 2)}</pre>

          {/*  Chat Persuasion */}
          <ChatInterface analysis={analysis} />

          {/*  Soft Close */}
          <button
            onClick={() => setShowPreApproval(true)}
            style={{ marginTop: "20px" }}
          >
            Check Pre-Approval
          </button>
        </>
      )}

      {/* Pre-Approval Modal */}
      <PreApprovalModal
        open={showPreApproval}
        onClose={() => setShowPreApproval(false)}
      />
    </div>
  );
}
