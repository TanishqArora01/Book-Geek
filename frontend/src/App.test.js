import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import App from './App';

// Mock child components to focus on App logic
vi.mock('./components/Background', () => ({
    default: () => <div data-testid="background" />
}));

vi.mock('./components/BookCard', () => ({
    default: ({ book }) => <div data-testid="book-card">{book.title}</div>
}));

describe('App', () => {
    it('renders basic structure', () => {
        render(<App />);

        expect(screen.getByTestId('background')).toBeInTheDocument();
        expect(screen.getByRole('heading', { name: /BookGeek-AI/i })).toBeInTheDocument();
    });
});
