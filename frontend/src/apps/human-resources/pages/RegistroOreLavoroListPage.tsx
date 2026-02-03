/**
 * RegistroOreLavoroListPage - Lista registri ore lavoro
 *
 * Features:
 * - Tabella paginata con Anno, Mese, Ore lavorabili, Ore lavorate
 * - Pulsante "Aggiungi registro"
 * - Azioni: Modifica / Elimina con modal conferma
 * - Filtro per anno (opzionale)
 */
import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Card,
  Table,
  Button,
  Spinner,
  Modal,
  Form,
  Row,
  Col,
  Alert,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import { FaClock, FaPlus, FaEdit, FaTrash } from 'react-icons/fa';
import { getRegistriOreLavoro, deleteRegistroOreLavoro } from '../api';
import type { RegistroOreLavoroList, PaginatedResponse } from '../types';

export default function RegistroOreLavoroListPage() {
  const navigate = useNavigate();
  const [items, setItems] = useState<RegistroOreLavoroList[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Pagination
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrev, setHasPrev] = useState(false);
  const pageSize = 20;

  // Filters
  const [filterYear, setFilterYear] = useState<string>('');

  // Delete modal
  const [deleteTarget, setDeleteTarget] = useState<RegistroOreLavoroList | null>(null);
  const [deleting, setDeleting] = useState(false);

  // Generate year options (last 10 years)
  const currentYear = new Date().getFullYear();
  const yearOptions = Array.from({ length: 10 }, (_, i) => currentYear - i);

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const params: Record<string, unknown> = {
        page,
        page_size: pageSize,
        ordering: '-entry_year,-entry_month',
      };
      if (filterYear) {
        params.entry_year = Number(filterYear);
      }
      const res = await getRegistriOreLavoro(params);
      const data: PaginatedResponse<RegistroOreLavoroList> = res.data;
      setItems(data.results);
      setTotalCount(data.count);
      setHasNext(!!data.next);
      setHasPrev(!!data.previous);
    } catch (err: any) {
      setError('Errore nel caricamento dei registri ore lavoro.');
      toast.error('Errore caricamento dati');
    } finally {
      setLoading(false);
    }
  }, [page, filterYear]);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    navigate('/human-resources/registro-ore-lavoro/new');
  };

  const handleEdit = (item: RegistroOreLavoroList) => {
    navigate(`/human-resources/registro-ore-lavoro/${item.id}`);
  };

  const handleDeleteClick = (item: RegistroOreLavoroList) => {
    setDeleteTarget(item);
  };

  const handleDeleteConfirm = async () => {
    if (!deleteTarget) return;
    try {
      setDeleting(true);
      await deleteRegistroOreLavoro(deleteTarget.id);
      toast.success('Registro eliminato');
      setDeleteTarget(null);
      await loadItems();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore durante l\'eliminazione';
      toast.error(msg);
    } finally {
      setDeleting(false);
    }
  };

  const handleFilterChange = (year: string) => {
    setFilterYear(year);
    setPage(1); // Reset to first page when filter changes
  };

  const formatValue = (val: number | null): string => {
    return val !== null && val !== undefined ? String(val) : '–';
  };

  return (
    <Container className="my-4">
      <Card className="shadow-sm">
        <Card.Header className="d-flex align-items-center justify-content-between">
          <div className="d-flex align-items-center">
            <FaClock className="me-2" />
            <span className="fw-bold">Registro Ore Lavoro</span>
          </div>
          <Button variant="primary" size="sm" onClick={handleAdd}>
            <FaPlus className="me-1" /> Aggiungi registro
          </Button>
        </Card.Header>
        <Card.Body>
          {/* Filters */}
          <Row className="mb-3">
            <Col md={3}>
              <Form.Group>
                <Form.Label className="small text-muted">Filtra per anno</Form.Label>
                <Form.Select
                  size="sm"
                  value={filterYear}
                  onChange={(e) => handleFilterChange(e.target.value)}
                >
                  <option value="">Tutti gli anni</option>
                  {yearOptions.map((y) => (
                    <option key={y} value={y}>
                      {y}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={9} className="d-flex align-items-end justify-content-end">
              <small className="text-muted">
                {totalCount} registri trovati
              </small>
            </Col>
          </Row>

          {/* Loading */}
          {loading && (
            <div className="text-center py-4">
              <Spinner animation="border" />
            </div>
          )}

          {/* Error */}
          {error && !loading && (
            <Alert variant="danger">{error}</Alert>
          )}

          {/* Table */}
          {!loading && !error && (
            <>
              <Table striped hover responsive>
                <thead>
                  <tr>
                    <th>Anno</th>
                    <th>Mese</th>
                    <th className="text-end">Ore Lavorabili</th>
                    <th className="text-end">Ore Lavorate</th>
                    <th style={{ width: '120px' }}>Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((item) => (
                    <tr key={item.id}>
                      <td>{item.entry_year}</td>
                      <td>{item.month_verbose}</td>
                      <td className="text-end">{formatValue(item.ore_lavorabili)}</td>
                      <td className="text-end">{formatValue(item.ore_lavorate)}</td>
                      <td>
                        <Button
                          size="sm"
                          variant="outline-primary"
                          className="me-1"
                          onClick={() => handleEdit(item)}
                          title="Modifica"
                        >
                          <FaEdit />
                        </Button>
                        <Button
                          size="sm"
                          variant="outline-danger"
                          onClick={() => handleDeleteClick(item)}
                          title="Elimina"
                        >
                          <FaTrash />
                        </Button>
                      </td>
                    </tr>
                  ))}
                  {items.length === 0 && (
                    <tr>
                      <td colSpan={5} className="text-center text-muted py-4">
                        Nessun registro ore lavoro presente.
                      </td>
                    </tr>
                  )}
                </tbody>
              </Table>

              {/* Pagination */}
              {(hasNext || hasPrev) && (
                <div className="d-flex justify-content-between align-items-center mt-3">
                  <Button
                    variant="outline-secondary"
                    size="sm"
                    disabled={!hasPrev}
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                  >
                    &laquo; Precedente
                  </Button>
                  <span className="text-muted">
                    Pagina {page} di {Math.ceil(totalCount / pageSize) || 1}
                  </span>
                  <Button
                    variant="outline-secondary"
                    size="sm"
                    disabled={!hasNext}
                    onClick={() => setPage((p) => p + 1)}
                  >
                    Successiva &raquo;
                  </Button>
                </div>
              )}
            </>
          )}
        </Card.Body>
      </Card>

      {/* Delete confirmation modal */}
      <Modal show={!!deleteTarget} onHide={() => setDeleteTarget(null)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>Conferma eliminazione</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {deleteTarget && (
            <p>
              Sei sicuro di voler eliminare il registro di{' '}
              <strong>
                {deleteTarget.month_verbose} {deleteTarget.entry_year}
              </strong>
              ?
            </p>
          )}
          <p className="text-muted small">Questa azione non può essere annullata.</p>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={() => setDeleteTarget(null)}
            disabled={deleting}
          >
            Annulla
          </Button>
          <Button
            variant="danger"
            onClick={handleDeleteConfirm}
            disabled={deleting}
          >
            {deleting ? <Spinner animation="border" size="sm" /> : 'Elimina'}
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}
