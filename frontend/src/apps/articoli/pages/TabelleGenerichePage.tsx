import { Container, Row, Col, Card } from 'react-bootstrap';
import { FaFlask, FaCogs, FaTools } from 'react-icons/fa';
import ElencoTestCard from '../components/TabelleGeneriche/ElencoTestCard';
import ElencoFasiCard from '../components/TabelleGeneriche/ElencoFasiCard';

export default function TabelleGenerichePage() {
  return (
    <Container className="my-4">
      <h3 className="mb-4">Tabelle Generiche - Articoli</h3>
      <Row className="g-4">
        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaFlask className="me-2" />
              Test da superare
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <ElencoTestCard />
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaCogs className="me-2" />
              Fasi di Lavoro
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <ElencoFasiCard />
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaTools className="me-2" />
              Codici Lavorazioni
            </Card.Header>
            <Card.Body className="text-muted text-center pt-5">
              <p>In sviluppo…</p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
