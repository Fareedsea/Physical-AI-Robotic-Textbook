import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function TranslateButton(): JSX.Element {
    const [isTranslated, setIsTranslated] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleTranslate = async () => {
        setLoading(true);
        // Simulate API call to backend for translation
        // In a real implementation, this would fetch the Urdu markdown or replace text nodes.
        setTimeout(() => {
            setIsTranslated(!isTranslated);
            setLoading(false);
            if (!isTranslated) {
                alert('Translating content to Urdu... (Simulation: Content would actially change here)');
            } else {
                alert('Reverting content to English...');
            }
        }, 1000);
    };

    return (
        <div className={styles.container}>
            <button
                className={clsx('button', 'button--sm', isTranslated ? 'button--warning' : 'button--outline button--primary', styles.translateBtn)}
                onClick={handleTranslate}
                disabled={loading}
            >
                {loading ? (
                    <span className={styles.spinner}>Translating...</span>
                ) : isTranslated ? (
                    <>
                        <span className={styles.icon}>اردو</span> View in English
                    </>
                ) : (
                    <>
                        <span className={styles.icon}>A/文</span> Translate to Urdu
                    </>
                )}
            </button>
            {isTranslated && (
                <span className={styles.badge} dir="rtl">
                    اردو ترجمہ فعال ہے (Urdu Translation Active)
                </span>
            )}
        </div>
    );
}
