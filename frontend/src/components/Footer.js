import React from 'react';
import { Github, Linkedin, MapPin, Mail, Phone } from 'lucide-react';

const Footer = () => {
    return (
        <footer className="footer relative z-10 border-t border-border/70 bg-white/75 px-4 pt-16 pb-10 backdrop-blur-xl">
            <div className="container mx-auto max-w-7xl">
                <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr] mb-12">
                    <div className="overflow-hidden rounded-3xl border border-border/70 bg-gradient-to-br from-white via-white to-[#f3fbff] p-8 shadow-[0_20px_45px_rgba(15,23,42,0.08)]">
                        <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-[#dcf7f5] px-3 py-1 text-[0.72rem] font-bold uppercase tracking-[0.18em] text-[#0f766e]">
                            Stay connected
                        </div>
                        <h5 className="text-[1.05rem] font-bold mb-3 text-text-primary">BookGeek-AI</h5>
                        <p className="max-w-xl text-sm leading-relaxed text-text-secondary">
                            A sharper recommendation experience with animated discovery, smart ranking, and a cleaner interface built for fast browsing.
                        </p>

                        <div className="mt-8 grid gap-3 sm:grid-cols-3">
                            <a href="https://github.com/TanishqArora01" target="_blank" rel="noopener noreferrer" className="group inline-flex items-center gap-3 rounded-2xl border border-border bg-white/80 px-4 py-3 text-sm font-medium text-text-secondary shadow-sm transition-all hover:-translate-y-0.5 hover:border-accent/40 hover:text-accent hover:shadow-md">
                                <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#e7f6ff] text-[#0b7285] transition-transform group-hover:scale-110">
                                    <Github size={16} />
                                </span>
                                <span className="flex flex-col text-left">
                                    <span className="text-xs uppercase tracking-[0.12em] text-text-muted">Github</span>
                                    <span>TanishqArora01</span>
                                </span>
                            </a>

                            <a href="https://www.linkedin.com/in/tanishq-arora-ai/" target="_blank" rel="noopener noreferrer" className="group inline-flex items-center gap-3 rounded-2xl border border-border bg-white/80 px-4 py-3 text-sm font-medium text-text-secondary shadow-sm transition-all hover:-translate-y-0.5 hover:border-accent/40 hover:text-accent hover:shadow-md">
                                <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#eff6ff] text-[#0f4c81] transition-transform group-hover:scale-110">
                                    <Linkedin size={16} />
                                </span>
                                <span className="flex flex-col text-left">
                                    <span className="text-xs uppercase tracking-[0.12em] text-text-muted">Linkedin</span>
                                    <span>Tanishq Arora AI</span>
                                </span>
                            </a>

                            <div className="group inline-flex items-center gap-3 rounded-2xl border border-border bg-white/80 px-4 py-3 text-sm font-medium text-text-secondary shadow-sm transition-all">
                                <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#ecfeff] text-[#0f766e]">
                                    <Mail size={16} />
                                </span>
                                <span className="flex flex-col text-left">
                                    <span className="text-xs uppercase tracking-[0.12em] text-text-muted">Email</span>
                                    <span>aroratanishq54@gmail.com</span>
                                </span>
                            </div>
                        </div>
                    </div>

                    <div className="rounded-3xl border border-border/70 bg-white/90 p-8 shadow-[0_20px_45px_rgba(15,23,42,0.08)]">
                        <h5 className="text-[0.95rem] font-bold mb-5 text-text-primary">Contact</h5>
                        <ul className="list-none space-y-4">
                            <li className="flex items-start gap-3 rounded-2xl bg-bg-body/70 px-4 py-3 text-text-secondary">
                                <MapPin size={16} className="mt-0.5 shrink-0 text-accent" />
                                <span>Jhajjar, Haryana</span>
                            </li>
                            <li className="flex items-start gap-3 rounded-2xl bg-bg-body/70 px-4 py-3 text-text-secondary">
                                <Mail size={16} className="mt-0.5 shrink-0 text-accent" />
                                <span>aroratanishq54@gmail.com</span>
                            </li>
                            <li className="flex items-start gap-3 rounded-2xl bg-bg-body/70 px-4 py-3 text-text-secondary">
                                <Phone size={16} className="mt-0.5 shrink-0 text-accent" />
                                <span>+91-8901502383</span>
                            </li>
                        </ul>
                    </div>
                </div>
                <div className="text-center pt-6 border-t border-border text-text-muted text-[0.82rem]">
                    <p>&copy; 2026 BookGeek-AI. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
