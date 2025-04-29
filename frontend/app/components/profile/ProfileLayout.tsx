import React from 'react';

interface ProfileLayoutProps {
  title: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
}

export const ProfileLayout: React.FC<ProfileLayoutProps> = ({ title, children, actions }) => (
  <div className="max-w-3xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
    <div className="flex justify-between items-center mb-6">
      <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
      {actions && <div className="flex space-x-3">{actions}</div>}
    </div>
    {children}
  </div>
);