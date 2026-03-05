import { Database, Github } from 'lucide-react';
import { NavLink } from 'react-router-dom';

export default function Navbar() {
    return (
        <nav style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '1.25rem 2rem',
            marginBottom: '3rem',
            background: 'rgba(10, 10, 13, 0.8)',
            backdropFilter: 'blur(16px)',
            WebkitBackdropFilter: 'blur(16px)',
            borderBottom: '1px solid var(--border)',
            position: 'sticky',
            top: 0,
            zIndex: 50,
            borderRadius: '0 0 16px 16px',
            margin: '0 -1.5rem 3rem -1.5rem'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div style={{ background: 'linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%)', padding: '0.4rem', borderRadius: '10px', boxShadow: '0 0 15px rgba(37,99,235,0.4)' }}>
                    <Database color="#fff" size={20} />
                </div>
                <div>
                    <h1 style={{ fontSize: '1.25rem', fontWeight: 700, letterSpacing: '-0.5px', margin: 0, lineHeight: 1 }}>SQLite Clone</h1>
                </div>
            </div>

            <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
                <div style={{ display: 'flex', gap: '1.5rem', background: 'rgba(255,255,255,0.03)', padding: '0.35rem 0.5rem', borderRadius: '9999px', border: '1px solid var(--border)' }}>
                    <NavLink
                        to="/"
                        style={({ isActive }) => ({
                            textDecoration: 'none',
                            padding: '0.4rem 1.25rem',
                            borderRadius: '9999px',
                            color: isActive ? '#fff' : 'var(--muted-foreground)',
                            background: isActive ? 'rgba(255,255,255,0.1)' : 'transparent',
                            fontWeight: 500,
                            fontSize: '0.9rem',
                            transition: 'all 0.2s ease'
                        })}
                    >
                        Home
                    </NavLink>
                    <NavLink
                        to="/editor"
                        style={({ isActive }) => ({
                            textDecoration: 'none',
                            padding: '0.4rem 1.25rem',
                            borderRadius: '9999px',
                            color: isActive ? '#fff' : 'var(--muted-foreground)',
                            background: isActive ? 'rgba(255,255,255,0.1)' : 'transparent',
                            fontWeight: 500,
                            fontSize: '0.9rem',
                            transition: 'all 0.2s ease'
                        })}
                    >
                        Query Editor
                    </NavLink>
                </div>

                <a
                    href="https://github.com/SouvickSarkar20/sqlite-clone"
                    target="_blank"
                    rel="noreferrer"
                    className="btn btn-outline"
                    style={{ padding: '0.5rem 1rem', fontSize: '0.9rem' }}
                >
                    <Github size={16} />
                    GitHub
                </a>
            </div>
        </nav>
    );
}
