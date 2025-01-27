import React, { useEffect } from 'react';

const CONFIG = {
  domain: 'auth.valleyboy.io',
  region: 'us-east-1',
  clientId: '7fll7fujida1t211f99vj07smp',
  redirectUri: 'https://www.valleyboy.io/callback'
};

function App() {
  useEffect(() => {
    const token = new URLSearchParams(window.location.hash.slice(1)).get('access_token');
    
    if (!token) {
      window.location.href = `https://${CONFIG.domain}.auth.${CONFIG.region}.amazoncognito.com/login?client_id=${CONFIG.clientId}&response_type=token&scope=aws.cognito.signin.user.admin&redirect_uri=${CONFIG.redirectUri}`;
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center">
      <div className="text-white">Redirecting to login...</div>
    </div>
  );
}

export default App;