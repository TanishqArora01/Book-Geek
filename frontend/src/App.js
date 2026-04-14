import React, { useState, useEffect } from 'react';
import Background from './components/Background';
import HomeView from './views/HomeView';
import ResultsView from './views/ResultsView';
import Footer from './components/Footer';

function App() {
  const [popularBooks, setPopularBooks] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingPopular, setLoadingPopular] = useState(true);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [view, setView] = useState('home'); // 'home' or 'results'
  const [method, setMethod] = useState('hybrid');
  const [bookTitle, setBookTitle] = useState('');
  const [apiError, setApiError] = useState('');

  useEffect(() => {
    let isMounted = true;

    const fetchPopularBooks = async () => {
      try {
        setLoadingPopular(true);
        const response = await fetch('/api/popular');
        if (!response.ok) {
          throw new Error('Failed to load popular books.');
        }

        const data = await response.json();
        if (isMounted) {
          setPopularBooks(Array.isArray(data) ? data : []);
        }
      } catch (err) {
        console.error(err);
        if (isMounted) {
          setApiError('Popular books could not be loaded right now. Recommendations still work.');
        }
      } finally {
        if (isMounted) {
          setLoadingPopular(false);
        }
      }
    };

    fetchPopularBooks();

    return () => {
      isMounted = false;
    };
  }, []);

  const handleRecommend = async (title, selectedMethod) => {
    const normalizedTitle = title.trim();
    if (!normalizedTitle) {
      setApiError('Choose or type a valid book title first.');
      return;
    }

    setApiError('');
    setLoading(true);
    setLoadingRecommendations(true);
    setMethod(selectedMethod);
    setBookTitle(normalizedTitle);
    setView('results');
    setRecommendations([]);
    setSelectedBook({
      title: normalizedTitle,
      author: 'Matching with the Book Geek graph...',
      image_url: 'https://placehold.co/280x420/f5f7ff/22314d?text=Book+Geek',
      year: null,
      publisher: null,
    });

    try {
      const formData = new FormData();
      formData.append('book_title', normalizedTitle);
      formData.append('method', selectedMethod);

      const resp = await fetch('/api/recommend', {
        method: 'POST',
        body: formData,
      });

      if (!resp.ok) {
        let serverMessage = 'Failed to fetch recommendations.';
        try {
          const errorPayload = await resp.json();
          if (errorPayload && typeof errorPayload.detail === 'string') {
            serverMessage = errorPayload.detail;
          }
        } catch {
          // Ignore parsing error and keep fallback message.
        }

        throw new Error(serverMessage);
      }

      const data = await resp.json();
      setRecommendations(Array.isArray(data.recommendations) ? data.recommendations : []);
      setSelectedBook(data.selected_book || null);

      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      console.error(err);
      setApiError(err.message || 'Something went wrong while fetching recommendations.');
      setSelectedBook(null);
    } finally {
      setLoading(false);
      setLoadingRecommendations(false);
    }
  };

  const handleBack = () => {
    setView('home');
    setRecommendations([]);
    setSelectedBook(null);
    setApiError('');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="relative min-h-screen text-text-primary bg-bg-body font-inter selection:bg-accent/30">
      <Background />

      {loading && (
        <div className="fixed top-0 left-0 right-0 z-[100] h-1 overflow-hidden bg-transparent">
          <div className="h-full w-1/3 animate-progress bg-gradient-to-r from-[#ffb347] via-[#7bdff2] to-[#0b7285]"></div>
        </div>
      )}

      <main className="relative z-10">
        {apiError && (
          <div className="mx-auto max-w-5xl px-4 pt-6">
            <div className="rounded-xl border border-[#ef4444]/20 bg-[#fee2e2]/80 px-4 py-3 text-sm font-medium text-[#991b1b] backdrop-blur-sm">
              {apiError}
            </div>
          </div>
        )}

        {view === 'home' ? (
          <HomeView
            popularBooks={popularBooks}
            loadingPopular={loadingPopular}
            onRecommend={handleRecommend}
          />
        ) : (
          <ResultsView
            bookTitle={bookTitle}
            selectedBook={selectedBook}
            recommendations={recommendations}
            loadingRecommendations={loadingRecommendations}
            method={method}
            onBack={handleBack}
            onRecommend={handleRecommend}
          />
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;
