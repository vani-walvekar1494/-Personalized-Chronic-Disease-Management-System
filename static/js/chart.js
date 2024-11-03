import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

const SymptomChart = () => {
  const chartRef = useRef(null);
  const dataRef = useRef(null);

  useEffect(() => {
    // Fetch symptom data from the backend
    const fetchData = async () => {
      const response = await fetch('/get_symptom_data');
      const data = await response.json();

      // Extract dates and severities for the chart
      const dates = data.map((entry) => entry.date);
      const severities = data.map((entry) => entry.severity);

      // Create chart if it doesn't exist
      if (dataRef.current) dataRef.current.destroy(); // Destroy existing chart instance if any

      // Create new chart instance
      dataRef.current = new Chart(chartRef.current, {
        type: 'line',
        data: {
          labels: dates,
          datasets: [
            {
              label: 'Symptom Severity',
              data: severities,
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderWidth: 2,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    };

    fetchData();

    return () => {
      // Cleanup: Destroy the chart instance when component unmounts
      if (dataRef.current) dataRef.current.destroy();
    };
  }, []);

  return (
    <div>
      <h2>Symptom Severity Over Time</h2>
      <canvas ref={chartRef} />
    </div>
  );
};

export default SymptomChart;
