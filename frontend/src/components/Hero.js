import React, { useState } from 'react';
import { Search, Sparkles, Sidebar as Shuffle, Users, BookOpen } from 'lucide-react';

const Hero = ({ onRecommend }) => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [showButtons, setShowButtons] = useState(false);

    const handleSearchChange = async (e) => {
        const val = e.target.value;
        setQuery(val);
        if (val.length > 2) {
            try {
                const resp = await fetch(`/api/search_books?query=${encodeURIComponent(val)}`);
                const data = await resp.json();
                setResults(data);
            } catch (err) {
                console.error(err);
            }
        } else {
            setResults([]);
        }
    };

    const handleSelect = (title) => {
        setQuery(title);
        setResults([]);
        setShowButtons(true);
    };

    const handleAction = (method) => {
        if (query.trim()) {
            onRecommend(query, method);
        }
    };

    return (
        <section className="hero-section py-20 flex flex-col items-center text-center px-4 bg-hero text-white mb-20 rounded-3xl shadow-xl">
            <div className="hero-badge px-4 py-1 bg-white/20 backdrop-blur-md rounded-full text-sm font-medium mb-6 flex items-center gap-2">
                <Sparkles size={16} />
                AI-Powered Recommendations
            </div>

            <h1 className="text-5xl md:text-7xl font-extrabold mb-4 tracking-tight">
                BookGeek-AI
            </h1>
            <p className="text-xl text-white/80 max-w-2xl mb-10 leading-relaxed">
                Discover your next favorite book with our intelligent hybrid recommendation engine
                that learns from millions of readers
            </p>

            <div className="search-container w-full max-w-xl relative mb-8">
                <div className="search-input-wrapper bg-white rounded-xl shadow-lg flex overflow-hidden">
                    <input
                        type="text"
                        className="search-input flex-1 py-4 px-6 text-slate-800 focus:outline-none text-lg"
                        placeholder="Search for a book you love..."
                        value={query}
                        onChange={handleSearchChange}
                        onKeyDown={(e) => e.key === 'Enter' && setShowButtons(true)}
                    />
                    <button
                        className="bg-accent hover:bg-accent-hover px-6 text-white transition-colors"
                        onClick={() => setShowButtons(true)}
                    >
                        <Search size={22} />
                    </button>
                </div>

                {results.length > 0 && (
                    <div className="absolute top-full left-0 w-full mt-2 bg-white border border-slate-200 rounded-xl shadow-2xl z-50 overflow-hidden text-left">
                        {results.map((book, i) => (
                            <button
                                key={i}
                                className="w-full flex items-center gap-4 p-4 hover:bg-slate-50 transition-all border-b border-slate-100 last:border-0"
                                onClick={() => handleSelect(book.title)}
                            >
                                <img src={book.image_url} alt={book.title} className="w-10 h-14 object-cover rounded shadow-sm" />
                                <div>
                                    <div className="font-semibold text-slate-900 leading-tight">{book.title}</div>
                                    <div className="text-sm text-slate-500 mt-1">{book.author}</div>
                                </div>
                            </button>
                        ))}
                    </div>
                )}
            </div>

            {showButtons && (
                <div className="recommend-buttons mt-8 flex flex-wrap justify-center gap-3 animate-in fade-in slide-in-from-top-4 duration-300">
                    <button
                        onClick={() => handleAction('hybrid')}
                        className="bg-gradient-to-r from-orange-400 to-orange-600 hover:from-orange-500 hover:to-orange-700 text-white px-6 py-3 rounded-lg font-bold text-sm shadow-md hover:-translate-y-1 transition-all flex items-center gap-2"
                    >
                        <Shuffle size={16} />
                        Hybrid
                    </button>
                    <button
                        onClick={() => handleAction('collaborative')}
                        className="bg-gradient-to-r from-indigo-500 to-indigo-700 hover:from-indigo-600 hover:to-indigo-800 text-white px-6 py-3 rounded-lg font-bold text-sm shadow-md hover:-translate-y-1 transition-all flex items-center gap-2"
                    >
                        <Users size={16} />
                        Collaborative
                    </button>
                    <button
                        onClick={() => handleAction('content')}
                        className="bg-gradient-to-r from-emerald-500 to-emerald-700 hover:from-emerald-600 hover:to-emerald-800 text-white px-6 py-3 rounded-lg font-bold text-sm shadow-md hover:-translate-y-1 transition-all flex items-center gap-2"
                    >
                        <BookOpen size={16} />
                        Content-Based
                    </button>
                </div>
            )}
        </section>
    );
};

export default Hero;
