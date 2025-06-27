import { Navbar, Container, Nav, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Sidebar from './Sidebar';
import { FaBars } from 'react-icons/fa';
import { useState } from 'react';

const AppNavbar = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    navigate('/login');
  };

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <>
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
          <Button
            variant="outline-light"
            className="me-2"
            onClick={toggleSidebar}
          >
            <FaBars /> Menu
          </Button>

          <Navbar.Brand href="/dashboard">QMS App</Navbar.Brand>
          <Nav className="ms-auto">
            {user && (
              <Navbar.Text className="text-white me-3">
                Benvenuto, <strong>{user.username}</strong>
              </Navbar.Text>
            )}

            <Button variant="outline-light" onClick={handleLogout}>
              Logout
            </Button>
          </Nav>
        </Container>
      </Navbar>
      <Sidebar show={sidebarOpen} onHide={toggleSidebar} />
    </>
  );
};

export default AppNavbar;
