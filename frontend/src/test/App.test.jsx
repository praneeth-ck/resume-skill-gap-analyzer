import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import LandingPage from "../pages/LandingPage.jsx";
import ScoreCard from "../components/ScoreCard.jsx";

describe("frontend surfaces", () => {
  it("renders landing call to action", () => {
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Resume Skill Gap Analyzer/i)).toBeInTheDocument();
    expect(screen.getByText(/Start analyzing/i)).toBeInTheDocument();
  });

  it("renders live score values rather than placeholders", () => {
    render(<ScoreCard label="Skill coverage" value={72.5} />);
    expect(screen.getByText("72.5%")).toBeInTheDocument();
  });
});
