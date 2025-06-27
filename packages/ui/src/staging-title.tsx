import React from 'react';

export type StagingTitleProps = {
  children: React.ReactNode;
};

export const StagingTitle: React.FC<StagingTitleProps> = ({ children }) => {
  return (
    <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '1rem' }}>
      {children}
    </h1>
  );
};