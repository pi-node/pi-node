// frontend/src/App.js

import React, { useState, useEffect } from 'react';
import { Route, Switch } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import NotFound from './components/NotFound';
import Header from './components/Header';
import Footer from './components/Footer';
import { DataProvider } from './context/DataContext';
import ErrorBoundary from './components/ErrorBoundary';
import './App.css'; // Import global styles

const App = () => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Simulate loading data or performing an initial fetch
        const fetchData = async () => {
            // Simulate a delay
            await new Promise((resolve) => setTimeout(resolve, 1000));
            setLoading(false);
        };

        fetchData();
    }, []);

    if (loading) {
        return <div className="loading">Loading...</div>; // Loading state
    }

    return (
        <DataProvider>
            <div className="app-container">
                <Header />
                <main>
                    <ErrorBoundary>
                        <Switch>
                            <Route exact path="/" component={Dashboard} />
                            <Route component={NotFound} />
                        </Switch>
                    </ErrorBoundary>
                </main>
                <Footer />
            </div>
        </DataProvider>
    );
};

export default App;
