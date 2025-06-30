import { Container, Row, Col } from 'react-bootstrap';
import Sidebar from '../Sidebar';
import { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <Container className="my-4 d-flex justify-content-center">
      <div className="w-100" style={{ maxWidth: '1200px' }}>
        {children}
      </div>
    </Container>
  );
}
