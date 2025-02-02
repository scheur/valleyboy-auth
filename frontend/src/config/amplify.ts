import { Auth } from 'aws-amplify';

export const amplifyConfig = {
  Auth: {
    region: 'us-east-1',
    userPoolId: 'us-east-1_NeuoyywqQ',
    userPoolWebClientId: '2dv9q29rkkskstlkpfmsd2lpn5',
    oauth: {
      domain: 'auth-dev.valleyboy.io',
      scope: ['email', 'openid', 'profile'],
      redirectSignIn: 'https://valleyboy.io/callback',
      redirectSignOut: 'https://valleyboy.io',
      responseType: 'token'
    }
  },
  API: {
    endpoints: [
      {
        name: 'ChatAPI',
        endpoint: `${process.env.REACT_APP_API_ENDPOINT || 'https://your-api-id.execute-api.us-east-1.amazonaws.com'}/dev`,
        region: 'us-east-1',
        custom_header: async () => {
          try {
            const session = await Auth.currentSession();
            return {
              Authorization: `Bearer ${session.getIdToken().getJwtToken()}`
            };
          } catch (error) {
            console.error('Error getting session:', error);
            return {};
          }
        }
      }
    ]
  }
};