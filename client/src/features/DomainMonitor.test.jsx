// DomainMonitor.test.jsx
import { render, screen, waitFor } from '@testing-library/react';
import DomainMonitor from './DomainMonitor';
import { MemoryRouter, Route, Routes } from 'react-router';
import { vi } from 'vitest';

// ----------------------
// Mock fetch globally
// ----------------------
global.fetch = vi.fn();

// Mock API response with domain_id field
const mockData = {
  examinations: [
    {
      domain_id: 1,
      status_code: 200,
      response_time: "PT0.123S",
      examination_time: new Date().toISOString(),
    },
    {
      domain_id: 1,
      status_code: 200,
      response_time: "PT0.456S",
      examination_time: new Date(Date.now() - 1000 * 60 * 60).toISOString(), // 1 hour ago
    },
  ],
};

describe('DomainMonitor', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('shows loading initially', () => {
    render(
      <MemoryRouter initialEntries={['/domain/example.com']}>
        <Routes>
          <Route path="/domain/:domainName" element={<DomainMonitor />} />
        </Routes>
      </MemoryRouter>
    );

    // Loading indicator should appear initially
    expect(screen.getByText(/Loading/i)).toBeInTheDocument();
  });

  it('renders domain data after fetch', async () => {
    // Mock fetch to resolve with sample data
    fetch.mockResolvedValueOnce({
      json: async () => mockData,
    });

    render(
      <MemoryRouter initialEntries={['/domain/example.com']}>
        <Routes>
          <Route path="/domain/:domainName" element={<DomainMonitor />} />
        </Routes>
      </MemoryRouter>
    );

    // Wait for fetch to complete
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));

    // -------- Assertions --------

    // Status code
    const statusDiv = screen.getByText(/Статус код:/i).parentElement;
    expect(statusDiv).toHaveTextContent('Статус код: 200');

    // Response time (converted to ms)
    const responseDiv = screen.getByText(/Время ответа:/i).parentElement;
    expect(responseDiv).toHaveTextContent('Время ответа: 456.000 ms');

    // Uptime (24h)
    const uptimeDiv = screen.getByText(/Аптайм/i).parentElement;
    expect(uptimeDiv).toHaveTextContent(/Аптайм.*\d+(\.\d+)?%/);

    // Last checked
    const lastCheckedDiv = screen.getByText(/Последняя проверка/i).parentElement;
    expect(lastCheckedDiv.textContent).not.toBe('Последняя проверка: N/A');

    // History items colors
    const items = screen.getAllByRole('dot'); // history-item divs
    expect(items.length).toBe(mockData.examinations.length);
    expect(items[0].className).toContain('green'); // status_code 200
    expect(items[1].className).toContain('green');   // status_code 200
  });

  it('handles empty data', async () => {
    // Mock fetch returning empty examinations
    fetch.mockResolvedValueOnce({
      json: async () => ({ examinations: [] }),
    });

    render(
      <MemoryRouter initialEntries={['/domain/example.com']}>
        <Routes>
          <Route path="/domain/:domainName" element={<DomainMonitor />} />
        </Routes>
      </MemoryRouter>
    );

    // Wait for fetch to complete
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));

    // -------- Assertions --------

    // Status code fallback
    const statusDiv = screen.getByText(/Статус код:/i).parentElement;
    expect(statusDiv).toHaveTextContent('Статус код: N/A');

    // Response time fallback
    const responseDiv = screen.getByText(/Время ответа:/i).parentElement;
    expect(responseDiv).toHaveTextContent('Время ответа: N/A ms');

    // Uptime fallback
    const uptimeDiv = screen.getByText(/Аптайм/i).parentElement;
    expect(uptimeDiv).toHaveTextContent('Аптайм (24ч): N/A%');

    // Last checked fallback
    const lastCheckedDiv = screen.getByText(/Последняя проверка/i).parentElement;
    expect(lastCheckedDiv).toHaveTextContent('Последняя проверка: N/A');
  });
});
