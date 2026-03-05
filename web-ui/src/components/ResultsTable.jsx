export default function ResultsTable({ data }) {
    if (!data || data.length === 0) return null;

    // Assuming data is an array of dicts, e.g., [{"values": [1, "alice", 25]}]
    // Since our simple DB just stores the raw values array, we'll format it basically.

    return (
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem' }}>
                Query Results ({data.length} rows)
            </h3>

            <div className="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            {/* For simplicity we just show columns based on the first row's structure */}
                            {data[0]?.values ? data[0].values.map((_, i) => <th key={i}>Column {i + 1}</th>) : <th>Data</th>}
                        </tr>
                    </thead>
                    <tbody>
                        {data.map((row, i) => (
                            <tr key={i}>
                                {row.values ? (
                                    row.values.map((val, cellIdx) => <td key={cellIdx}>{val}</td>)
                                ) : (
                                    <td>{JSON.stringify(row)}</td>
                                )}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
