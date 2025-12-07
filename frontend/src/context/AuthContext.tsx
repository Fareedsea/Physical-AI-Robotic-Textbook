import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Define User Interface
export interface User {
    name: string;
    email: string;
    softwareBg: string;
    hardwareBg: string;
    progress: number;
}

// Define Context Interface
interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    loading: boolean;
    login: (email: string) => Promise<void>;
    signup: (data: User) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Default User for simulation
const MOCK_USER: User = {
    name: 'Robotics Engineer',
    email: 'demo@example.com',
    softwareBg: 'Intermediate',
    hardwareBg: 'Arduino',
    progress: 15,
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check local storage for persisted session simulation
        const storedUser = localStorage.getItem('physical_ai_user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    const login = async (email: string) => {
        return new Promise<void>((resolve, reject) => {
            setTimeout(() => {
                // Mock validation
                if (email.includes('@')) {
                    const userData = { ...MOCK_USER, email };
                    setUser(userData);
                    localStorage.setItem('physical_ai_user', JSON.stringify(userData));
                    resolve();
                } else {
                    reject(new Error('Invalid email'));
                }
            }, 1000);
        });
    };

    const signup = async (data: User) => {
        return new Promise<void>((resolve) => {
            setTimeout(() => {
                const newUser = { ...data, progress: 0 };
                setUser(newUser);
                localStorage.setItem('physical_ai_user', JSON.stringify(newUser));
                resolve();
            }, 1500);
        });
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('physical_ai_user');
        window.location.href = '/Physical-AI-Robotic-Textbook/'; // Redirect to home
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated: !!user,
                loading,
                login,
                signup,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
