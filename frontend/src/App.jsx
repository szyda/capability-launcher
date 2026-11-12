import { useEffect, useMemo, useState } from 'react';
import { fetchCapabilities, runCapability } from './api';

function App() {
  const [capabilities, setCapabilities] = useState([]);
  const [selectedId, setSelectedId] = useState('');
  const [formValues, setFormValues] = useState({});
  const [loadingCapabilities, setLoadingCapabilities] = useState(true);
  const [runningCapability, setRunningCapability] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadCapabilities() {
      try {
        setError('');
        const data = await fetchCapabilities();

        if (data.length === 0) {
          setCapabilities([]);
          setSelectedId('');
          setFormValues({});
          return;
        }

        setCapabilities(data);
        setSelectedId(data[0].id);
        setFormValues(buildInitialValues(data[0].inputs || []));
      } catch (loadError) {
        setError(loadError.message);
      } finally {
        setLoadingCapabilities(false);
      }
    }

    loadCapabilities();
  }, []);

  const selectedCapability = useMemo(
    () => capabilities.find((capability) => capability.id === selectedId) || null,
    [capabilities, selectedId]
  );

  useEffect(() => {
    if (!selectedCapability) {
      return;
    }

    setResult(null);
    setError('');
    setFormValues(buildInitialValues(selectedCapability.inputs || []));
  }, [selectedCapability]);

  function buildInitialValues(fields) {
    return (fields || []).reduce((acc, field) => {
      const defaultValue = field.default ?? (field.type === 'checkbox' ? false : '');
      acc[field.name] = defaultValue;
      return acc;
    }, {});
  }

  function handleFieldChange(name, value) {
    setFormValues((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (!selectedCapability) {
      return;
    }

    setRunningCapability(true);
    setError('');
    setResult(null);

    try {
      const payload = await runCapability(selectedCapability.id, formValues);
      setResult(payload);
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setRunningCapability(false);
    }
  }

  function renderField(field) {
    const value = formValues[field.name] ?? '';

    switch (field.type) {
      case 'textarea':
        return (
          <textarea
            key={field.name}
            id={field.name}
            value={value}
            onChange={(event) => handleFieldChange(field.name, event.target.value)}
            rows={6}
          />
        );
      case 'number':
        return (
          <input
            key={field.name}
            id={field.name}
            type="number"
            value={value}
            onChange={(event) => handleFieldChange(field.name, Number(event.target.value))}
          />
        );
      case 'checkbox':
        return (
          <label key={field.name} className="checkbox-row">
            <input
              id={field.name}
              type="checkbox"
              checked={Boolean(value)}
              onChange={(event) => handleFieldChange(field.name, event.target.checked)}
            />
            <span>{field.label}</span>
          </label>
        );
      case 'select':
        return (
          <select
            key={field.name}
            id={field.name}
            value={value}
            onChange={(event) => handleFieldChange(field.name, event.target.value)}
          >
            {field.options?.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        );
      case 'text':
      default:
        return (
          <input
            key={field.name}
            id={field.name}
            type="text"
            value={value}
            onChange={(event) => handleFieldChange(field.name, event.target.value)}
          />
        );
    }
  }

  const resultData = result?.result ?? result;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-header">
          <p className="eyebrow">Launcher</p>
          <h2>Capabilities</h2>
        </div>

        {loadingCapabilities ? (
          <p className="sidebar-empty">Loading...</p>
        ) : capabilities.length === 0 ? (
          <p className="sidebar-empty">No capabilities found.</p>
        ) : (
          capabilities.map((capability) => (
            <button
              key={capability.id}
              type="button"
              className={selectedId === capability.id ? 'capability-button selected' : 'capability-button'}
              onClick={() => setSelectedId(capability.id)}
            >
              <span className="capability-name">{capability.name}</span>
              <span className="capability-id">{capability.id}</span>
            </button>
          ))
        )}
      </aside>

      <main className="main-panel">
        {selectedCapability ? (
          <form onSubmit={handleSubmit} className="capability-form">
            <div className="header-block">
              <p className="eyebrow">Capability</p>
              <h1>{selectedCapability.name}</h1>
              <p>{selectedCapability.description}</p>
            </div>

            <div className="meta-row">
              <span>Version {selectedCapability.version || '1.0.0'}</span>
              <span>{selectedCapability.inputs?.length || 0} inputs</span>
            </div>

            {selectedCapability.inputs?.map((field) => (
              <div key={field.name} className="field-row">
                <label htmlFor={field.name}>{field.label}</label>
                {renderField(field)}
              </div>
            ))}

            <button type="submit" disabled={runningCapability}>
              {runningCapability ? 'Running...' : 'Run capability'}
            </button>
          </form>
        ) : (
          <div className="empty-panel">
            <h2>No capability selected</h2>
            <p>The API did not return any capabilities yet.</p>
          </div>
        )}

        {error && <div className="message error">{error}</div>}

        {result && (
          <div className="result-panel">
            <div className="result-header">
              <h3>Result</h3>
              <span className="status-badge">{result.status}</span>
            </div>
            <pre>{JSON.stringify(resultData, null, 2)}</pre>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
