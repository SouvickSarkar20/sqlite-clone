import { useState } from 'react';
import QueryEditor from '../components/QueryEditor';
import ExecutionStepper from '../components/ExecutionStepper';
import ResultsTable from '../components/ResultsTable';

export default function Editor() {
    const [query, setQuery] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [steps, setSteps] = useState([]);
    const [results, setResults] = useState(null);
    const [errorMsg, setErrorMsg] = useState('');

    const handleExecute = async () => {
        setIsLoading(true);
        setSteps([]);
        setResults(null);
        setErrorMsg('');

        // Create initial step
        const uiSteps = [{ action: 'Connecting to database engine', status: 'success' }];
        setSteps([...uiSteps]);

        try {
            // Simulate network delay for UI effect
            let currentSteps = [...uiSteps, { action: 'Sending query', status: 'running' }];
            setSteps([...currentSteps]);
            await new Promise(r => setTimeout(r, 400));

            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
            const response = await fetch(`${API_URL}/query`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sql: query })
            });

            const data = await response.json();

            // The backend returns step-by-step progress. 
            currentSteps[currentSteps.length - 1].status = 'success';
            currentSteps[currentSteps.length - 1].action = 'Query sent';

            if (data.steps && data.steps.length > 0) {
                // Add backend steps
                currentSteps = [...currentSteps, ...data.steps];
            } else if (data.status === 'error') {
                currentSteps.push({ action: 'Execution Failed', status: 'error', details: data.message });
            }

            setSteps(currentSteps);

            if (data.status === 'success') {
                if (data.data) {
                    setResults(data.data);
                } else {
                    // For INSERT/CREATE, just add a success step
                    setSteps(prev => [...prev, { action: data.message, status: 'success' }]);
                }
            } else {
                setErrorMsg(data.message);
            }

        } catch (e) {
            console.error(e);
            setErrorMsg("Failed to connect to the backend running on port 5000.");
            setSteps(prev => {
                const newSteps = [...prev];
                if (newSteps.length > 0 && newSteps[newSteps.length - 1].status === 'running') {
                    newSteps[newSteps.length - 1].status = 'error';
                }
                return [...newSteps, { action: 'Connection Error', status: 'error', details: e.message }];
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            <QueryEditor
                value={query}
                onChange={setQuery}
                onExecute={handleExecute}
                isLoading={isLoading}
            />

            <div style={{ display: 'grid', gridTemplateColumns: steps.length > 0 ? '300px 1fr' : '1fr', gap: '1.5rem', alignItems: 'start' }}>
                {steps.length > 0 && (
                    <div style={{ position: 'sticky', top: '2rem' }}>
                        <ExecutionStepper steps={steps} />
                    </div>
                )}

                <div style={{ width: '100%', overflow: 'hidden' }}>
                    {errorMsg && !steps.length && (
                        <div className="glass-panel" style={{ borderLeft: '4px solid var(--error)' }}>
                            <h3 style={{ color: 'var(--error)', marginBottom: '0.5rem' }}>Error</h3>
                            <p>{errorMsg}</p>
                        </div>
                    )}
                    {results && <ResultsTable data={results} />}
                </div>
            </div>
        </div>
    );
}
