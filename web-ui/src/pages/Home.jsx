import { Database, Zap, BookOpen, Clock, ArrowRight, Github, Code, Layers, FileDown } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Home() {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '5rem', paddingBottom: '4rem' }}>

            {/* Hero Section */}
            <section style={{ textAlign: 'center', paddingTop: '4rem', paddingBottom: '2rem' }}>
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(37, 99, 235, 0.1)', border: '1px solid rgba(37, 99, 235, 0.2)', padding: '0.5rem 1rem', borderRadius: '9999px', color: 'var(--primary-light)', fontSize: '0.875rem', fontWeight: 600, marginBottom: '2rem' }}>
                    <span style={{ width: '8px', height: '8px', background: 'var(--primary)', borderRadius: '50%', display: 'inline-block', boxShadow: '0 0 8px var(--primary)' }}></span>
                    v1.0.0 Now Live
                </div>

                <h1 style={{ fontSize: 'clamp(2.5rem, 5vw, 4.5rem)', fontWeight: 800, letterSpacing: '-0.03em', lineHeight: 1.1, marginBottom: '1.5rem', maxWidth: '900px', margin: '0 auto 1.5rem' }}>
                    The Interactive <br />
                    <span className="text-gradient">Database Engine</span>
                </h1>

                <p style={{ fontSize: '1.125rem', color: 'var(--muted-foreground)', maxWidth: '650px', margin: '0 auto', lineHeight: 1.6, marginBottom: '3rem' }}>
                    A lightweight, Python-based educational B-Tree database engine. Experience query execution, paging, and serialization step-by-step in real time.
                </p>

                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
                    <Link to="/editor" className="btn btn-primary">
                        Start Writing Queries <ArrowRight size={18} />
                    </Link>
                    <a href="https://github.com/SouvickSarkar20/sqlite-clone" target="_blank" rel="noreferrer" className="btn btn-outline">
                        <Github size={18} /> View Source Code
                    </a>
                </div>
            </section>



            {/* Core Architecture Features Grid */}
            <section>
                <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
                    <h2 style={{ fontSize: '2.5rem', fontWeight: 700, letterSpacing: '-0.02em', marginBottom: '1rem' }}>Architected for Understanding</h2>
                    <p style={{ color: 'var(--muted-foreground)', maxWidth: '600px', margin: '0 auto' }}>Deep dive into the internals of database design, from lexical parsing down to raw byte allocation.</p>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
                    <div className="feature-card">
                        <div className="icon-wrapper">
                            <Code size={24} />
                        </div>
                        <h3 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>Custom SQL Parser</h3>
                        <p style={{ color: 'var(--muted-foreground)', lineHeight: 1.6 }}>
                            Transforms raw SQL strings into structured syntax trees, intelligently validating CREATE, INSERT, and SELECT grammar.
                        </p>
                    </div>

                    <div className="feature-card">
                        <div className="icon-wrapper">
                            <Layers size={24} />
                        </div>
                        <h3 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>B-Tree Indexing</h3>
                        <p style={{ color: 'var(--muted-foreground)', lineHeight: 1.6 }}>
                            A robust storage paradigm that inherently supports automatic page splitting at capacity, maintaining search efficiency.
                        </p>
                    </div>

                    <div className="feature-card">
                        <div className="icon-wrapper">
                            <FileDown size={24} />
                        </div>
                        <h3 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.75rem' }}>Disk Pager & Serializer</h3>
                        <p style={{ color: 'var(--muted-foreground)', lineHeight: 1.6 }}>
                            Manages memory-to-disk translation via struct packing, ensuring every byte is correctly aligned and persisted safely.
                        </p>
                    </div>
                </div>
            </section>

            {/* Interactive Execution Block */}
            <section className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '2rem', padding: '3rem' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr minmax(300px, 1fr)', gap: '3rem', alignItems: 'center' }}>
                    <div>
                        <div style={{ display: 'inline-block', background: 'rgba(16, 185, 129, 0.1)', color: 'var(--success)', padding: '0.5rem 1rem', borderRadius: '8px', fontWeight: 600, fontSize: '0.875rem', marginBottom: '1.5rem' }}>
                            Real-Time Feedback
                        </div>
                        <h2 style={{ fontSize: '2rem', fontWeight: 700, letterSpacing: '-0.02em', marginBottom: '1.5rem' }}>
                            Visualize the Execution Step-by-Step
                        </h2>
                        <p style={{ color: 'var(--muted-foreground)', lineHeight: 1.6, marginBottom: '1.5rem', fontSize: '1.1rem' }}>
                            We've bridged the Python backend with a React UI to expose the exact sequence of events that occurs when you press Enter.
                        </p>
                        <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            {['Parsing & Validation', 'B-Tree Traversal & Node Splitting', 'I/O Disk Serialization'].map((item, i) => (
                                <li key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--foreground)', fontWeight: 500 }}>
                                    <div style={{ background: 'var(--primary)', borderRadius: '50%', padding: '2px', color: '#fff' }}>
                                        <Zap size={14} />
                                    </div>
                                    {item}
                                </li>
                            ))}
                        </ul>
                    </div>
                    {/* Mock UI for demonstration */}
                    <div style={{ background: '#000', borderRadius: '12px', border: '1px solid var(--border)', padding: '1.5rem', boxShadow: '0 20px 40px rgba(0,0,0,0.5)' }}>
                        <div style={{ borderBottom: '1px solid var(--border)', paddingBottom: '1rem', marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
                            <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#ef4444' }}></div>
                            <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#f59e0b' }}></div>
                            <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#10b981' }}></div>
                        </div>
                        <div style={{ fontFamily: 'monospace', color: 'var(--primary-light)', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
                            &gt; INSERT INTO users VALUES (1, 'Alice', 25)
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}><div style={{ width: 16, height: 16, background: 'var(--success)', borderRadius: '50%' }}></div><span style={{ fontSize: '0.85rem' }}>Parsing SQL syntax</span></div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}><div style={{ width: 16, height: 16, background: 'var(--success)', borderRadius: '50%' }}></div><span style={{ fontSize: '0.85rem' }}>Searching B-Tree for PK</span></div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}><div style={{ width: 16, height: 16, background: 'var(--primary)', borderRadius: '50%', boxShadow: '0 0 10px var(--primary)' }}></div><span style={{ fontSize: '0.85rem', color: 'white' }}>Writing Page 2 to Disk...</span></div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Future Roadmap : Delete */}
            <section style={{ position: 'relative', marginTop: '3rem' }}>
                <div className="glass-panel" style={{ background: 'linear-gradient(135deg, rgba(10,10,13,1) 0%, rgba(15,23,42,1) 100%)', border: '1px solid rgba(59, 130, 246, 0.2)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.25rem' }}>
                        <div style={{ background: 'rgba(37, 99, 235, 0.2)', padding: '0.5rem', borderRadius: '10px' }}>
                            <Clock color="var(--primary-light)" size={24} />
                        </div>
                        <h3 style={{ fontSize: '1.75rem', fontWeight: 600 }}>Roadmap: Implementing DELETE</h3>
                    </div>
                    <p style={{ color: 'var(--muted-foreground)', lineHeight: 1.7, marginBottom: '1.5rem', fontSize: '1.05rem', maxWidth: '800px' }}>
                        Currently, the engine robustly handles <code style={{ color: 'var(--primary-light)', background: 'rgba(37,99,235,0.1)', padding: '2px 6px', borderRadius: '4px' }}>CREATE</code>, <code style={{ color: 'var(--primary-light)', background: 'rgba(37,99,235,0.1)', padding: '2px 6px', borderRadius: '4px' }}>INSERT</code>, and <code style={{ color: 'var(--primary-light)', background: 'rgba(37,99,235,0.1)', padding: '2px 6px', borderRadius: '4px' }}>SELECT</code>. Our next major milestone is implementing row deletion.
                    </p>
                    <div style={{ background: 'rgba(0,0,0,0.4)', border: '1px solid var(--border)', borderRadius: '12px', padding: '1.5rem' }}>
                        <h4 style={{ color: 'var(--foreground)', marginBottom: '0.75rem', fontWeight: 600 }}>The "Lazy Delete" Architecture</h4>
                        <p style={{ color: 'var(--muted-foreground)', lineHeight: 1.6, fontSize: '0.95rem' }}>
                            True B-Tree deletion involves highly complex Node Rebalancing (borrowing from sibling nodes or merging deflated nodes). Instead of rewriting the structural constraints, we will adopt a production-standard <strong>Lazy Deletion</strong> strategy. Deleted records will be flagged with an <code>is_deleted</code> metadata byte during serialization. The B-Tree remains structurally intact, while the executor's traversal logic will simply bypass flagged records, offering O(1) delete execution times.
                        </p>
                    </div>
                </div>
            </section>

        </div>
    );
}
