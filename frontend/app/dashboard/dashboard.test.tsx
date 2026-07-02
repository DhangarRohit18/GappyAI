import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import DashboardPage from './page';

// Mock components or dependencies as needed
jest.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }: any) => <div {...props}>{children}</div>,
    button: ({ children, ...props }: any) => <button {...props}>{children}</button>,
  },
  AnimatePresence: ({ children }: any) => <>{children}</>,
}));

describe('Dashboard Page Component Tests', () => {
  it('renders all metrics card', () => {
    render(<DashboardPage />);
    expect(screen.getByText('Active Goals')).toBeInTheDocument();
    expect(screen.getByText('Tasks Automated')).toBeInTheDocument();
    expect(screen.getByText('Hours Saved')).toBeInTheDocument();
  });

  it('allows input to be changed and processes goal launch', () => {
    render(<DashboardPage />);
    const input = screen.getByPlaceholderText(/Launch/i);
    fireEvent.change(input, { target: { value: 'Launch production next month' } });
    expect(input.value).toBe('Launch production next month');

    const launchBtn = screen.getByRole('button', { name: /Launch/i });
    fireEvent.click(launchBtn);
    
    // UI enters processing state
    expect(screen.getByText(/Processing.../i)).toBeInTheDocument();
  });
});
