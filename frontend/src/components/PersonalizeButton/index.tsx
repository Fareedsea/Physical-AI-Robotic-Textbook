import React, { useState } from 'react';
import clsx from 'clsx';
import { useAuth } from '../../context/AuthContext';
import styles from './styles.module.css';

export default function PersonalizeButton(): JSX.Element {
    const { user } = useAuth();
    const [isPersonalized, setIsPersonalized] = useState(false);
    const [loading, setLoading] = useState(false);

    // If no user is logged in, or they haven't set a background, we might hide this or show a prompt.
    // For now, we'll show it but it might prompt to login.

    const handlePersonalize = async () => {
        if (!user) {
            alert('Please login to use Personalization features.');
            window.location.href = '/Physical-AI-Robotic-Textbook/login';
            return;
        }

        setLoading(true);
        // Simulate API call to backend
        setTimeout(() => {
            setIsPersonalized(!isPersonalized);
            setLoading(false);
            if (!isPersonalized) {
                alert(`Content Personalized for:\nSoftware: ${user.softwareBg}\nHardware: ${user.hardwareBg}`);
            } else {
                alert('Content Reset to Standard View');
            }
        }, 1500);
    };

    return (
        <div className={styles.container}>
            <button
                className={clsx('button', 'button--sm', isPersonalized ? 'button--success' : 'button--secondary', styles.personalizeBtn)}
                onClick={handlePersonalize}
                disabled={loading}
            >
                {loading ? (
                    <span className={styles.spinner}>Processing...</span>
                ) : isPersonalized ? (
                    <>
                        <span className={styles.icon}>✨</span> Personalized Mode Active
                    </>
                ) : (
                    <>
                        <span className={styles.icon}>⚡</span> Personalize for Me
                    </>
                )}
            </button>
            {isPersonalized && (
                <span className={styles.badge}>
                    Adapted for {user?.softwareBg} / {user?.hardwareBg}
                </span>
            )}
        </div>
    );
}
