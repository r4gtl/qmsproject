import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        {/* card anagrafiche */}
        <Col md={6} lg={4}>
          <Card className="shadow-sm mb-4">
            <Card.Body>
              <Card.Title>Anagrafiche</Card.Title>
              <Card.Text>Gestisci Clienti e Fornitori</Card.Text>
              <div className="d-flex flex-column gap-2">
                <Button as={Link} to="/clienti" variant="primary">
                  Clienti
                </Button>
                <Button as={Link} to="/fornitori" variant="primary">
                  Fornitori
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
        {/* card articoli */}
        <Col md={6} lg={4}>
          <Card className="shadow-sm mb-4">
            <Card.Body>
              <Card.Title>Articoli</Card.Title>
              <Card.Text>
                Esplora, crea, modifica ed elimina gli articoli.
              </Card.Text>
              <div className="d-flex flex-column gap-2">
                <Button as={Link} to="/articoli" variant="primary">
                  Articoli
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
        {/* card human resources */}
        <Col md={6} lg={4}>
          <Card className="shadow-sm mb-4">
            <Card.Body>
              <Card.Title>Human Resources</Card.Title>
              <Card.Text>
                Gestisci dipendenti, mansioni e valutazioni.
              </Card.Text>
              <div className="d-flex flex-column gap-2">
                <Button as={Link} to="/human-resources/dipendenti" variant="primary">
                  Dipendenti
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
        {/* card acquisti pelli */}
        <Col md={6} lg={4}>
          <Card className="shadow-sm mb-4">
            <Card.Body>
              <Card.Title>Acquisti Pelli</Card.Title>
              <Card.Text>
                Gestisci lotti, origini e tabelle acquisti pelli.
              </Card.Text>
              <div className="d-flex flex-column gap-2">
                <Button as={Link} to="/acquistopelli" variant="primary">
                  Apri
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
        {/* card monitoraggi */}
        <Col md={6} lg={4}>
          <Card className="shadow-sm mb-4">
            <Card.Body>
              <Card.Title>Monitoraggi</Card.Title>
              <Card.Text>
                Acqua, Gas, Energia, Produzione
              </Card.Text>
              <div className="d-flex flex-column gap-2">
                <Button as={Link} to="/monitoraggi" variant="primary">
                  Apri
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
        {/* card manutenzioni */}
        <Col md={6} lg={4}>
          <Card className="shadow-sm mb-4">
            <Card.Body>
              <Card.Title>Manutenzioni</Card.Title>
              <Card.Text>
                Gestisci attrezzature, tarature e controlli periodici
              </Card.Text>
              <div className="d-flex flex-column gap-2">
                <Button as={Link} to="/manutenzioni" variant="primary">
                  Attrezzature
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
        {/* card manuale procedure */}
        <Col md={6} lg={4}>
          <Card className="shadow-sm mb-4">
            <Card.Body>
              <Card.Title>Manuale Procedure</Card.Title>
              <Card.Text>
                Gestisci procedure, revisioni e moduli aziendali
              </Card.Text>
              <div className="d-flex flex-column gap-2">
                <Button as={Link} to="/manualeprocedure" variant="primary">
                  Procedure
                </Button>
              </div>
            </Card.Body>
          </Card>
        </Col>
        {/* In futuro: altre cards per altre app */}
      </Row>
    </Container>
  );
};

export default Dashboard;
