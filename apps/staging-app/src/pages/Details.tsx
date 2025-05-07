import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

interface ProjectionResponse {
  changeset_id: string;
  record_id: string;
  projection: Record<string, any>;
}

export default function Details() {
  const { changeset_id, record_id } = useParams<{ changeset_id: string; record_id: string }>();
  const [data, setData] = useState<ProjectionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProjection = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:8000/api/v1/staging/changeset/${changeset_id}/record/${record_id}/projection`
        );
        if (!res.ok) throw new Error(await res.text());
        const json = await res.json();
        setData(json);
      } catch (err: any) {
        setError(err.message || 'Unknown error');
      }
    };

    if (changeset_id && record_id) {
      fetchProjection();
    }
  }, [changeset_id, record_id]);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Details for Record</h2>
      <p><strong>Changeset:</strong> {changeset_id}</p>
      <p><strong>Record ID:</strong> {record_id}</p>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {data && (
        <pre
          style={{
            background: '#f0f0f0',
            padding: '1rem',
            borderRadius: '4px',
            overflowX: 'auto',
            marginTop: '1rem'
          }}
        >
          {JSON.stringify(data.projection, null, 2)}
        </pre>
      )}
    </div>
  );
}