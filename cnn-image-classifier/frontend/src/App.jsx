import React, { useState, useEffect } from 'react';
import { Brain, Info, History, Trash2, AlertCircle } from 'lucide-react';
import ImageUpload from './components/ImageUpload';
import PredictionResult from './components/PredictionResult';
import { apiService } from './services/api';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    loadModelInfo();
    loadHistory();
  }, []);

  const loadModelInfo = async () => {
    try {
      const info = await apiService.getModelInfo();
      setModelInfo(info);
    } catch (err) {
      console.error('Model info yuklashda xatolik:', err);
    }
  };

  const loadHistory = async () => {
    try {
      const data = await apiService.getHistory();
      setHistory(data.history);
    } catch (err) {
      console.error('Tarixni yuklashda xatolik:', err);
    }
  };

  const handlePredict = async (file) => {
    setLoading(true);
    setError(null);

    try {
      const result = await apiService.predictImage(file);
      setPrediction(result);
      await loadHistory();
    } catch (err) {
      setError(err.response?.data?.detail || 'Xatolik yuz berdi');
      console.error('Bashorat qilishda xatolik:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    if (window.confirm('Tarixni tozalashni xohlaysizmi?')) {
      try {
        await apiService.clearHistory();
        setHistory([]);
      } catch (err) {
        console.error('Tarixni tozalashda xatolik:', err);
      }
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <Brain size={32} />
            <h1>CNN Tasvir Klassifikatori</h1>
          </div>
          {modelInfo && (
            <div className="model-badge">
              <Info size={16} />
              <span>Accuracy: {(modelInfo.accuracy * 100).toFixed(2)}%</span>
            </div>
          )}
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          {error && (
            <div className="error-message">
              <AlertCircle size={20} />
              <span>{error}</span>
            </div>
          )}

          <div className="main-grid">
            <div className="upload-section">
              <h2>Rasm yuklash</h2>
              <ImageUpload onPredict={handlePredict} loading={loading} />
            </div>

            <div className="result-section">
              {prediction ? (
                <PredictionResult result={prediction} />
              ) : (
                <div className="empty-state">
                  <Brain size={64} className="empty-icon" />
                  <p>Natijalar bu yerda ko'rsatiladi</p>
                  <p className="empty-hint">Rasmni yuklang va klassifikatsiya qiling</p>
                </div>
              )}
            </div>
          </div>

          <div className="history-section">
            <div className="history-header">
              <h2>
                <History size={24} />
                Bashoratlar tarixi ({history.length})
              </h2>
              <div className="history-actions">
                <button
                  className="btn-secondary"
                  onClick={() => setShowHistory(!showHistory)}
                >
                  {showHistory ? 'Yashirish' : 'Ko\'rsatish'}
                </button>
                {history.length > 0 && (
                  <button
                    className="btn-danger"
                    onClick={handleClearHistory}
                  >
                    <Trash2 size={16} />
                    Tozalash
                  </button>
                )}
              </div>
            </div>

            {showHistory && history.length > 0 && (
              <div className="history-table-container">
                <table className="history-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Vaqt</th>
                      <th>Fayl</th>
                      <th>Sinf</th>
                      <th>Ishonch</th>
                    </tr>
                  </thead>
                  <tbody>
                    {history.slice().reverse().map((item, index) => (
                      <tr key={index}>
                        <td>{history.length - index}</td>
                        <td>{new Date(item.timestamp).toLocaleString('uz-UZ')}</td>
                        <td className="filename">{item.filename}</td>
                        <td>
                          <span className="class-tag">{item.predicted_class}</span>
                        </td>
                        <td>
                          <span className="confidence-badge">
                            {item.confidence.toFixed(2)}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>© 2024 CNN Image Classifier | FastAPI + React</p>
      </footer>
    </div>
  );
}

export default App;
