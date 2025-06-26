import { Container, Row, Col, Card } from 'react-bootstrap';

const Dashboard = () => {
  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col md={8}>
          <Card className="p-4 shadow rounded-3">
            <h2 className="text-center">Benvenuto nella Dashboard</h2>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
