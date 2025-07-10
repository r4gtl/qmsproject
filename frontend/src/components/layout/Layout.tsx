import { Container, Row, Col } from 'react-bootstrap';
import { ReactNode } from 'react';
import AppNavBar from './NavBar';
import Breadcrumbs from './Breadcrumbs';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <>
      <AppNavBar />
      <Container className="my-4 d-flex justify-content-center">
        <div className="w-100" style={{ maxWidth: '1200px' }}>
          <Breadcrumbs />
          {children}
        </div>
      </Container>
    </>
  );
}
