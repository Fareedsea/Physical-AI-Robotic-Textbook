import React, { useEffect } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import clsx from 'clsx';
import { useAuth } from '../context/AuthContext';
import styles from './dashboard.module.css';

export default function Dashboard(): JSX.Element {
    const { user, loading, logout } = useAuth();

    useEffect(() => {
        if (!loading && !user) {
            // Redirect to login if not authenticated
            window.location.href = '/Physical-AI-Robotic-Textbook/login';
        }
    }, [user, loading]);

    if (loading || !user) {
        return (
            <Layout title="Dashboard">
                <div className={styles.loadingContainer}>
                    <div className={styles.spinner}></div>
                    <p>Initializing Command Center...</p>
                </div>
            </Layout>
        );
    }

    // Calculate initials
    const initials = user.name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);

    return (
        <Layout title="Dashboard" description="User Command Center">
            <div className={styles.dashboardContainer}>
                <div className="container">
                    <header className={styles.dashboardHeader}>
                        <div>
                            <h1 className={styles.greeting}>Command Center</h1>
                            <p className={styles.status}>System Status: <span className={styles.online}>ONLINE</span></p>
                        </div>
                        <div className={styles.profileBadge}>
                            <div className={styles.avatar}>{initials}</div>
                            <div>
                                <strong>{user.name}</strong>
                                <span className={styles.role}>Cadet</span>
                            </div>
                        </div>
                    </header>

                    <div className="row">
                        {/* Progress Section */}
                        <div className="col col--8">
                            <div className={styles.card}>
                                <h3 className={styles.cardTitle}>Mission Progress</h3>
                                <div className={styles.progressBarContainer}>
                                    <div
                                        className={styles.progressBar}
                                        style={{ width: `${user.progress}%` }}
                                    ></div>
                                </div>
                                <p className={styles.progressText}>{user.progress}% Complete</p>

                                <div className={styles.moduleList}>
                                    <div className={clsx(styles.moduleItem, styles.completed)}>
                                        <span className={styles.moduleStatus}>✓</span>
                                        <span>Module 0: Orientation</span>
                                    </div>
                                    <div className={clsx(styles.moduleItem, styles.active)}>
                                        <span className={styles.moduleStatus}>►</span>
                                        <span>Module 1: The Robotic Nervous System (ROS 2)</span>
                                        <Link to="/docs/intro" className="button button--primary button--sm margin-left--md">Resume</Link>
                                    </div>
                                    <div className={clsx(styles.moduleItem, styles.locked)}>
                                        <span className={styles.moduleStatus}>🔒</span>
                                        <span>Module 2: The Digital Twin</span>
                                    </div>
                                    <div className={clsx(styles.moduleItem, styles.locked)}>
                                        <span className={styles.moduleStatus}>🔒</span>
                                        <span>Module 3: The AI-Robot Brain</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Sidebar Stats */}
                        <div className="col col--4">
                            <div className={styles.card}>
                                <h3 className={styles.cardTitle}>Operative Profile</h3>
                                <ul className={styles.statsList}>
                                    <li>
                                        <strong>Software Clearance:</strong>
                                        <span className={styles.tag}>{user.softwareBg}</span>
                                    </li>
                                    <li>
                                        <strong>Hardware Access:</strong>
                                        <span className={styles.tag}>{user.hardwareBg}</span>
                                    </li>
                                </ul>
                            </div>

                            <div className={clsx(styles.card, 'margin-top--md')}>
                                <h3 className={styles.cardTitle}>Quick Actions</h3>
                                <div className={styles.actionButtons}>
                                    <button className="button button--secondary button--block margin-bottom--sm">
                                        Access Terminal
                                    </button>
                                    <button
                                        className="button button--danger button--outline button--block"
                                        onClick={logout}
                                    >
                                        Log Out
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
}
