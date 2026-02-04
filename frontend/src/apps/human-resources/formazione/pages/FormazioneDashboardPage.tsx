/**
 * FormazioneDashboardPage - Lista registri formazione (dashboard)
 *
 * Features:
 * - Tabella ordinata DESC per data_formazione
 * - Colonne: Data | Corso | Ore | Partecipanti | Azioni
 * - Paginazione server-side
 * - Pulsante "Aggiungi Formazione"
 * - Delete con conferma modal
 */
import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  Table,
  Button,
  Spinner,
  Badge,
  ButtonGroup,
  Modal,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import { FaGraduationCap, FaPlus, FaEdit, FaTrash } from 'react-icons/fa';
import { getRegistriFormazione, deleteRegistroFormazione } from '../api/formazioneApi';
import type { RegistroFormazioneList } from '../types';
import type { PaginatedResponse } from '../../types';

const PAGE_SIZE = 50;

export default function FormazioneDashboardPage() {
  const navigate = useNavigate();

  // State
  const [registri, setRegistri] = useState<RegistroFormazioneList[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [nextPage, setNextPage] = useState<string | null>(null);
  const [prevPage, setPrevPage] = useState<string | null>(null);

  // Delete modal state
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  // Fetch registri
  const fetchRegistri = useCallback(async () => {
    try {
      setLoading(true);
      const params: Record<string, unknown> = {
        page,
        page_size: PAGE_SIZE,
        ordering: '-data_formazione',
      };

      const res = await getRegistriFormazione(params);
      const data: PaginatedResponse<RegistroFormazioneList> = res.data;

      setRegistri(data.results);
      setTotalCount(data.count);
      setNextPage(data.next);
      setPrevPage(data.previous);
    } catch {
      toast.error('Errore nel caricamento dei registri formazione');
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    fetchRegistri();
  }, [fetchRegistri]);

  // Navigazione
  const handleAddNew = () => {
    navigate('/human-resources/formazione/registri/new');
  };

  const handleEdit = (id: number) => {
    navigate(`/human-resources/formazione/registri/${id}`);
  };

  // Delete handlers
  const handleDeleteClick = (e: React.MouseEvent, id: number) => {
    e.stopPropagation();
    setDeletingId(id);
    setShowDeleteModal(true);
  };

  const handleDeleteConfirm = async () => {
    if (!deletingId) return;

    try {
      setDeleteLoading(true);
      await deleteRegistroFormazione(deletingId);
      toast.success('Registro formazione eliminato');
      setShowDeleteModal(false);
      setDeletingId(null);
      fetchRegistri();
    } catch (err: any) {
      // Handle DRF errors: detail string or field errors object
      const data = err.response?.data;
      let msg = 'Errore durante l\'eliminazione';
      if (typeof data === 'string') {
        msg = data;
      } else if (data?.detail) {
        msg = data.detail;
      } else if (data && typeof data === 'object') {
        // Field errors: { field: ["error1", "error2"] }
        const errors = Object.values(data).flat().join(', ');
        if (errors) msg = errors;
      }
      toast.error(msg);
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleDeleteCancel = () => {
    setShowDeleteModal(false);
    setDeletingId(null);
  };

  // Formatta data
  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('it-IT');
  };

  // Calcolo pagine
  const totalPages = Math.ceil(totalCount / PAGE_SIZE);

  return (
    <>
      <Card>
        <Card.Header className="d-flex justify-content-between align-items-center">
          <span className="d-flex align-items-center">
            <FaGraduationCap className="me-2" />
            <strong>Formazione</strong>
            <Badge bg="secondary" className="ms-2">
              {totalCount}
            </Badge>
          </span>
          <Button variant="primary" size="sm" onClick={handleAddNew}>
            <FaPlus className="me-1" /> Aggiungi Formazione
          </Button>
        </Card.Header>

        <Card.Body>
          {loading ? (
            <div className="text-center py-4">
              <Spinner animation="border" />
              <p className="mt-2 text-muted">Caricamento...</p>
            </div>
          ) : registri.length === 0 ? (
            <p className="text-muted">Nessun registro formazione presente.</p>
          ) : (
            <>
              <Table hover responsive bordered>
                <thead className="table-light">
                  <tr>
                    <th style={{ width: '120px' }}>Data</th>
                    <th>Corso</th>
                    <th style={{ width: '100px' }}>Ore</th>
                    <th style={{ width: '120px' }}>Partecipanti</th>
                    <th style={{ width: '120px' }}>Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  {registri.map((r) => (
                    <tr
                      key={r.id}
                      onClick={() => handleEdit(r.id)}
                      style={{ cursor: 'pointer' }}
                      className="align-middle"
                    >
                      <td>{formatDate(r.data_formazione)}</td>
                      <td className="text-primary">{r.corso_descrizione || '—'}</td>
                      <td>{r.ore || '—'}</td>
                      <td>
                        <Badge bg="info">{r.num_partecipanti ?? 0}</Badge>
                      </td>
                      <td>
                        <ButtonGroup size="sm">
                          <Button
                            variant="outline-primary"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleEdit(r.id);
                            }}
                            title="Modifica"
                          >
                            <FaEdit />
                          </Button>
                          <Button
                            variant="outline-danger"
                            onClick={(e) => handleDeleteClick(e, r.id)}
                            title="Elimina"
                          >
                            <FaTrash />
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
                      &larr; Precedente
                    </Button>
                    <Button
                      variant="outline-secondary"
                      disabled={!nextPage}
                      onClick={() => setPage((p) => p + 1)}
                    >
                      Successiva &rarr;
                    </Button>
                  </ButtonGroup>
                </div>
              )}
            </>
          )}
        </Card.Body>
      </Card>

      {/* Delete Confirmation Modal */}
      <Modal show={showDeleteModal} onHide={handleDeleteCancel} centered>
        <Modal.Header closeButton>
          <Modal.Title>Conferma eliminazione</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Sei sicuro di voler eliminare questo registro formazione?
          <br />
          <small className="text-muted">
            Verranno eliminati anche tutti i dettagli (operatori) associati.
          </small>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleDeleteCancel} disabled={deleteLoading}>
            Annulla
          </Button>
          <Button variant="danger" onClick={handleDeleteConfirm} disabled={deleteLoading}>
            {deleteLoading ? <Spinner animation="border" size="sm" /> : 'Elimina'}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
