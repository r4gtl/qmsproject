/**
 * EmployeesPage - Lista dipendenti con filtro e paginazione
 *
 * Funzionalità:
 * - Tabella con colonne: Cognome Nome, Data Assunzione, Data Dimissione, Azioni
 * - Filtro ricerca per nome/cognome (debounce 300ms, backend ?q=)
 * - Paginazione server-side
 * - Righe cliccabili -> dettaglio
 * - Pulsante "Aggiungi dipendente"
 */
import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  Table,
  Button,
  Form,
  InputGroup,
  Spinner,
  Badge,
  ButtonGroup,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import { getDipendenti, deleteDipendente } from '../api';
import type { HumanResourceList, PaginatedResponse } from '../types';

// Debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

const PAGE_SIZE = 50;

export default function EmployeesPage() {
  const navigate = useNavigate();

  // State
  const [dipendenti, setDipendenti] = useState<HumanResourceList[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState<number | null>(null);

  // Filtro e paginazione
  const [searchQuery, setSearchQuery] = useState('');
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [nextPage, setNextPage] = useState<string | null>(null);
  const [prevPage, setPrevPage] = useState<string | null>(null);

  // Debounce ricerca
  const debouncedSearch = useDebounce(searchQuery, 300);

  // Fetch dipendenti
  const fetchDipendenti = useCallback(async () => {
    try {
      setLoading(true);
      const params: Record<string, unknown> = {
        page,
        page_size: PAGE_SIZE,
      };
      if (debouncedSearch) {
        params.q = debouncedSearch;
      }

      const res = await getDipendenti(params);
      const data: PaginatedResponse<HumanResourceList> = res.data;

      setDipendenti(data.results);
      setTotalCount(data.count);
      setNextPage(data.next);
      setPrevPage(data.previous);
    } catch {
      toast.error('Errore nel caricamento dipendenti');
    } finally {
      setLoading(false);
    }
  }, [page, debouncedSearch]);

  useEffect(() => {
    fetchDipendenti();
  }, [fetchDipendenti]);

  // Reset pagina quando cambia la ricerca
  useEffect(() => {
    setPage(1);
  }, [debouncedSearch]);

  // Navigazione a dettaglio
  const handleRowClick = (id: number) => {
    navigate(`/human-resources/dipendenti/${id}`);
  };

  // Elimina dipendente
  const handleDelete = async (e: React.MouseEvent, id: number) => {
    e.stopPropagation(); // Evita navigazione
    if (!confirm('Eliminare questo dipendente?')) return;

    try {
      setDeleting(id);
      await deleteDipendente(id);
      toast.success('Dipendente eliminato');
      fetchDipendenti();
    } catch {
      toast.error('Errore eliminazione dipendente');
    } finally {
      setDeleting(null);
    }
  };

  // Formatta data
  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('it-IT');
  };

  // Calcolo pagine
  const totalPages = Math.ceil(totalCount / PAGE_SIZE);

  return (
    <Card>
      <Card.Header className="d-flex justify-content-between align-items-center">
        <span>
          <strong>Dipendenti</strong>
          <Badge bg="secondary" className="ms-2">
            {totalCount}
          </Badge>
        </span>
        <Button
          variant="primary"
          size="sm"
          onClick={() => navigate('/human-resources/dipendenti/new')}
        >
          + Aggiungi Dipendente
        </Button>
      </Card.Header>

      <Card.Body>
        {/* Filtro ricerca */}
        <InputGroup className="mb-3" style={{ maxWidth: '400px' }}>
          <Form.Control
            placeholder="Cerca per nome o cognome..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          {searchQuery && (
            <Button
              variant="outline-secondary"
              onClick={() => setSearchQuery('')}
            >
              ✕
            </Button>
          )}
        </InputGroup>

        {/* Tabella o loading */}
        {loading ? (
          <div className="text-center py-4">
            <Spinner animation="border" />
            <p className="mt-2 text-muted">Caricamento...</p>
          </div>
        ) : dipendenti.length === 0 ? (
          <p className="text-muted">
            {debouncedSearch
              ? `Nessun dipendente trovato per "${debouncedSearch}".`
              : 'Nessun dipendente presente.'}
          </p>
        ) : (
          <>
            <Table hover responsive bordered>
              <thead className="table-light">
                <tr>
                  <th>Cognome Nome</th>
                  <th style={{ width: '150px' }}>Data Assunzione</th>
                  <th style={{ width: '150px' }}>Data Dimissione</th>
                  <th style={{ width: '100px' }}>Azioni</th>
                </tr>
              </thead>
              <tbody>
                {dipendenti.map((d) => (
                  <tr
                    key={d.id}
                    onClick={() => handleRowClick(d.id)}
                    style={{ cursor: 'pointer' }}
                    className="align-middle"
                  >
                    <td className="text-primary">{d.full_name}</td>
                    <td>{formatDate(d.dataassunzione)}</td>
                    <td>
                      {d.datadimissioni ? (
                        <Badge bg="warning" text="dark">
                          {formatDate(d.datadimissioni)}
                        </Badge>
                      ) : (
                        <Badge bg="success">In forza</Badge>
                      )}
                    </td>
                    <td>
                      <ButtonGroup size="sm">
                        <Button
                          variant="outline-primary"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleRowClick(d.id);
                          }}
                          title="Modifica"
                        >
                          ✎
                        </Button>
                        <Button
                          variant="outline-danger"
                          onClick={(e) => handleDelete(e, d.id)}
                          disabled={deleting === d.id}
                          title="Elimina"
                        >
                          {deleting === d.id ? '...' : '✕'}
                        </Button>
                      </ButtonGroup>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>

            {/* Paginazione */}
            {totalPages > 1 && (
              <div className="d-flex justify-content-between align-items-center mt-3">
                <span className="text-muted">
                  Pagina {page} di {totalPages}
                </span>
                <ButtonGroup size="sm">
                  <Button
                    variant="outline-secondary"
                    disabled={!prevPage}
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                  >
                    ← Precedente
                  </Button>
                  <Button
                    variant="outline-secondary"
                    disabled={!nextPage}
                    onClick={() => setPage((p) => p + 1)}
                  >
                    Successiva →
                  </Button>
                </ButtonGroup>
              </div>
            )}
          </>
        )}
      </Card.Body>
    </Card>
  );
}
