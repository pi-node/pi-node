// src/Dashboard.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2'; // Importing a charting library for visualization
import './Dashboard.css'; // Importing CSS for styling

const Dashboard = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [refreshInterval, setRefreshInterval] = useState(5000); // Refresh every 5 seconds

    const fetchData = async () => {
        try {
            const result = await axios('/api/metrics');
            setData(result.data);
            setLoading(false);
        } catch (err) {
            setError('Error fetching data');
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, refreshInterval);
        return () => clearInterval(interval); // Cleanup on unmount
    }, [refreshInterval]);

    // Prepare data for charting
    const chartData = {
        labels: data.map(item => item.metricName),
        datasets: [
            {
                label: 'Metric Values',
                data: data.map(item => item.value),
                fill: false,
                backgroundColor: 'rgba(75,192,192,0.4)',
                borderColor: 'rgba(75,192,192,1)',
            },
        ],
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="dashboard">
            <h1>Real-Time Analytics</h1>
            <Line data={chartData} />
            <ul>
                {data.map(item => (
                    <li key={item.id}>{item.metricName}: {item.value}</li>
                ))}
            </ul>
            <button onClick={fetchData}>Refresh Now</button>
            <label>
                Refresh Interval (ms):
                <input
                    type="number"
                    value={refreshInterval}
                    onChange={(e) => setRefreshInterval(e.target.value)}
                />
            </label>
        </div>
    );
};

export default Dashboard;
