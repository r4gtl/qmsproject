import { Offcanvas, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';

interface SidebarProps {
  show: boolean;
  onHide: () => void;
}

const Sidebar = ({ show, onHide }: SidebarProps) => {
  return (
    <Offcanvas show={show} onHide={onHide} backdrop="static">
      <Offcanvas.Header closeButton>
        <Offcanvas.Title>Menu</Offcanvas.Title>
      </Offcanvas.Header>
      <Offcanvas.Body>
        <Nav className="flex-column">
          <Nav.Link as={Link} to="/dashboard" onClick={onHide}>
            Dashboard
          </Nav.Link>
          <Nav.Link as={Link} to="/fornitori" onClick={onHide}>
            Fornitori
          </Nav.Link>
          <Nav.Link as={Link} to="/documenti" onClick={onHide}>
            Documenti
          </Nav.Link>
          {/* Altri link */}
        </Nav>
      </Offcanvas.Body>
    </Offcanvas>
  );
};

export default Sidebar;
