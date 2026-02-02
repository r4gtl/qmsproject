import { Offcanvas, Nav } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';

interface SidebarProps {
  show: boolean;
  onHide: () => void;
}

const Sidebar = ({ show, onHide }: SidebarProps) => {
  const location = useLocation();
  const isInArticoli = location.pathname.startsWith('/articoli');
  const isInHumanResources = location.pathname.startsWith('/human-resources');

  return (
    <Offcanvas show={show} onHide={onHide} backdrop="static" placement="start">
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
          {/* Sezione visibile solo per articoli */}
          {isInArticoli && (
            <>
              <hr />
              <div className="fw-bold text-muted px-2 mb-1">
                Tabelle Articoli
              </div>
              <Nav.Link as={Link} to="/articoli/tabelle" onClick={onHide}>
                Tabelle Generiche
              </Nav.Link>
            </>
          )}

          {/* Sezione visibile solo per human resources */}
          {isInHumanResources && (
            <>
              <hr />
              <div className="fw-bold text-muted px-2 mb-1">
                Human Resources
              </div>
              <Nav.Link as={Link} to="/human-resources/dipendenti" onClick={onHide}>
                Dipendenti
              </Nav.Link>
              <Nav.Link as={Link} to="/human-resources/tabelle" onClick={onHide}>
                Tabelle Generiche
              </Nav.Link>
            </>
          )}

          {/* Altri link */}
        </Nav>
      </Offcanvas.Body>
    </Offcanvas>
  );
};

export default Sidebar;
