import { Breadcrumb } from 'react-bootstrap';
import { Link, useLocation, matchPath } from 'react-router-dom';
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
  '/articoli': 'Articoli',
  '/human-resources': 'Human Resources',
  '/human-resources/dipendenti': 'Dipendenti',
  '/human-resources/tabelle': 'Tabelle Generiche',
  '/human-resources/registro-ore-lavoro': 'Registro Ore Lavoro',
  '/human-resources/formazione': 'Formazione',
  '/human-resources/formazione/tabelle': 'Tabelle Formazione',
};

// Helper per formattare data in formato italiano
const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('it-IT');
};

interface ArticoloData {
  id: number;
  descrizione: string;
}

interface ProceduraData {
  id: number;
  nr_procedura: number;
  data_procedura: string;
  nr_revisione: number;
  data_revisione: string;
}

interface RegistroFormazioneData {
  id: number;
  data_formazione: string;
  corso_descrizione: string;
}

const Breadcrumbs = () => {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);
  const [fornitoreData, setFornitoreData] = useState<{ id: string; ragionesociale: string } | null>(null);
  const [articoloData, setArticoloData] = useState<ArticoloData | null>(null);
  const [proceduraData, setProceduraData] = useState<ProceduraData | null>(null);
  const [registroFormazioneData, setRegistroFormazioneData] = useState<RegistroFormazioneData | null>(null);

  // Controlla se siamo nella pagina di modifica fornitore
  const fornitoreMatch = matchPath({ path: '/fornitori/:id/modifica', end: true }, location.pathname);

  // Controlla se siamo nella pagina procedura
  const proceduraMatch = matchPath(
    { path: '/articoli/:articoloId/procedure/:proceduraId', end: true },
    location.pathname
  );

  // Controlla se siamo nella pagina articolo (edit)
  const articoloMatch = matchPath({ path: '/articoli/:id', end: true }, location.pathname);

  // Controlla se siamo in pagine formazione registri (registro o dettaglio)
  const registroFormazioneMatch = matchPath(
    { path: '/human-resources/formazione/registri/:registroId', end: true },
    location.pathname
  );
  const dettaglioFormazioneMatch = matchPath(
    { path: '/human-resources/formazione/registri/:registroId/dettagli/:dettaglioId', end: true },
    location.pathname
  );
  // ID registro per caricare i dati
  const registroId = registroFormazioneMatch?.params.registroId || dettaglioFormazioneMatch?.params.registroId;

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

  // Carica dati articolo e procedura per breadcrumb
  useEffect(() => {
    if (proceduraMatch?.params.articoloId) {
      axios
        .get(`/articoli/articoli/${proceduraMatch.params.articoloId}/`)
        .then((res) => setArticoloData(res.data))
        .catch((err) => console.error('Errore caricamento articolo per breadcrumb:', err));
    } else if (articoloMatch?.params.id && articoloMatch.params.id !== 'new') {
      axios
        .get(`/articoli/articoli/${articoloMatch.params.id}/`)
        .then((res) => setArticoloData(res.data))
        .catch((err) => console.error('Errore caricamento articolo per breadcrumb:', err));
    } else {
      setArticoloData(null);
    }
  }, [proceduraMatch?.params.articoloId, articoloMatch?.params.id]);

  useEffect(() => {
    if (proceduraMatch?.params.proceduraId) {
      axios
        .get(`/articoli/procedure/${proceduraMatch.params.proceduraId}/`)
        .then((res) => setProceduraData(res.data))
        .catch((err) => console.error('Errore caricamento procedura per breadcrumb:', err));
    } else {
      setProceduraData(null);
    }
  }, [proceduraMatch?.params.proceduraId]);

  // Carica dati registro formazione per breadcrumb
  useEffect(() => {
    if (registroId) {
      axios
        .get(`/human-resources/registri-formazione/${registroId}/`)
        .then((res) => setRegistroFormazioneData(res.data))
        .catch((err) => console.error('Errore caricamento registro formazione per breadcrumb:', err));
    } else {
      setRegistroFormazioneData(null);
    }
  }, [registroId]);

  if (location.pathname === '/login') return null;

  const buildBreadcrumb = () => {
    const crumbs = [];
    let path = '';

    // Se siamo nella pagina procedura, costruisci breadcrumb custom
    if (proceduraMatch) {
      // Articoli
      crumbs.push(
        <Breadcrumb.Item key="/articoli" linkAs={Link} linkProps={{ to: '/articoli' }}>
          Articoli
        </Breadcrumb.Item>
      );

      // Articolo (descrizione)
      const articoloPath = `/articoli/${proceduraMatch.params.articoloId}`;
      const articoloLabel = articoloData?.descrizione || `Articolo ${proceduraMatch.params.articoloId}`;
      crumbs.push(
        <Breadcrumb.Item key={articoloPath} linkAs={Link} linkProps={{ to: articoloPath }}>
          {articoloLabel}
        </Breadcrumb.Item>
      );

      // Procedura (formato completo)
      const proceduraLabel = proceduraData
        ? `Procedura n. ${proceduraData.nr_procedura} del ${formatDate(proceduraData.data_procedura)} Rev. n. ${proceduraData.nr_revisione} del ${formatDate(proceduraData.data_revisione)}`
        : `Procedura ${proceduraMatch.params.proceduraId}`;
      crumbs.push(
        <Breadcrumb.Item key={location.pathname} active>
          {proceduraLabel}
        </Breadcrumb.Item>
      );

      return crumbs;
    }

    // Se siamo in pagine formazione registri, costruisci breadcrumb custom
    // (salta "registri" che non ha una route propria)
    if (registroFormazioneMatch || dettaglioFormazioneMatch) {
      // Human Resources
      crumbs.push(
        <Breadcrumb.Item key="/human-resources" linkAs={Link} linkProps={{ to: '/human-resources' }}>
          Human Resources
        </Breadcrumb.Item>
      );

      // Formazione (lista registri)
      crumbs.push(
        <Breadcrumb.Item key="/human-resources/formazione" linkAs={Link} linkProps={{ to: '/human-resources/formazione' }}>
          Formazione
        </Breadcrumb.Item>
      );

      // Registro (con info corso e data)
      const registroLabel = registroFormazioneData
        ? `${registroFormazioneData.corso_descrizione} - ${formatDate(registroFormazioneData.data_formazione)}`
        : `Registro ${registroId}`;

      if (dettaglioFormazioneMatch) {
        // Se siamo nel dettaglio, il registro è cliccabile
        crumbs.push(
          <Breadcrumb.Item
            key={`/human-resources/formazione/registri/${registroId}`}
            linkAs={Link}
            linkProps={{ to: `/human-resources/formazione/registri/${registroId}` }}
          >
            {registroLabel}
          </Breadcrumb.Item>
        );

        // Dettaglio (attivo)
        const isNew = dettaglioFormazioneMatch.params.dettaglioId === 'new';
        crumbs.push(
          <Breadcrumb.Item key={location.pathname} active>
            {isNew ? 'Nuovo Operatore' : 'Modifica Operatore'}
          </Breadcrumb.Item>
        );
      } else {
        // Siamo nel registro, è l'ultimo elemento (attivo)
        const isNew = registroFormazioneMatch?.params.registroId === 'new';
        crumbs.push(
          <Breadcrumb.Item key={location.pathname} active>
            {isNew ? 'Nuovo Registro' : registroLabel}
          </Breadcrumb.Item>
        );
      }

      return crumbs;
    }

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

      // Per pagina articolo singolo, mostra descrizione
      if (isLast && articoloMatch && articoloData && !proceduraMatch) {
        name = articoloData.descrizione;
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
