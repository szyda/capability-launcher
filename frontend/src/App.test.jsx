import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import App from './App';
import { vi } from 'vitest';

const mockCapabilities = [
  {
    id: 'url_inspector',
    name: 'URL Inspector',
    description: 'Inspect a URL',
    version: '1.0.0',
    inputs: [
      {
        name: 'url',
        label: 'URL',
        type: 'text',
        required: true,
        default: 'https://example.com',
      },
    ],
  },
];

vi.mock('./api', () => ({
  fetchCapabilities: vi.fn(),
  runCapability: vi.fn(),
}));

import { fetchCapabilities, runCapability } from './api';

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('loads and renders capabilities from the API', async () => {
    fetchCapabilities.mockResolvedValue(mockCapabilities);

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('URL Inspector')).toBeInTheDocument();
    });

    expect(screen.getByLabelText('URL')).toBeInTheDocument();
  });

  it('runs a capability and shows the result', async () => {
    fetchCapabilities.mockResolvedValue(mockCapabilities);
    runCapability.mockResolvedValue({
      capability_id: 'url_inspector',
      status: 'success',
      result: { parsed_url: 'https://example.com' },
      duration_ms: 12,
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('URL Inspector')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /run capability/i }));

    await waitFor(() => {
      expect(runCapability).toHaveBeenCalledWith('url_inspector', {
        url: 'https://example.com',
      });
    });

    await waitFor(() => {
      expect(screen.getByText('Result')).toBeInTheDocument();
    });
  });

  it('shows an API error when the run request fails', async () => {
    fetchCapabilities.mockResolvedValue(mockCapabilities);
    runCapability.mockRejectedValue(new Error('Request failed'));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('URL Inspector')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /run capability/i }));

    await waitFor(() => {
      expect(screen.getByText('Request failed')).toBeInTheDocument();
    });
  });
});
