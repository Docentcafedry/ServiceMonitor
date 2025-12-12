import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AddDomainForm from "./AddDomainForm";
import { MemoryRouter } from "react-router";

// Mock useNavigate only
const mockedNavigate = vi.fn();

vi.mock("react-router", async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual, // keep all other exports like MemoryRouter
    useNavigate: () => mockedNavigate, // override only useNavigate
  };
});

// Mock global fetch
global.fetch = vi.fn();

describe("AddDomainForm", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // Test 1: Render input and button
  it("renders input and button", () => {
    render(
      <MemoryRouter>
        <AddDomainForm />
      </MemoryRouter>
    );

    // Check for input field
    expect(screen.getByPlaceholderText("Enter URL http://example.com")).toBeInTheDocument();

    // Check for submit button specifically
    expect(screen.getByRole("button", { name: "Add Domain" })).toBeInTheDocument();
  });

  // Test 2: Show error when input is empty
  it("shows error when input is empty", async () => {
    render(
      <MemoryRouter>
        <AddDomainForm />
      </MemoryRouter>
    );

    // Click the submit button
    userEvent.click(screen.getByRole("button", { name: "Add Domain" }));

    // Expect error message to appear
    expect(await screen.findByText("Please enter a domain.")).toBeInTheDocument();
  });

  // Test 3: Successful form submission
  it("submits form successfully", async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({ message: "Domain added successfully!" }),
  });

  render(
    <MemoryRouter>
      <AddDomainForm />
    </MemoryRouter>
  );

  // Enter domain
  const input = screen.getByPlaceholderText("Enter URL http://example.com");
  await userEvent.type(input, "http://example.com"); // ✅ await

  // Click submit button
  await userEvent.click(screen.getByRole("button", { name: "Add Domain" })); // ✅ await

  // Wait for fetch to be called
  await waitFor(() => {
    expect(fetch).toHaveBeenCalledWith(
      "http://localhost/api/add_domain",
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ domain: "http://example.com" }),
      })
    );

    // Navigation should happen
    expect(mockedNavigate).toHaveBeenCalledWith("/");
  });
});

  // Test 4: API error response
  it("shows error message on failed submit", async () => {
  // Mock a failed API response
  fetch.mockResolvedValueOnce({
    ok: false,
    json: async () => ({ detail: "Domain already exists" }),
  });

  render(
    <MemoryRouter>
      <AddDomainForm />
    </MemoryRouter>
  );

  const input = screen.getByPlaceholderText("Enter URL http://example.com");
  await userEvent.type(input, "http://example.com"); // ✅ input must be typed

  const button = screen.getByRole("button", { name: "Add Domain" });
  await userEvent.click(button); // ✅ click submit

  // Wait for error message
  expect(await screen.findByText("Domain already exists")).toBeInTheDocument();
});

  // Test 5: Network failure
  it("shows error message on network failure", async () => {
    fetch.mockRejectedValueOnce(new Error("Network error"));

    render(
        <MemoryRouter>
        <AddDomainForm />
        </MemoryRouter>
    );

    const input = screen.getByPlaceholderText("Enter URL http://example.com");
    await userEvent.type(input, "http://example.com");

    const button = screen.getByRole("button", { name: "Add Domain" });
    await userEvent.click(button);

    expect(await screen.findByText("Failed to connect to server.")).toBeInTheDocument();
});
});
