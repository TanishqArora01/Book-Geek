import React from 'react';

const SkeletonBookCard = ({ compact = false }) => {
  return (
    <div className="book-card bg-white border border-border rounded-xl flex flex-col h-full overflow-hidden">
      <div className="relative aspect-[3/4] p-4 bg-bg-hover border-b border-border">
        <div className="h-full w-full rounded-lg skeleton-shimmer" />
      </div>

      <div className="p-4 flex flex-col gap-2.5">
        <div className="h-4 w-5/6 rounded skeleton-shimmer" />
        <div className="h-3.5 w-3/5 rounded skeleton-shimmer" />
        <div className="h-3 w-2/3 rounded skeleton-shimmer" />

        {!compact && (
          <div className="mt-3 grid grid-cols-3 gap-1.5">
            <div className="h-7 rounded skeleton-shimmer" />
            <div className="h-7 rounded skeleton-shimmer" />
            <div className="h-7 rounded skeleton-shimmer" />
          </div>
        )}
      </div>
    </div>
  );
};

export default SkeletonBookCard;
