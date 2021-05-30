import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import Loading from './Loading';

describe('Loading component', () => {
  it('renders a loading spinner before the data is loaded', async () => {
    const loadingFunction = () => {
      return new Promise<void>((resolve, reject) => {
        // never resolved
      });
    };
    const display = <div>data display</div>;

    render(<Loading loadingFunction={loadingFunction}>{display}</Loading>);
    await waitFor(() => {
      expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });
  });

  it('renders the given data display once the data is loaded', async () => {
    const loadingFunction = () => {
      return new Promise<void>((resolve, reject) => {
        resolve();
      });
    };
    const display = <div>data display</div>;

    render(<Loading loadingFunction={loadingFunction}>{display}</Loading>);
    await waitFor(() => {
      expect(screen.getByText(/data display/i)).toBeInTheDocument();
    });
  });

  it('renders an error if there is a problem loading the data', async () => {
    const loadingFunction = () => {
      return new Promise<string>((resolve, reject) => {
        reject('error message');
      });
    };
    const display = <div>data display</div>;

    render(<Loading loadingFunction={loadingFunction}>{display}</Loading>);
    await waitFor(() => {
      expect(screen.getByText(/error message/i)).toBeInTheDocument();
    });
  });

  it('only calls the loading function once', async () => {
    const loadingFunction = jest.fn(() => {
      return new Promise<void>((resolve, reject) => {
        resolve();
      });
    });
    const display = <div>data display</div>;

    render(<Loading loadingFunction={loadingFunction}>{display}</Loading>);
    await waitFor(() => {
      expect(loadingFunction).toHaveBeenCalledTimes(1);
    });
  });

  it('only calls the loading function once even after error', async () => {
    const loadingFunction = jest.fn(() => {
      return new Promise<void>((resolve, reject) => {
        reject('error message');
      });
    });
    const display = <div>data display</div>;

    render(<Loading loadingFunction={loadingFunction}>{display}</Loading>);
    await waitFor(() => {
      expect(loadingFunction).toHaveBeenCalledTimes(1);
    });
  });
});
