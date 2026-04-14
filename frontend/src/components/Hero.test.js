import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Hero from './Hero';

describe('Hero', () => {
    beforeEach(() => {
        global.fetch = vi.fn(() =>
            Promise.resolve({
                json: () => Promise.resolve([]),
            })
        );
    });

    it('renders hero title and search items', () => {
        render(<Hero />);

        expect(screen.getByText(/BookGeek-AI/i)).toBeInTheDocument();
        expect(screen.getByPlaceholderText(/Search for a book you love.../i)).toBeInTheDocument();
    });

    it('updates input value on change', () => {
        render(<Hero />);
        const input = screen.getByPlaceholderText(/Search for a book you love.../i);

        fireEvent.change(input, { target: { value: 'Harry Potter' } });
        expect(input.value).toBe('Harry Potter');
    });

    it('calls onRecommend when a method button is clicked', () => {
        const onRecommend = vi.fn();
        render(<Hero onRecommend={onRecommend} />);

        const input = screen.getByPlaceholderText(/Search for a book you love.../i);
        fireEvent.change(input, { target: { value: 'Harry Potter' } });
        const searchButtons = screen.getAllByRole('button');
        fireEvent.click(searchButtons[0]);

        const hybridButton = screen.getByRole('button', { name: /hybrid/i });
        fireEvent.click(hybridButton);

        expect(onRecommend).toHaveBeenCalledWith('Harry Potter', 'hybrid');
    });
});
