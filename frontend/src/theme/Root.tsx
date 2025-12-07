import React from 'react';
import { AuthProvider } from '../context/AuthContext';
import Chatbot from '../components/Chatbot';
import SelectionTooltip from '../components/SelectionTooltip';

// Default implementation, that you can customize
export default function Root({ children }) {
    return (
        <AuthProvider>
            {children}
            <SelectionTooltip />
            <Chatbot />
        </AuthProvider>
    );
}
