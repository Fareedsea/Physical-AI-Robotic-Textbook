import React from 'react';
import Layout from '@theme/Layout';

export default function Home(): JSX.Element {
  return (
    <Layout
      title="Home"
      description="Physical AI Robotic Textbook">
      <main style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '50vh',
        fontSize: '1.5rem',
      }}>
        <p>Physical AI Robotic Textbook - Under Construction</p>
      </main>
    </Layout>
  );
}
