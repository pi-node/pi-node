// frontend/src/components/WrappedPiToken.js

import React, { useState } from 'react';
import { ethers } from 'ethers';
import WrappedPiTokenABI from './WrappedPiTokenABI.json'; // Import the ABI of the Wrapped Pi Token contract
import './WrappedPiToken.css'; // Import styles for the component

const WrappedPiToken = ({ contractAddress }) => {
    const [amount, setAmount] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');

    const handleInputChange = (e) => {
        setAmount(e.target.value);
        setError(null); // Reset error on input change
        setSuccessMessage(''); // Reset success message on input change
    };

    const wrapTokens = async () => {
        if (!amount || isNaN(amount) || amount <= 0) {
            setError('Please enter a valid amount.');
            return;
        }

        setLoading(true);
        setError(null);
        setSuccessMessage('');

        try {
            const provider = new ethers.providers.Web3Provider(window.ethereum);
            const signer = provider.getSigner();
            const contract = new ethers.Contract(contractAddress, WrappedPiTokenABI, signer);

            // Approve the contract to spend Pi tokens
            const piTokenAddress = 'YOUR_PI_TOKEN_ADDRESS'; // Replace with your Pi token contract address
            const piTokenContract = new ethers.Contract(piTokenAddress, WrappedPiTokenABI, signer);
            const approvalTx = await piTokenContract.approve(contractAddress, ethers.utils.parseUnits(amount, 18));
            await approvalTx.wait();

            // Wrap the tokens
            const tx = await contract.wrap(ethers.utils.parseUnits(amount, 18));
            await tx.wait();

            setSuccessMessage('Tokens wrapped successfully!');
            setAmount('');
        } catch (err) {
            console.error(err);
            setError('An error occurred while wrapping tokens. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const unwrapTokens = async () => {
        if (!amount || isNaN(amount) || amount <= 0) {
            setError('Please enter a valid amount.');
            return;
        }

        setLoading(true);
        setError(null);
        setSuccessMessage('');

        try {
            const provider = new ethers.providers.Web3Provider(window.ethereum);
            const signer = provider.getSigner();
            const contract = new ethers.Contract(contractAddress, WrappedPiTokenABI, signer);

            // Unwrap the tokens
            const tx = await contract.unwrap(ethers.utils.parseUnits(amount, 18));
            await tx.wait();

            setSuccessMessage('Tokens unwrapped successfully!');
            setAmount('');
        } catch (err) {
            console.error(err);
            setError('An error occurred while unwrapping tokens. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="wrapped-pi-token">
            <h2>Wrap/Unwrap Pi Tokens</h2>
            <input
                type="number"
                value={amount}
                onChange={handleInputChange}
                placeholder="Amount"
                min="0"
                step="any"
            />
            <div className="button-group">
                <button onClick={wrapTokens} disabled={loading}>
                    {loading ? 'Wrapping...' : 'Wrap Tokens'}
                </button>
                <button onClick={unwrapTokens} disabled={loading}>
                    {loading ? 'Unwrapping...' : 'Unwrap Tokens'}
                </button>
            </div>
            {error && <div className="error">{error}</div>}
            {successMessage && <div className="success">{successMessage}</div>}
        </div>
    );
};

export default WrappedPiToken;
