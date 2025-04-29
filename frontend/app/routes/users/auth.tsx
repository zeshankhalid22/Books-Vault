import React, { useState } from 'react';
import Login from '~/components/Login';
import Register from '~/components/Register';

const AuthPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'login' | 'register'>('login');

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
      {/* Enhanced Tab Navigation */}
      <div className="flex border-b border-gray-200 mb-6">
        <div className="w-1/2">
          <button
            className={`w-full py-3 px-4 text-center font-medium rounded-t-lg transition-all duration-200 ${
              activeTab === 'login'
                ? 'bg-white border-l border-t border-r border-gray-200 text-blue-600'
                : 'bg-gray-100 text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
            onClick={() => setActiveTab('login')}
          >
            Log In
          </button>
        </div>
        <div className="w-1/2">
          <button
            className={`w-full py-3 px-4 text-center font-medium rounded-t-lg transition-all duration-200 ${
              activeTab === 'register'
                ? 'bg-white border-l border-t border-r border-gray-200 text-blue-600'
                : 'bg-gray-100 text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
            onClick={() => setActiveTab('register')}
          >
            Sign Up
          </button>
        </div>
      </div>

      {/* Form Container */}
      <div className="auth-forms p-2">
        {activeTab === 'login' ? <Login /> : <Register />}
      </div>
    </div>
  );
};

export default AuthPage;