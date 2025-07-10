import { Breadcrumb } from 'react-bootstrap';
import { Link, useLocation, matchPath } from 'react-router-dom';

const breadcrumbNameMap: Record<string, string> = {
  '/dashboard': 'Dashboard',
  '/fornitori': 'Fornitori',
  '/fornitori/nuovo/:categoria': 'Nuovo Fornitore',
  '/fornitori/:id/modifica': 'Modifica Fornitore',
  '/clienti': 'Clienti',
  '/clienti/nuovo': 'Nuovo Cliente',
  '/clienti/:id': 'Modifica Cliente',
};

const Breadcrumbs = () => {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);

  if (location.pathname === '/login') return null;

  const buildBreadcrumb = () => {
    const crumbs = [];
    let path = '';

    for (let i = 0; i < pathnames.length; i++) {
      path += `/${pathnames[i]}`;
      const found = Object.entries(breadcrumbNameMap).find(([pattern]) =>
        matchPath({ path: pattern, end: true }, path)
      );

      const name = found?.[1] || pathnames[i];

      const isLast = i === pathnames.length - 1;
      crumbs.push(
        <Breadcrumb.Item
          key={path}
          linkAs={Link}
          linkProps={{ to: path }}
          active={isLast}
        >
          {name.charAt(0).toUpperCase() + name.slice(1)}
        </Breadcrumb.Item>
      );
    }

    return crumbs;
  };

  return (
    <Breadcrumb className="mb-4">
      <Breadcrumb.Item linkAs={Link} linkProps={{ to: '/' }}>
        Home
      </Breadcrumb.Item>
      {buildBreadcrumb()}
    </Breadcrumb>
  );
};

export default Breadcrumbs;
