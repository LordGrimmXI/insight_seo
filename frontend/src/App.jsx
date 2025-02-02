import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [seoData, setSeoData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeSEO = async () => {
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      setError('Please enter a valid URL starting with http:// or https://');
      return;
    }

    setLoading(true);
    setError(null);
    setSeoData(null);

    try {
      const response = await axios.post('http://localhost:5000/analyze', { url });
      setSeoData(response.data);
    } catch (error) {
      console.error('Error analyzing SEO:', error);
      setError("Error analyzing the URL. Please check it and try again.");
    } finally {
      setLoading(false);
    }
  };

  const getColorForMetric = (metric) => {
    switch (metric) {
      case 'SLOW':
        return 'red';
      case 'AVERAGE':
        return 'yellow';
      case 'GOOD':
        return 'green';
      default:
        return 'black';
    }
  };

  return (
    <div className="app-container">
      <h1>Insight SEO</h1>
      <div className="input-area">
        <input
          type="text"
          placeholder="Enter website URL (e.g., https://www.youtube.com)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="url-input"
        />
        <button onClick={analyzeSEO} disabled={loading} className="analyze-button">
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}

      {seoData && (
        <div className="results-area">
          <h2>Analysis Results</h2>
          <pre className="seo-data">{JSON.stringify(seoData, null, 2)}</pre>

          {seoData.page_speed && seoData.page_speed.lighthouse_metrics && (
            <>
              <h3 style={{ color: 'black' }}>PageSpeed Insights:</h3>
              <table className="seo-table">
                <thead>
                  <tr>
                    <th>Metric</th>
                    <th>Value</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(seoData.page_speed.lighthouse_metrics).map(([metric, value]) => (
                    <tr key={metric}>
                      <td>{metric}</td>
                      <td>{value || 'Not available'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}

          {seoData.page_speed && seoData.page_speed.crux_metrics && (
            <>
              <h3 style={{ color: 'black' }}>CrUX Metrics:</h3>
              <table className="seo-table">
                <thead>
                  <tr>
                    <th>Metric</th>
                    <th>Value</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(seoData.page_speed.crux_metrics).map(([metric, value]) => (
                    <tr key={metric}>
                      <td>{metric}</td>
                      <td style={{ color: getColorForMetric(value) }}>{value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
