/**
 * Manuale Procedure - Lista Procedure
 */
import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Table,
  Button,
  Form,
  Row,
  Col,
  Modal,
  Pagination,
  ButtonGroup,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import { FaEye, FaEdit, FaTrash } from 'react-icons/fa';
import {
  getProcedure,
  getSezioniLWG,
  createProcedura,
  updateProcedura,
  deleteProcedura,
} from '../api/manualeprocedureApi';
import type { Procedura, ProceduraCreate, SezioneLWG } from '../types';

const ProceduresPage = () => {
  const navigate = useNavigate();

  // List state
  const [items, setItems] = useState<Procedura[]>([]);
  const [loading, setLoading] = useState(false);
  const [totalCount, setTotalCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 50;

  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [filterSezione, setFilterSezione] = useState('');

  // Lookups
  const [sezioni, setSezioni] = useState<SezioneLWG[]>([]);

  // Modal state
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<Procedura | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  // Form fields
  const [formIdentificativo, setFormIdentificativo] = useState('');
  const [formDataProcedura, setFormDataProcedura] = useState('');
  const [formDescrizione, setFormDescrizione] = useState('');
  const [formSezione, setFormSezione] = useState<number | ''>('');
  const [formNote, setFormNote] = useState('');

  // Fetch sezioni lookup
  useEffect(() => {
    getSezioniLWG()
      .then((res) => setSezioni(res.data))
      .catch((err) => console.error('Error loading sezioni LWG:', err));
  }, []);

  // Fetch procedure list
  const fetchItems = useCallback(() => {
    setLoading(true);
    const params: Record<string, any> = {
      page: currentPage,
      page_size: pageSize,
      ordering: '-data_procedura',
    };
    if (searchQuery) params.search = searchQuery;
    if (filterSezione) params.fk_lwgsection = filterSezione;

    getProcedure(params)
      .then((res) => {
        setItems(res.data.results);
        setTotalCount(res.data.count);
      })
      .catch((err) => {
        console.error('Error fetching procedure:', err);
        toast.error('Errore caricamento procedure');
      })
      .finally(() => setLoading(false));
  }, [currentPage, searchQuery, filterSezione]);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  // Pagination
  const totalPages = Math.ceil(totalCount / pageSize);
  const handlePageChange = (page: number) => setCurrentPage(page);

  // Add/Edit modal handlers
  const handleAdd = () => {
    setEditing(null);
    setFormIdentificativo('');
    setFormDataProcedura('');
    setFormDescrizione('');
    setFormSezione('');
    setFormNote('');
    setShowModal(true);
  };

  const handleEdit = (item: Procedura) => {
    setEditing(item);
    setFormIdentificativo(item.identificativo);
    setFormDataProcedura(item.data_procedura);
    setFormDescrizione(item.descrizione);
    setFormSezione(item.fk_lwgsection || '');
    setFormNote(item.note || '');
    setShowModal(true);
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    const data: ProceduraCreate = {
      identificativo: formIdentificativo,
      data_procedura: formDataProcedura,
      descrizione: formDescrizione,
      fk_lwgsection: formSezione || null,
      note: formNote,
    };

    const promise = editing
      ? updateProcedura(editing.id, data)
      : createProcedura(data);

    promise
      .then(() => {
        toast.success(editing ? 'Procedura aggiornata' : 'Procedura creata');
        setShowModal(false);
        fetchItems();
      })
      .catch((err) => {
        console.error('Error saving procedura:', err);
        toast.error('Errore salvataggio procedura');
      });
  };

  // Delete handlers
  const handleDeleteClick = (id: number) => {
    setDeleteId(id);
    setShowDeleteModal(true);
  };

  const handleDeleteConfirm = () => {
    if (!deleteId) return;
    deleteProcedura(deleteId)
      .then(() => {
        toast.success('Procedura eliminata');
        setShowDeleteModal(false);
        fetchItems();
      })
      .catch((err) => {
        console.error('Error deleting procedura:', err);
        toast.error('Errore eliminazione procedura');
      });
  };

  const handleViewDetails = (id: number) => {
    navigate(`/manualeprocedure/procedure/${id}`);
  };

  return (
    <Container className="mt-4">
      <h2>Manuale Procedure</h2>

      {/* Filters */}
      <Row className="mb-3">
        <Col md={6}>
          <Form.Control
            type="text"
            placeholder="Cerca per descrizione o numero procedura..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </Col>
        <Col md={4}>
          <Form.Select value={filterSezione} onChange={(e) => setFilterSezione(e.target.value)}>
            <option value="">-- Tutte le sezioni LWG --</option>
            {sezioni.map((s) => (
              <option key={s.id} value={s.id}>
                {s.lwgsection}
              </option>
            ))}
          </Form.Select>
        </Col>
        <Col md={2} className="text-end">
          <Button onClick={handleAdd}>+ Aggiungi</Button>
        </Col>
      </Row>

      {/* Table */}
      <Table striped hover responsive>
        <thead>
          <tr>
            <th>Procedura</th>
            <th>Numero procedura</th>
            <th>Data procedura</th>
            <th>Sezione LWG</th>
            <th>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {loading && (
            <tr>
              <td colSpan={5} className="text-center">
                Caricamento...
              </td>
            </tr>
          )}
          {!loading && items.length === 0 && (
            <tr>
              <td colSpan={5} className="text-center text-muted">
                Nessuna procedura trovata
              </td>
            </tr>
          )}
          {!loading &&
            items.map((item) => (
              <tr
                key={item.id}
                onClick={() => handleViewDetails(item.id)}
                style={{ cursor: 'pointer' }}
              >
                <td>{item.descrizione}</td>
                <td>{item.identificativo}</td>
                <td>{new Date(item.data_procedura).toLocaleDateString('it-IT')}</td>
                <td>{item.fk_lwgsection_display || '—'}</td>
                <td>
                  <ButtonGroup size="sm">
                    <Button
                      variant="outline-info"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleViewDetails(item.id);
                      }}
                    >
                      <FaEye />
                    </Button>
                    <Button
                      variant="outline-primary"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEdit(item);
                      }}
                    >
                      <FaEdit />
                    </Button>
                    <Button
                      variant="outline-danger"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteClick(item.id);
                      }}
                    >
                      <FaTrash />
                    </Button>
                  </ButtonGroup>
                </td>
              </tr>
            ))}
        </tbody>
      </Table>

      {/* Pagination */}
      {totalPages > 1 && (
        <Pagination>
          <Pagination.First onClick={() => handlePageChange(1)} disabled={currentPage === 1} />
          <Pagination.Prev
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
          />
          {[...Array(totalPages)].map((_, i) => (
            <Pagination.Item
              key={i + 1}
              active={i + 1 === currentPage}
              onClick={() => handlePageChange(i + 1)}
            >
              {i + 1}
            </Pagination.Item>
          ))}
          <Pagination.Next
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
          />
          <Pagination.Last
            onClick={() => handlePageChange(totalPages)}
            disabled={currentPage === totalPages}
          />
        </Pagination>
      )}

      {/* Add/Edit Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>{editing ? 'Modifica Procedura' : 'Nuova Procedura'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>
                Numero procedura <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                type="text"
                value={formIdentificativo}
                onChange={(e) => setFormIdentificativo(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>
                Data procedura <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                type="date"
                value={formDataProcedura}
                onChange={(e) => setFormDataProcedura(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>
                Descrizione <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                type="text"
                value={formDescrizione}
                onChange={(e) => setFormDescrizione(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Sezione LWG</Form.Label>
              <Form.Select
                value={formSezione}
                onChange={(e) => setFormSezione(e.target.value ? Number(e.target.value) : '')}
              >
                <option value="">-- Seleziona --</option>
                {sezioni.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.lwgsection}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={formNote}
                onChange={(e) => setFormNote(e.target.value)}
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Annulla
            </Button>
            <Button type="submit" variant="primary">
              Salva
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Conferma eliminazione</Modal.Title>
        </Modal.Header>
        <Modal.Body>Sei sicuro di voler eliminare questa procedura?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
            Annulla
          </Button>
          <Button variant="danger" onClick={handleDeleteConfirm}>
            Elimina
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default ProceduresPage;
