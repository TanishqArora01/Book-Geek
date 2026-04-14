import React from 'react';
import { Sidebar as Shuffle, Users, BookOpen, ChartLine } from 'lucide-react';

const FALLBACK_IMAGE = 'https://placehold.co/150x220/f5f7ff/22314d?text=No+Cover';

const BookCard = ({ book, onRecommend, mode = 'popular' }) => {
    return (
        <div className="book-card bg-white border border-border rounded-xl flex flex-col h-full group">
            <div className="book-card-image relative aspect-[3/4] p-4 flex items-center justify-center bg-bg-body border-b border-border rounded-t-xl overflow-hidden">
                {mode === 'results' && (
                    <>
                        <div className={`type-badge method-badge-${book.type || 'hybrid'} absolute top-2 right-2 scale-75 origin-top-right`}>
                            {book.type === 'hybrid' ? <Shuffle size={12} /> : book.type === 'collaborative' ? <Users size={12} /> : <BookOpen size={12} />}
                            <span className="ml-1 uppercase">{book.type || 'hybrid'}</span>
                        </div>
                        <div className="score-badge absolute bottom-2 left-2 bg-black/70 text-[#34d399] px-2 py-1 rounded text-[0.68rem] font-bold flex items-center gap-1">
                            <ChartLine size={10} /> {Math.round((book.score || 0.85) * 100)}% Match
                        </div>
                    </>
                )}
                <img
                    src={book.image_url}
                    alt={book.title}
                    className="max-h-full max-w-full object-contain rounded shadow-sm transition-transform duration-500 group-hover:scale-[1.04]"
                    loading="lazy"
                    onError={(e) => {
                        e.currentTarget.onerror = null;
                        e.currentTarget.src = FALLBACK_IMAGE;
                    }}
                />
            </div>

            <div className="book-card-body p-4 flex flex-col flex-grow text-left">
                <h4 className="book-card-title text-[0.9rem] font-bold text-text-primary mb-1 line-clamp-2 h-[2.8em] leading-snug">
                    {book.title}
                </h4>
                <p className="book-card-author text-[0.82rem] text-text-secondary mb-1">
                    {book.author}
                </p>
                {(book.year || book.publisher) && (
                    <p className="book-card-meta text-[0.75rem] text-text-muted mb-4 italic">
                        {book.year || 'N/A'} • {book.publisher || 'N/A'}
                    </p>
                )}

                <div className="book-card-actions mt-auto flex flex-wrap gap-1.5 pt-2">
                    <button
                        onClick={() => onRecommend(book.title, 'hybrid')}
                        className="action-btn flex-1 flex items-center justify-center gap-1.5 p-2 rounded-md border border-border text-text-secondary hover:text-accent hover:border-accent hover:bg-bg-hover transition-all active:scale-95 text-[0.7rem] font-bold"
                        title="Hybrid"
                        aria-label={`Get hybrid recommendations for ${book.title}`}
                    >
                        <Shuffle size={12} /> Hybrid
                    </button>
                    <button
                        onClick={() => onRecommend(book.title, 'collaborative')}
                        className="action-btn flex-1 flex items-center justify-center gap-1.5 p-2 rounded-md border border-border text-text-secondary hover:text-accent hover:border-accent hover:bg-bg-hover transition-all active:scale-95 text-[0.7rem] font-bold"
                        title="Collaborative"
                        aria-label={`Get collaborative recommendations for ${book.title}`}
                    >
                        <Users size={12} /> Collab
                    </button>
                    <button
                        onClick={() => onRecommend(book.title, 'content')}
                        className="action-btn flex-1 flex items-center justify-center gap-1.5 p-2 rounded-md border border-border text-text-secondary hover:text-accent hover:border-accent hover:bg-bg-hover transition-all active:scale-95 text-[0.7rem] font-bold"
                        title="Content-Based"
                        aria-label={`Get content-based recommendations for ${book.title}`}
                    >
                        <BookOpen size={12} /> Content
                    </button>
                </div>
            </div>
        </div>
    );
};

export default BookCard;
