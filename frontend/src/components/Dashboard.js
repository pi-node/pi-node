// frontend/src/components/Dashboard.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Dashboard.css'; // Import styles for the dashboard

const Dashboard = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await axios.get('/api/data'); // Adjust the endpoint as needed
                setData(response.data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return <div className="loading">Loading data...</div>; // Loading state
    }

    if (error) {
        return <div className="error">Error: {error}</div>; // Error state
    }

    return (
        <div className="dashboard">
            <h2>Dashboard</h2>
            <div className="data-container">
                {data.length > 0 ? (
                    data.map((item, index) => (
                        <div key={index} className="data-item">
                            <h3>{item.title || item.name}</h3>
                            <p>{item.description || item.details}</p>
                            {/* Add more fields as necessary */}
                        </div>
                    ))
                ) : (
                    <p>No data available.</p>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
