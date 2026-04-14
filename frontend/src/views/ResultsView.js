import React from 'react';
import { ArrowLeft, Star, Calendar, Building, CheckCircle, Search, Shuffle, Users, BookOpen } from 'lucide-react';
import BookCard from '../components/BookCard';
import SkeletonBookCard from '../components/SkeletonBookCard';

const ResultsView = ({ bookTitle, selectedBook, recommendations, loadingRecommendations, method, onBack, onRecommend }) => {
    const methodLabel = method.charAt(0).toUpperCase() + method.slice(1);
    const scoredRecommendations = recommendations.filter((book) => typeof book.score === 'number');
    const averageScore = scoredRecommendations.length > 0
        ? Math.round((scoredRecommendations.reduce((acc, book) => acc + book.score, 0) / scoredRecommendations.length) * 100)
        : null;

    return (
        <div className="results-view animate-in">
            {/* Navbar */}
            <nav className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-border py-4 px-4 shadow-sm">
                <div className="container mx-auto max-w-7xl flex justify-between items-center">
                    <button
                        onClick={onBack}
                        className="flex items-center gap-2 py-2 px-4 border border-border rounded-lg text-text-secondary hover:bg-bg-hover hover:text-text-primary transition-all text-sm font-medium"
                    >
                        <ArrowLeft size={16} />
                        Back to Home
                    </button>
                    <div className={`method-badge method-badge-${method}`}>
                        {method === 'hybrid' ? <Shuffle size={14} /> : method === 'collaborative' ? <Users size={14} /> : <BookOpen size={14} />}
                        <span className="ml-1.5">{methodLabel}</span>
                    </div>
                </div>
            </nav>

            {/* Selected Book Section */}
            <section className="bg-white py-12 border-b border-border px-4">
                <div className="container mx-auto max-w-5xl">
                    <div className="flex items-center gap-2.5 text-[0.78rem] font-bold uppercase tracking-[0.08em] text-text-muted mb-6 after:content-[''] after:flex-1 after:h-[1px] after:bg-border">
                        <Star size={14} className="fill-accent text-accent" />
                        <span>Your Selected Book</span>
                    </div>

                    {selectedBook ? (
                        <div className="flex flex-col md:flex-row gap-8 items-start">
                            <div className="w-32 h-48 flex-shrink-0 rounded-lg overflow-hidden shadow-2xl border border-border bg-bg-body">
                                <img src={selectedBook.image_url} alt={selectedBook.title} className="w-full h-full object-cover" />
                            </div>
                            <div className="flex-1 pt-1">
                                <h1 className="text-3xl md:text-4xl font-extrabold text-text-primary leading-tight mb-1">{selectedBook.title}</h1>
                                <p className="text-xl text-text-secondary mb-5">by {selectedBook.author}</p>

                                <div className="flex flex-wrap gap-3 mb-6">
                                    {selectedBook.year && (
                                        <div className="flex items-center gap-2 px-3 py-1.5 bg-bg-body rounded-md text-sm text-text-secondary">
                                            <Calendar size={14} className="text-accent" /> {selectedBook.year}
                                        </div>
                                    )}
                                    {selectedBook.publisher && (
                                        <div className="flex items-center gap-2 px-3 py-1.5 bg-bg-body rounded-md text-sm text-text-secondary">
                                            <Building size={14} className="text-accent" /> {selectedBook.publisher}
                                        </div>
                                    )}
                                </div>

                                <div className="border-t border-border pt-6 mt-6">
                                    <span className="text-text-secondary text-[0.8rem] block mb-3 opacity-60">Get specific recommendations for this book:</span>
                                    <div className="flex flex-wrap gap-2.5">
                                        <button onClick={() => onRecommend(selectedBook.title, 'hybrid')} className="flex items-center gap-2 py-2 px-4 border border-border rounded-lg text-sm font-medium hover:border-accent hover:text-accent transition-all">
                                            <Shuffle size={14} /> Hybrid
                                        </button>
                                        <button onClick={() => onRecommend(selectedBook.title, 'collaborative')} className="flex items-center gap-2 py-2 px-4 border border-border rounded-lg text-sm font-medium hover:border-accent hover:text-accent transition-all">
                                            <Users size={14} /> Collab
                                        </button>
                                        <button onClick={() => onRecommend(selectedBook.title, 'content')} className="flex items-center gap-2 py-2 px-4 border border-border rounded-lg text-sm font-medium hover:border-accent hover:text-accent transition-all">
                                            <BookOpen size={14} /> Content
                                        </button>
                                    </div>
                                </div>

                                <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-[#fef3c7] text-[#92400e] rounded-full font-bold text-[0.78rem] mt-6">
                                    <CheckCircle size={14} /> Showing {methodLabel} recommendations
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="rounded-xl border border-border bg-bg-body px-6 py-8 text-2xl font-extrabold text-text-primary shadow-sm">
                            Recommendations for "{bookTitle}"
                        </div>
                    )}
                </div>
            </section>

            {/* Recommendations Section */}
            <section className="py-12 px-4 bg-bg-body min-h-[50vh]">
                <div className="container mx-auto max-w-7xl">
                    {!loadingRecommendations && recommendations.length > 0 && (
                        <div className="mb-6 rounded-xl border border-border bg-white px-4 py-3 shadow-sm">
                            <div className="flex flex-wrap items-center gap-3 text-sm text-text-secondary">
                                <span className="inline-flex items-center rounded-full bg-bg-hover px-3 py-1 font-semibold text-text-primary">
                                    {recommendations.length} recommendations
                                </span>
                                <span className="inline-flex items-center rounded-full bg-bg-hover px-3 py-1 font-semibold text-text-primary">
                                    Method: {methodLabel}
                                </span>
                                {averageScore !== null && (
                                    <span className="inline-flex items-center rounded-full bg-[#dff7f3] px-3 py-1 font-semibold text-[#0f766e]">
                                        Avg confidence: {averageScore}%
                                    </span>
                                )}
                            </div>
                        </div>
                    )}

                    {loadingRecommendations ? (
                        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5">
                            {Array.from({ length: 10 }).map((_, i) => (
                                <div key={`results-skeleton-${i}`} className="stagger-item" style={{ animationDelay: `${i * 40}ms` }}>
                                    <SkeletonBookCard compact />
                                </div>
                            ))}
                        </div>
                    ) : recommendations.length === 0 ? (
                        <div className="text-center py-20 bg-white border border-dashed border-border rounded-xl shadow-sm">
                            <BookOpen size={48} className="mx-auto text-text-muted mb-4" />
                            <h3 className="text-xl font-bold mb-2">No Recommendations Found</h3>
                            <p className="text-text-secondary mb-6">Try a different book or method.</p>
                            <button onClick={onBack} className="bg-accent hover:bg-accent-hover text-white px-6 py-2.5 rounded-lg font-medium transition-all inline-flex items-center gap-2">
                                <Search size={18} /> Search Another Book
                            </button>
                        </div>
                    ) : (
                        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5">
                            {recommendations.map((book, i) => (
                                <div key={i} className="stagger-item" style={{ animationDelay: `${i * 50}ms` }}>
                                    <BookCard book={book} onRecommend={onRecommend} mode="results" />
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </section>
        </div>
    );
};

export default ResultsView;
