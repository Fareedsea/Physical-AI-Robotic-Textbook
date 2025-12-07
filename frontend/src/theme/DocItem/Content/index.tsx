import React from 'react';
import Content from '@theme-original/DocItem/Content';
import PersonalizeButton from '@site/src/components/PersonalizeButton';
import TranslateButton from '@site/src/components/TranslateButton';
import styles from './styles.module.css'; // We'll need a wrapper style maybe for layout

export default function ContentWrapper(props): JSX.Element {
    return (
        <>
            <div className="row" style={{ marginBottom: '1rem', gap: '1rem', marginLeft: '0.2rem' }}>
                <PersonalizeButton />
                <TranslateButton />
            </div>
            <Content {...props} />
        </>
    );
}
