import { Breadcrumb } from 'react-bootstrap';
import { Link, useLocation, matchPath, useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from '@/api/axios';

const breadcrumbNameMap: Record<string, string> = {
  '/dashboard': 'Dashboard',
  '/fornitori': 'Fornitori',
  '/fornitori/nuovo/:categoria': 'Nuovo Fornitore',
  '/fornitori/:id/modifica': 'Modifica',
  '/clienti': 'Clienti',
  '/clienti/nuovo': 'Nuovo Cliente',
  '/clienti/:id': 'Modifica Cliente',
};

const Breadcrumbs = () => {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);
  const [fornitoreData, setFornitoreData] = useState<{ id: string; ragionesociale: string } | null>(null);

  // Controlla se siamo nella pagina di modifica fornitore
  const fornitoreMatch = matchPath({ path: '/fornitori/:id/modifica', end: true }, location.pathname);

  useEffect(() => {
    if (fornitoreMatch?.params.id) {
      axios
        .get(`/anagrafiche/fornitori/${fornitoreMatch.params.id}/`)
        .then((res) => setFornitoreData(res.data))
        .catch((err) => console.error('Errore caricamento fornitore per breadcrumb:', err));
    } else {
      setFornitoreData(null);
    }
  }, [fornitoreMatch?.params.id]);

  if (location.pathname === '/login') return null;

  const buildBreadcrumb = () => {
    const crumbs = [];
    let path = '';

    for (let i = 0; i < pathnames.length; i++) {
      path += `/${pathnames[i]}`;
      const found = Object.entries(breadcrumbNameMap).find(([pattern]) =>
        matchPath({ path: pattern, end: true }, path)
      );

      let name = found?.[1] || pathnames[i];

      // Se siamo nell'ultima breadcrumb della pagina di modifica fornitore, mostra la ragione sociale
      const isLast = i === pathnames.length - 1;

      // Salta l'ID nella breadcrumb (quando è solo un numero)
      const isNumericId = /^\d+$/.test(pathnames[i]);
      if (isNumericId && fornitoreMatch) {
        continue; // Non mostrare l'ID come breadcrumb separata
      }

      if (isLast && fornitoreMatch && fornitoreData) {
        name = `Modifica ${fornitoreData.ragionesociale}`;
      }

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
