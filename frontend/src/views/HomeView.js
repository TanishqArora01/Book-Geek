import React, { useEffect, useState } from 'react';
import { Search, Sparkles, Sidebar as Shuffle, Users, BookOpen } from 'lucide-react';
import BookCard from '../components/BookCard';
import SkeletonBookCard from '../components/SkeletonBookCard';

const HomeView = ({ popularBooks, loadingPopular, onRecommend }) => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [showButtons, setShowButtons] = useState(false);
    const [isSearching, setIsSearching] = useState(false);
    const [searchFeedback, setSearchFeedback] = useState('');

    useEffect(() => {
        const normalized = query.trim();

        if (normalized.length < 2) {
            setResults([]);
            setSearchFeedback(normalized.length === 0 ? '' : 'Type at least 2 characters to search.');
            return;
        }

        const controller = new AbortController();
        const timeoutId = setTimeout(async () => {
            setIsSearching(true);
            setSearchFeedback('');

            try {
                const resp = await fetch(`/api/search_books?query=${encodeURIComponent(normalized)}`, {
                    signal: controller.signal,
                });

                if (!resp.ok) {
                    throw new Error('Search is temporarily unavailable.');
                }

                const data = await resp.json();
                const safeResults = Array.isArray(data) ? data : [];
                setResults(safeResults);

                if (safeResults.length === 0) {
                    setSearchFeedback('No exact matches found yet. Try a different spelling.');
                }
            } catch (err) {
                if (err.name !== 'AbortError') {
                    console.error(err);
                    setSearchFeedback('Could not complete the search. Please try again.');
                }
            } finally {
                setIsSearching(false);
            }
        }, 300);

        return () => {
            controller.abort();
            clearTimeout(timeoutId);
        };
    }, [query]);

    const handleSearchChange = (e) => {
        setQuery(e.target.value);
        setShowButtons(false);
    };

    const handleSelect = (title) => {
        setQuery(title);
        setResults([]);
        setShowButtons(true);
        setSearchFeedback('');
    };

    const canRecommend = query.trim().length > 0;

    return (
        <div className="home-view animate-in">
            {/* Hero Section */}
            <section className="hero-section pt-24 pb-16 px-4 text-center rounded-b-[40px] shadow-2xl relative z-20">
                <div className="container mx-auto max-w-4xl">
                    <div className="hero-badge cursor-default">
                        <Sparkles size={14} className="text-white" />
                        <span>AI-Powered Recommendations</span>
                    </div>

                    <h1 className="hero-title">BookGeek-AI</h1>
                    <p className="hero-subtitle">
                        Discover your next favorite read with a cinematic recommendation experience,
                        adaptive intelligence, and real-time hybrid ranking.
                    </p>

                    <div className="search-container max-w-xl mx-auto relative z-30">
                        <div className="search-input-wrapper">
                            <input
                                type="text"
                                className="flex-1 py-4 px-6 text-text-primary focus:outline-none text-[1rem]"
                                placeholder="Search for a book you love..."
                                value={query}
                                onChange={handleSearchChange}
                                onKeyDown={(e) => e.key === 'Enter' && setShowButtons(true)}
                            />
                            <button
                                className="search-btn-accent"
                                onClick={() => setShowButtons(true)}
                            >
                                <Search size={20} />
                            </button>
                        </div>

                        {results.length > 0 && (
                            <div className="absolute top-full left-0 w-full mt-2 bg-white border border-border rounded-lg shadow-xl z-50 overflow-hidden text-left">
                                {results.map((book, i) => (
                                    <button
                                        key={i}
                                        className="w-full flex items-center gap-3 p-3 hover:bg-bg-hover transition-all border-b border-border last:border-0"
                                        onClick={() => handleSelect(book.title)}
                                    >
                                        <img src={book.image_url} alt={book.title} className="w-9 h-13 object-cover rounded shadow-sm" />
                                        <div>
                                            <div className="font-semibold text-text-primary text-sm leading-tight">{book.title}</div>
                                            <div className="text-xs text-text-secondary mt-1">{book.author}</div>
                                        </div>
                                    </button>
                                ))}
                            </div>
                        )}

                        {isSearching && (
                            <div className="mt-3 text-xs font-semibold uppercase tracking-[0.08em] text-white/90">
                                Searching...
                            </div>
                        )}

                        {!isSearching && searchFeedback && (
                            <div className="mt-3 text-xs font-semibold text-white/85">
                                {searchFeedback}
                            </div>
                        )}

                        {showButtons && (
                            <div className="recommend-buttons mt-6 flex flex-wrap justify-center gap-3 animate-slide-up">
                                <button
                                    onClick={() => onRecommend(query, 'hybrid')}
                                    className="bg-gradient-to-r from-[#f59e0b] to-[#d97706] text-white px-5 py-2.5 rounded-lg font-bold text-sm shadow-md hover:-translate-y-0.5 transition-all flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:translate-y-0"
                                    disabled={!canRecommend}
                                >
                                    <Shuffle size={16} /> Hybrid
                                </button>
                                <button
                                    onClick={() => onRecommend(query, 'collaborative')}
                                    className="bg-gradient-to-r from-[#0891b2] to-[#0e7490] text-white px-5 py-2.5 rounded-lg font-bold text-sm shadow-md hover:-translate-y-0.5 transition-all flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:translate-y-0"
                                    disabled={!canRecommend}
                                >
                                    <Users size={16} /> Collab
                                </button>
                                <button
                                    onClick={() => onRecommend(query, 'content')}
                                    className="bg-gradient-to-r from-[#0f766e] to-[#115e59] text-white px-5 py-2.5 rounded-lg font-bold text-sm shadow-md hover:-translate-y-0.5 transition-all flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:translate-y-0"
                                    disabled={!canRecommend}
                                >
                                    <BookOpen size={16} /> Content
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </section>

            {/* Methods Section */}
            <section className="py-20 bg-white border-b border-border">
                <div className="container mx-auto max-w-6xl px-4 text-center">
                    <div className="mb-12">
                        <h2 className="text-2xl font-bold text-text-primary mb-2">How Book Geek Thinks</h2>
                        <p className="text-text-secondary text-sm">A multi-model stack with confidence-aware ranking and instant feedback.</p>
                    </div>
                    <div className="grid md:grid-cols-3 gap-6">
                        <div className="bg-bg-body p-8 rounded-xl border border-border hover:shadow-md transition-all text-center group stagger-item" style={{ animationDelay: '40ms' }}>
                            <div className="w-11 h-11 bg-gradient-to-r from-[#6366f1] to-[#4f46e5] text-white rounded-lg flex items-center justify-center mx-auto mb-5">
                                <Users size={20} />
                            </div>
                            <h3 className="text-[1.05rem] font-bold mb-3">Collaborative Filtering</h3>
                            <p className="text-text-secondary text-sm leading-relaxed">Finds books loved by readers with similar tastes to yours</p>
                        </div>
                        <div className="bg-bg-body p-8 rounded-xl border border-border hover:shadow-md transition-all text-center group stagger-item" style={{ animationDelay: '120ms' }}>
                            <div className="w-11 h-11 bg-gradient-to-r from-[#10b981] to-[#059669] text-white rounded-lg flex items-center justify-center mx-auto mb-5">
                                <BookOpen size={20} />
                            </div>
                            <h3 className="text-[1.05rem] font-bold mb-3">Content-Based</h3>
                            <p className="text-text-secondary text-sm leading-relaxed">Analyzes book content, genres, and metadata to find similar titles</p>
                        </div>
                        <div className="bg-bg-body p-8 rounded-xl border border-border hover:shadow-md transition-all text-center group stagger-item" style={{ animationDelay: '200ms' }}>
                            <div className="w-11 h-11 bg-gradient-to-r from-[#f59e0b] to-[#d97706] text-white rounded-lg flex items-center justify-center mx-auto mb-5">
                                <Shuffle size={20} />
                            </div>
                            <h3 className="text-[1.05rem] font-bold mb-3">Hybrid Model</h3>
                            <p className="text-text-secondary text-sm leading-relaxed">Combines both methods for the most accurate recommendations</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Popular Books Section */}
            <section className="py-20">
                <div className="container mx-auto max-w-7xl px-4">
                    <div className="text-center mb-12">
                        <h2 className="text-2xl font-bold text-text-primary mb-2">Trending Books</h2>
                        <p className="text-text-secondary text-sm">Top rated books by the Book Geek community</p>
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5">
                        {loadingPopular
                            ? Array.from({ length: 10 }).map((_, i) => <SkeletonBookCard key={`popular-skeleton-${i}`} />)
                            : popularBooks.map((book, i) => (
                                <div key={i} className="stagger-item" style={{ animationDelay: `${i * 50}ms` }}>
                                    <BookCard book={book} onRecommend={onRecommend} />
                                </div>
                            ))}
                    </div>
                </div>
            </section>
        </div>
    );
};

export default HomeView;
