import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import BookCard from './BookCard';

describe('BookCard', () => {
    const mockBook = {
        title: 'Test Book',
        author: 'Test Author',
        image_url: 'http://example.com/image.jpg'
    };

    it('renders book details correctly', () => {
        render(<BookCard book={mockBook} />);

        expect(screen.getByText('Test Book')).toBeInTheDocument();
        expect(screen.getByText('Test Author')).toBeInTheDocument();
        expect(screen.getByRole('img')).toHaveAttribute('src', mockBook.image_url);
    });

    it('calls onRecommend when a method button is clicked', () => {
        const onRecommend = vi.fn();
        render(<BookCard book={mockBook} onRecommend={onRecommend} />);

        const hybridButton = screen.getByTitle('Hybrid');
        fireEvent.click(hybridButton);

        expect(onRecommend).toHaveBeenCalledWith(mockBook.title, 'hybrid');
    });
});
