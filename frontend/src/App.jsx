import { Navigate, Route, Routes } from "react-router-dom";
import AppLayout from "./components/AppLayout.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import AnalysisResultPage from "./pages/AnalysisResultPage.jsx";
import AnalyzePage from "./pages/AnalyzePage.jsx";
import ComparePage from "./pages/ComparePage.jsx";
import DashboardPage from "./pages/DashboardPage.jsx";
import HistoryPage from "./pages/HistoryPage.jsx";
import JobPage from "./pages/JobPage.jsx";
import LandingPage from "./pages/LandingPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";
import ResumeUploadPage from "./pages/ResumeUploadPage.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/app"
        element={(
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        )}
      >
        <Route index element={<DashboardPage />} />
        <Route path="resumes" element={<ResumeUploadPage />} />
        <Route path="jobs" element={<JobPage />} />
        <Route path="analyze" element={<AnalyzePage />} />
        <Route path="analyses/:analysisId" element={<AnalysisResultPage />} />
        <Route path="history" element={<HistoryPage />} />
        <Route path="compare" element={<ComparePage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
