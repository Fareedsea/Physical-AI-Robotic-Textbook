import React, { useEffect, useState } from 'react';
import styles from './styles.module.css';

export default function SelectionTooltip() {
    const [position, setPosition] = useState<{ top: number; left: number } | null>(null);
    const [selectedText, setSelectedText] = useState('');

    useEffect(() => {
        const handleMouseUp = () => {
            const selection = window.getSelection();
            if (!selection || selection.isCollapsed) {
                setPosition(null);
                setSelectedText('');
                return;
            }

            const text = selection.toString().trim();
            if (!text) {
                setPosition(null);
                return;
            }

            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();

            // Calculate position relative to viewport, adjusted for scroll
            setPosition({
                top: rect.top + window.scrollY - 40, // 40px above selection
                left: rect.left + window.scrollX + (rect.width / 2),
            });
            setSelectedText(text);
        };

        const handleMouseDown = () => {
            // Hide immediately on new click
            // setPosition(null); 
        };

        document.addEventListener('mouseup', handleMouseUp);
        document.addEventListener('mousedown', handleMouseDown);

        return () => {
            document.removeEventListener('mouseup', handleMouseUp);
            document.removeEventListener('mousedown', handleMouseDown);
        };
    }, []);

    const handleAskAI = () => {
        // Dispatch custom event for Chatbot to listen to
        const event = new CustomEvent('ASK_AI_SELECTION', {
            detail: { text: selectedText }
        });
        window.dispatchEvent(event);
        setPosition(null);

        // Clear selection
        window.getSelection()?.removeAllRanges();
    };

    if (!position) return null;

    return (
        <div
            className={styles.tooltip}
            style={{ top: position.top, left: position.left }}
            onClick={handleAskAI}
        >
            Ask AI ✨
        </div>
    );
}
