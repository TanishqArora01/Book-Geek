import React, { useState } from 'react';

const Background = () => {
    const [particles] = useState(() => Array.from({ length: 12 }).map((_, i) => ({
        id: i,
        left: `${Math.random() * 100}%`,
        delay: `${Math.random() * 5}s`,
        duration: `${14 + Math.random() * 8}s`,
        size: `${Math.random() * 24 + 8}px`,
        opacity: 0.09 + Math.random() * 0.14,
    })));

    return (
        <>
            <div className="bg-animation" />
            <div className="particles">
                {particles.map((p) => (
                    <div
                        key={p.id}
                        className="particle"
                        style={{
                            left: p.left,
                            width: p.size,
                            height: p.size,
                            opacity: p.opacity,
                            animationDelay: p.delay,
                            animationDuration: p.duration,
                        }}
                    />
                ))}
            </div>
        </>
    );
};

export default Background;
