import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useAuth } from '../context/AuthContext';
import styles from './signup.module.css';

export default function Signup(): JSX.Element {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        softwareBg: 'beginner',
        hardwareBg: 'none'
    });
    const { signup } = useAuth();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.id]: e.target.value });
    };

    const handleSignup = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError('');

        try {
            await signup({
                name: formData.name,
                email: formData.email,
                softwareBg: formData.softwareBg,
                hardwareBg: formData.hardwareBg,
                progress: 0
            });
            alert('Account Created! Personalization data saved.');
            window.location.href = '/Physical-AI-Robotic-Textbook/dashboard';
        } catch (err: any) {
            setError('Signup failed. Please try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Layout title="Sign Up" description="Create an account for Physical AI Robotic Textbook">
            <div className={styles.signupContainer}>
                <div className={styles.signupCard}>
                    <h1 className={styles.title}>Create Account</h1>
                    <p className={styles.subtitle}>Join the future of robotics engineering.</p>

                    <form onSubmit={handleSignup} className={styles.form}>
                        <div className={styles.inputGroup}>
                            <label htmlFor="name">Full Name</label>
                            <input
                                type="text"
                                id="name"
                                value={formData.name}
                                onChange={handleChange}
                                required
                                placeholder="John Doe"
                                className={styles.input}
                            />
                        </div>

                        <div className={styles.inputGroup}>
                            <label htmlFor="email">Email Address</label>
                            <input
                                type="email"
                                id="email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                                placeholder="name@example.com"
                                className={styles.input}
                            />
                        </div>

                        <div className={styles.inputGroup}>
                            <label htmlFor="password">Password</label>
                            <input
                                type="password"
                                id="password"
                                value={formData.password}
                                onChange={handleChange}
                                required
                                placeholder="••••••••"
                                className={styles.input}
                            />
                        </div>

                        <div className={styles.row}>
                            <div className={styles.inputGroup}>
                                <label htmlFor="softwareBg">Software Background</label>
                                <select
                                    id="softwareBg"
                                    value={formData.softwareBg}
                                    onChange={handleChange}
                                    className={styles.select}
                                >
                                    <option value="beginner">Beginner (No coding)</option>
                                    <option value="intermediate">Intermediate (Python/C++)</option>
                                    <option value="advanced">Advanced (ROS/AI)</option>
                                </select>
                            </div>

                            <div className={styles.inputGroup}>
                                <label htmlFor="hardwareBg">Hardware Background</label>
                                <select
                                    id="hardwareBg"
                                    value={formData.hardwareBg}
                                    onChange={handleChange}
                                    className={styles.select}
                                >
                                    <option value="none">None</option>
                                    <option value="arduino">Arduino/Raspberry Pi</option>
                                    <option value="robotics">Robotics/Mechatronics</option>
                                </select>
                            </div>
                        </div>

                        <div className={styles.infoBox}>
                            <p>We use your background to personalize the difficulty of the textbook content.</p>
                        </div>

                        {error && <div className={styles.errorMessage}>{error}</div>}

                        <button type="submit" className={styles.submitButton} disabled={isSubmitting}>
                            {isSubmitting ? 'Creating Account...' : 'Sign Up'}
                        </button>
                    </form>

                    <div className={styles.footer}>
                        <p>Already have an account? <Link to="/login">Sign in</Link></p>
                    </div>
                </div>
            </div>
        </Layout>
    );
}
