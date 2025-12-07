import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Start Learning ⏱️
          </Link>
          <Link
            className="button button--outline button--secondary button--lg margin-left--md"
            to="/docs/intro">
            Learn More
          </Link>
        </div>
      </div>
    </header>
  );
}

function Feature({ title, description }: { title: string, description: JSX.Element }) {
  return (
    <div className={clsx('col col--4')}>
      <div className="card padding--lg card--full-height">
        <div className="card__header">
          <Heading as="h3">{title}</Heading>
        </div>
        <div className="card__body">
          <p>{description}</p>
        </div>
      </div>
    </div>
  );
}

function HomepageFeatures(): JSX.Element {
  const FeatureList = [
    {
      title: 'The Future of Work',
      description: (
        <>
          Robotics is redefining industries. From manufacturing to healthcare, learn how
          humanoid robots are augmenting human potential and reshaping the global workforce.
        </>
      ),
    },
    {
      title: 'Physical AI',
      description: (
        <>
          Beyond digital agents. Understanding the convergence of Large Language Models (LLMs)
          and physical actuation to create embodied intelligence that interacts with the real world.
        </>
      ),
    },
    {
      title: 'Humanoid Robotics',
      description: (
        <>
          Master the full stack: ROS 2, NVIDIA Isaac Sim, and VLA (Vision-Language-Action) models.
          Build the nervous system, digital twin, and cognitive brain of a robot.
        </>
      ),
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="The Ultimate Physical AI & Humanoid Robotics Textbook">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
