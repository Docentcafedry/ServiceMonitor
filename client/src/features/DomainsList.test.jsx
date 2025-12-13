import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router';
import DomainList from './DomainsList';

// Mock DomainCard
vi.mock('./DomainCard', () => {
  return {
    default: ({ domain }) => <div data-testid="domain-card">{domain}</div>,
  };
});

describe('DomainList Component', () => {
  beforeEach(() => {
    vi.restoreAllMocks(); // reset mocks between tests
  });

  it('displays loading initially', () => {
    render(
      <MemoryRouter>
        <DomainList />
      </MemoryRouter>
    );

    expect(screen.getByText(/Loading domain list/i)).toBeInTheDocument();
  });

  it('renders domains after successful fetch', async () => {
    const mockDomains = [{ domain: 'example.com' }, { domain: 'test.com' }];

    // Mock global fetch
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockDomains),
        })
      )
    );

    render(
      <MemoryRouter>
        <DomainList />
      </MemoryRouter>
    );

    const cards = await screen.findAllByTestId('domain-card');
    expect(cards).toHaveLength(mockDomains.length);
    expect(cards[0]).toHaveTextContent('example.com');
    expect(cards[1]).toHaveTextContent('test.com');
  });

  it('renders error message on fetch failure', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() => Promise.resolve({ ok: false }))
    );

    render(
      <MemoryRouter>
        <DomainList />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(
        screen.getByText(/Error: Failed to fetch domain list/i)
      ).toBeInTheDocument();
    });
  });
});
