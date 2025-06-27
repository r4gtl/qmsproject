import { Container, Row, Col } from 'react-bootstrap';
import Navbar from '../NavBar';
import Sidebar from '../Sidebar';
import { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <>
      <Navbar />
      <Container fluid>
        <Row>
          <Col md={2}>
            <Sidebar />
          </Col>
          <Col md={10} className="p-4">
            {children}
          </Col>
        </Row>
      </Container>
    </>
  );
}
