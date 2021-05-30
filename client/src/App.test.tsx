import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders text', () => {
  render(<App />);
  const hello = screen.getByText(/Easy Freezey/i);
  expect(hello).toBeInTheDocument();
});
