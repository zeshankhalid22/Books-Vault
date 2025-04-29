import React from 'react';

interface ErrorMessageProps {
  title: string;
  message: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ title, message }) => (
  <div className="text-center py-10">
    <h2 className="text-xl font-semibold text-red-500">{title}</h2>
    <p>{message}</p>
  </div>
);