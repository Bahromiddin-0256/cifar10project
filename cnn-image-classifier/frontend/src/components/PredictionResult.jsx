import React from 'react';
import { CheckCircle, Clock, TrendingUp } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const PredictionResult = ({ result }) => {
  if (!result) return null;

  const chartData = Object.entries(result.probabilities).map(([name, value]) => ({
    name,
    probability: value
  }));

  const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6',
                  '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'];

  return (
    <div className="prediction-result">
      <div className="result-header">
        <h2>
          <CheckCircle className="icon-success" />
          Natija
        </h2>
      </div>

      <div className="result-main">
        <div className="predicted-class">
          <h3>Bashorat qilingan sinf:</h3>
          <div className="class-badge">
            {result.predicted_class}
          </div>
        </div>

        <div className="confidence-score">
          <h4>
            <TrendingUp size={20} />
            Ishonch darajasi
          </h4>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{ width: `${result.confidence}%` }}
            />
          </div>
          <p className="confidence-text">{result.confidence.toFixed(2)}%</p>
        </div>

        <div className="processing-time">
          <Clock size={16} />
          <span>Qayta ishlash vaqti: {result.processing_time.toFixed(3)}s</span>
        </div>
      </div>

      <div className="probabilities-chart">
        <h4>Barcha sinflar ehtimolliklari:</h4>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData} layout="horizontal">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" domain={[0, 100]} />
            <YAxis dataKey="name" type="category" width={100} />
            <Tooltip
              formatter={(value) => `${value.toFixed(2)}%`}
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '1px solid #e5e7eb',
                borderRadius: '8px'
              }}
            />
            <Bar dataKey="probability" radius={[0, 4, 4, 0]}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PredictionResult;
