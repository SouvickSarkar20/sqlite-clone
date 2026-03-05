import { Play } from 'lucide-react';

export default function QueryEditor({ value, onChange, onExecute, isLoading }) {
  return (
    <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <textarea 
        className="input-area"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Type your SQL query here... (e.g. CREATE TABLE users (id, name, age) or SELECT * FROM users)"
        spellCheck={false}
      />
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <button 
          className="btn-primary" 
          onClick={onExecute}
          disabled={!value.trim() || isLoading}
        >
          <Play size={18} />
          {isLoading ? 'Executing...' : 'Run Query'}
        </button>
      </div>
    </div>
  );
}
