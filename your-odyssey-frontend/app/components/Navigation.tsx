import { Container, Nav, Navbar, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';
import styles from './navigation.module.css';

export default function Navigation() {
  const { isAuthenticated, loginWithRedirect, logout, user } = useAuth0();

  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/" className={styles.logo}>
          Your<span>Ω</span>dyssey
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Home</Nav.Link>
            <Nav.Link as={Link} to="/plan">Plan Trip</Nav.Link>
            {isAuthenticated && (
              <>
                <Nav.Link as={Link} to="/my-trips">My Trips</Nav.Link>
                <Nav.Link as={Link} to="/follows">Follows</Nav.Link>
              </>
            )}
          </Nav>
          <Nav>
            {!isAuthenticated ? (
              <Button
                variant="outline-light"
                onClick={() => loginWithRedirect()}
              >
                Log In
              </Button>
            ) : (
              <div className="d-flex align-items-center">
                <span className="text-light me-3">
                  Welcome, {user?.name}
                </span>
                <Button
                  variant="outline-light"
                  onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
                >
                  Log Out
                </Button>
              </div>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
