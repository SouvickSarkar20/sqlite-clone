import { Check, X, Loader2, Circle } from 'lucide-react';

export default function ExecutionStepper({ steps }) {
    if (!steps || steps.length === 0) return null;

    return (
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem' }}>
                Execution Progress
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginTop: '0.5rem' }}>
                {steps.map((step, index) => (
                    <div key={index} className="step-item" style={{ animationDelay: `${index * 0.1}s` }}>
                        <div className={`step-icon ${step.status}`}>
                            {step.status === 'success' && <Check size={14} color="#000" />}
                            {step.status === 'error' && <X size={14} color="#000" />}
                            {step.status === 'running' && <Loader2 size={14} color="#fff" className="spin" />}
                            {step.status === 'pending' && <Circle size={10} color="var(--muted-foreground)" />}
                        </div>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                            <span style={{ fontWeight: 500, color: step.status === 'error' ? 'var(--error)' : 'inherit' }}>
                                {step.action}
                            </span>
                            {step.details && (
                                <div style={{
                                    fontSize: '0.85rem',
                                    color: 'var(--muted-foreground)',
                                    background: 'rgba(0,0,0,0.3)',
                                    padding: '0.5rem',
                                    borderRadius: '4px',
                                    fontFamily: 'monospace',
                                    whiteSpace: 'pre-wrap',
                                    wordBreak: 'break-all'
                                }}>
                                    {typeof step.details === 'string' ? step.details : JSON.stringify(step.details, null, 2)}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
