import { useEffect, useState } from "react";
import api, { getErrorMessage } from "../api/client.js";
import ErrorMessage from "../components/ErrorMessage.jsx";
import FileUpload from "../components/FileUpload.jsx";

export default function ResumeUploadPage() {
  const [resumes, setResumes] = useState([]);
  const [current, setCurrent] = useState(null);
  const [error, setError] = useState("");
  const [progress, setProgress] = useState(0);

  const load = () => {
    api.get("/api/resumes").then((response) => setResumes(response.data.items)).catch((err) => setError(getErrorMessage(err)));
  };

  useEffect(() => { load(); }, []);

  const onFile = async (file) => {
    setError("");
    const form = new FormData();
    form.append("file", file);
    try {
      const response = await api.post("/api/resumes/upload", form, {
        onUploadProgress: (event) => setProgress(Math.round((event.loaded / (event.total || file.size)) * 100)),
      });
      setCurrent(response.data);
      setProgress(100);
      load();
    } catch (err) {
      setError(getErrorMessage(err, "Upload failed."));
      setProgress(0);
    }
  };

  const remove = async (id) => {
    await api.delete(`/api/resumes/${id}`);
    if (current?.id === id) setCurrent(null);
    load();
  };

  return (
    <div>
      <h1>Resume upload</h1>
      <ErrorMessage message={error} />
      <FileUpload onFile={onFile} progress={progress} />
      {current ? (
        <div className="card" style={{ marginTop: 18 }}>
          <h3>Extracted text · {current.filename}</h3>
          <pre className="preview">{current.extracted_text}</pre>
        </div>
      ) : null}
      <div className="card" style={{ marginTop: 18 }}>
        <h3>Your resumes</h3>
        {resumes.map((resume) => (
          <div key={resume.id} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0" }}>
            <div>
              <strong>{resume.filename}</strong>
              <p className="muted">{resume.text_preview}</p>
            </div>
            <button className="btn btn-danger" onClick={() => remove(resume.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}
