import { useAuth0 } from '@auth0/auth0-react';

export default function Login() {
  const { loginWithRedirect, logout, user, isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return (
      <div className="container py-5 text-center">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card card-custom">
            <div className="card-body text-center">
              <h2 className="mb-4">{isAuthenticated ? `Welcome, ${user?.name || user?.email}` : 'Login'}</h2>
              {isAuthenticated ? (
                <>
                  <button className="btn btn-secondary me-2" onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}>
                    Logout
                  </button>
                </>
              ) : (
                <button className="btn btn-primary" onClick={() => loginWithRedirect()}>
                  Login with Auth0
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
