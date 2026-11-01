import { useState } from "react";

export default function FileUpload({ onFile, progress, disabled }) {
  const [dragOver, setDragOver] = useState(false);

  const handleFiles = (files) => {
    const file = files?.[0];
    if (file) onFile(file);
  };

  return (
    <div
      className="dropzone"
      onDragOver={(event) => {
        event.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={() => setDragOver(false)}
      onDrop={(event) => {
        event.preventDefault();
        setDragOver(false);
        handleFiles(event.dataTransfer.files);
      }}
      style={{ outline: dragOver ? "2px solid #3b6cff" : "none" }}
    >
      <h3>Drop a PDF or DOCX resume</h3>
      <p className="muted">Maximum size 5 MB. Files stay private to your account.</p>
      <input
        type="file"
        accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        disabled={disabled}
        onChange={(event) => handleFiles(event.target.files)}
      />
      {progress > 0 && progress < 100 ? (
        <div className="progress" style={{ marginTop: 16 }}>
          <span style={{ width: `${progress}%` }} />
        </div>
      ) : null}
    </div>
  );
}
