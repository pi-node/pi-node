// frontend/src/index.js

import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import App from './App';
import * as serviceWorker from './serviceWorker';
import './index.css'; // Import global styles

// Render the application
ReactDOM.render(
    <Router>
        <App />
    </Router>,
    document.getElementById('root')
);

// Register the service worker for offline capabilities
serviceWorker.register();
