import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import DomainCard from "./DomainCard";

describe("DomainCard", () => {
  
  // -------------------------------------------------------
  // Test 1: Basic rendering of domain text and correct link
  // -------------------------------------------------------
  test("renders domain text and link", () => {
    // MemoryRouter is required because DomainCard uses <Link>
    render(
      <MemoryRouter>
        <DomainCard domain="example.com" />
      </MemoryRouter>
    );

    // Get the link element containing the domain text
    const link = screen.getByText("example.com");

    // Verify it's in the document
    expect(link).toBeInTheDocument();

    // Verify the link points to the correct URL
    expect(link.getAttribute("href")).toBe("/domains/example.com");
  });

  // -------------------------------------------------------
  // Test 2: Uses default status ("online") and default note
  // -------------------------------------------------------
  test("renders the default status and note", () => {
    render(
      <MemoryRouter>
        <DomainCard domain="test.com" />
      </MemoryRouter>
    );

    // The component renders <span class="status-dot online">
    // There is no accessible role, so we must query the DOM directly
    const statusDot = document.querySelector(".status-dot.online");

    expect(statusDot).not.toBeNull(); // Ensure it exists

    // Default note is "in database"
    expect(screen.getByText("in database")).toBeInTheDocument();
  });

  // -------------------------------------------------------
  // Test 3: Renders custom status and custom note
  // -------------------------------------------------------
  test("renders custom status and note", () => {
    render(
      <MemoryRouter>
        <DomainCard 
          domain="abc.com"
          status="offline"
          note="not found"
        />
      </MemoryRouter>
    );

    // Custom status applies the class: .status-dot.offline
    const statusDot = document.querySelector(".status-dot.offline");
    expect(statusDot).not.toBeNull();

    // Custom note should appear
    expect(screen.getByText("not found")).toBeInTheDocument();
  });

  // -------------------------------------------------------
  // Test 4: Note should not render if it's an empty string
  // -------------------------------------------------------
  test("hides note when note prop is empty", () => {
    render(
      <MemoryRouter>
        <DomainCard domain="no-note.com" note="" />
      </MemoryRouter>
    );

    // Query for the default note (or any note) — should NOT exist
    const note = screen.queryByText("in database");

    // queryBy returns null when not found, which is correct here
    expect(note).toBeNull();
  });
});
