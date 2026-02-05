/**
 * LottiPage - Lista lotti con filtri server-side e paginazione.
 */
import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container, Card, Table, Button, Form, Row, Col,
  Spinner, Badge, ButtonGroup,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import ConfirmModal from '@/components/common/ConfirmModal';
import {
  getLotti, deleteLotto,
  getTipiAnimale, getTipiGrezzo, getFornitoriLookup,
} from '../api/acquistopelliApi';
import type {
  LottoList, TipoAnimale, TipoGrezzo, Fornitore,
  PaginatedResponse,
} from '../types';

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  useEffect(() => {
    const h = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(h);
  }, [value, delay]);
  return debouncedValue;
}

const PAGE_SIZE = 25;

export default function LottiPage() {
  const navigate = useNavigate();

  const [lotti, setLotti] = useState<LottoList[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [nextPage, setNextPage] = useState<string | null>(null);
  const [prevPage, setPrevPage] = useState<string | null>(null);

  // Filtri
  const [searchId, setSearchId] = useState('');
  const [filterFornitore, setFilterFornitore] = useState('');
  const [filterAnimale, setFilterAnimale] = useState('');
  const [filterGrezzo, setFilterGrezzo] = useState('');
  const debouncedSearch = useDebounce(searchId, 400);

  // Lookups
  const [fornitori, setFornitori] = useState<Fornitore[]>([]);
  const [tipiAnimale, setTipiAnimale] = useState<TipoAnimale[]>([]);
  const [tipiGrezzo, setTipiGrezzo] = useState<TipoGrezzo[]>([]);

  // Delete
  const [deleteId, setDeleteId] = useState<number | null>(null);

  // Load lookups
  useEffect(() => {
    Promise.all([
      getFornitoriLookup(),
      getTipiAnimale({ page_size: 1000 }),
      getTipiGrezzo({ page_size: 1000 }),
    ]).then(([fRes, aRes, gRes]) => {
      setFornitori(fRes.data.results);
      setTipiAnimale(aRes.data.results);
      setTipiGrezzo(gRes.data.results);
    }).catch(() => toast.error('Errore caricamento filtri'));
  }, []);

  const fetchLotti = useCallback(async () => {
    setLoading(true);
    try {
      const params: Record<string, unknown> = {
        page,
        page_size: PAGE_SIZE,
      };
      if (debouncedSearch) params.search = debouncedSearch;
      if (filterFornitore) params.fk_fornitore = filterFornitore;
      if (filterAnimale) params.fk_tipoanimale = filterAnimale;
      if (filterGrezzo) params.fk_tipogrezzo = filterGrezzo;

      const res = await getLotti(params);
      const data: PaginatedResponse<LottoList> = res.data;
      setLotti(data.results);
      setTotalCount(data.count);
      setNextPage(data.next);
      setPrevPage(data.previous);
    } catch {
      toast.error('Errore caricamento lotti');
    } finally {
      setLoading(false);
    }
  }, [page, debouncedSearch, filterFornitore, filterAnimale, filterGrezzo]);

  useEffect(() => { fetchLotti(); }, [fetchLotti]);
  useEffect(() => { setPage(1); }, [debouncedSearch, filterFornitore, filterAnimale, filterGrezzo]);

  const handleDelete = async (id: number) => {
    try {
      await deleteLotto(id);
      toast.success('Lotto eliminato');
      fetchLotti();
    } catch {
      toast.error('Errore eliminazione lotto');
    }
    setDeleteId(null);
  };

  const formatDate = (d: string) => d ? new Date(d).toLocaleDateString('it-IT') : '—';
  const totalPages = Math.ceil(totalCount / PAGE_SIZE);

  return (
    <Container className="my-4">
      <Card className="shadow-sm">
        <Card.Header className="d-flex justify-content-between align-items-center">
          <span className="fw-bold">Acquisti Pelli</span>
          <Button size="sm" onClick={() => navigate('/acquistopelli/lotti/new')}>
            + Nuovo Acquisto
          </Button>
        </Card.Header>
        <Card.Body>
          {/* Filtri */}
          <Row className="mb-3 g-2">
            <Col md={3}>
              <Form.Control
                size="sm"
                placeholder="Cerca identificativo..."
                value={searchId}
                onChange={(e) => setSearchId(e.target.value)}
              />
            </Col>
            <Col md={3}>
              <Form.Select size="sm" value={filterFornitore} onChange={(e) => setFilterFornitore(e.target.value)}>
                <option value="">Tutti i fornitori</option>
                {fornitori.map((f) => (
                  <option key={f.id} value={f.id}>{f.ragionesociale}</option>
                ))}
              </Form.Select>
            </Col>
            <Col md={3}>
              <Form.Select size="sm" value={filterAnimale} onChange={(e) => setFilterAnimale(e.target.value)}>
                <option value="">Tutti gli animali</option>
                {tipiAnimale.map((a) => (
                  <option key={a.id} value={a.id}>{a.descrizione}</option>
                ))}
              </Form.Select>
            </Col>
            <Col md={3}>
              <Form.Select size="sm" value={filterGrezzo} onChange={(e) => setFilterGrezzo(e.target.value)}>
                <option value="">Tutti i grezzi</option>
                {tipiGrezzo.map((g) => (
                  <option key={g.id} value={g.id}>{g.descrizione}</option>
                ))}
              </Form.Select>
            </Col>
          </Row>

          {loading ? (
            <div className="text-center py-4"><Spinner /></div>
          ) : (
            <>
              <Table striped hover responsive>
                <thead>
                  <tr>
                    <th>Data Acquisto</th>
                    <th>Identificativo</th>
                    <th>Fornitore</th>
                    <th>Tipo Animale</th>
                    <th>Tipo Grezzo</th>
                    <th>Pezzi</th>
                    <th className="text-end">Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  {lotti.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="text-center text-muted">
                        Nessun lotto trovato
                      </td>
                    </tr>
                  ) : (
                    lotti.map((l) => (
                      <tr
                        key={l.id}
                        onClick={() => navigate(`/acquistopelli/lotti/${l.id}`)}
                        style={{ cursor: 'pointer' }}
                      >
                        <td>{formatDate(l.data_acquisto)}</td>
                        <td>
                          <span className="fw-semibold">{l.identificativo}</span>
                          {l.is_lwg && <Badge bg="success" className="ms-1">LWG</Badge>}
                        </td>
                        <td>{l.fornitore_ragionesociale || '—'}</td>
                        <td>{l.tipoanimale_descrizione || '—'}</td>
                        <td>{l.tipogrezzo_descrizione || '—'}</td>
                        <td>{l.pezzi ?? '—'}</td>
                        <td className="text-end">
                          <ButtonGroup size="sm">
                            <Button
                              variant="outline-primary"
                              onClick={(e) => {
                                e.stopPropagation();
                                navigate(`/acquistopelli/lotti/${l.id}`);
                              }}
                            >
                              ✏️
                            </Button>
                            <Button
                              variant="outline-danger"
                              onClick={(e) => {
                                e.stopPropagation();
                                setDeleteId(l.id);
                              }}
                            >
                              🗑
                            </Button>
                          </ButtonGroup>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </Table>

              {/* Paginazione */}
              {totalPages > 1 && (
                <div className="d-flex justify-content-between align-items-center">
                  <small className="text-muted">
                    {totalCount} risultati - Pagina {page} di {totalPages}
                  </small>
                  <ButtonGroup size="sm">
                    <Button
                      variant="outline-secondary"
                      disabled={!prevPage}
                      onClick={() => setPage((p) => p - 1)}
                    >
                      Precedente
                    </Button>
                    <Button
                      variant="outline-secondary"
                      disabled={!nextPage}
                      onClick={() => setPage((p) => p + 1)}
                    >
                      Successivo
                    </Button>
                  </ButtonGroup>
                </div>
              )}
            </>
          )}
        </Card.Body>
      </Card>

      <ConfirmModal
        show={!!deleteId}
        onHide={() => setDeleteId(null)}
        onConfirm={() => deleteId && handleDelete(deleteId)}
        message="Sei sicuro di voler eliminare questo lotto?"
      />
    </Container>
  );
}
