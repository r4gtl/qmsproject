import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
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
        {/* In futuro: altre cards per altre app */}
      </Row>
    </Container>
  );
};

export default Dashboard;
