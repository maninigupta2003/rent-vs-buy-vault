// Soft close modal
export default function PreApprovalModal({ open, onClose }) {
    if (!open) return null;
  
    return (
      <div
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: "rgba(0,0,0,0.4)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 1000,
        }}
      >
        <div
          style={{
            background: "#fff",
            padding: "24px",
            borderRadius: "8px",
            width: "360px",
          }}
        >
          <h3> Pre-Approval</h3>
  
          <p style={{ marginTop: "10px" }}>
            Based on your financial profile, you are eligible for a home loan.
          </p>
  
          <p style={{ marginTop: "10px" }}>
            Would you like us to generate your pre-approval certificate?
          </p>
  
          <button
            onClick={onClose}
            style={{ marginTop: "16px", padding: "8px 12px" }}
          >
            Submit Details
          </button>
        </div>
      </div>
    );
  }
  