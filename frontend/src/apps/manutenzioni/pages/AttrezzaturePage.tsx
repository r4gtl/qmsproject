/**
 * AttrezzaturePage - Lista attrezzature con CRUD modals
 *
 * Features:
 * - Tabella con paginazione server-side
 * - Ricerca per codice/descrizione/modello
 * - Modal create/edit con upload image
 * - Delete con conferma modal
 */
import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Card,
  Table,
  Button,
  Spinner,
  Badge,
  ButtonGroup,
  Modal,
  Form,
  Row,
  Col,
  InputGroup,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import { FaCog, FaPlus, FaEdit, FaTrash, FaSearch, FaEye } from 'react-icons/fa';
import {
  getAttrezzature,
  createAttrezzatura,
  updateAttrezzatura,
  deleteAttrezzatura,
  getWardsForSelect,
  getDipendentiForSelect,
} from '../api/manutenzioniApi';
import type {
  AttrezzaturaList,
  AttrezzaturaDetail,
  Ward,
  HumanResource,
} from '../types';
import { extractErrorMessage } from '../utils/drfErrors';

const PAGE_SIZE = 50;

export default function AttrezzaturePage() {
  const navigate = useNavigate();

  // State
  const [attrezzature, setAttrezzature] = useState<AttrezzaturaList[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [nextPage, setNextPage] = useState<string | null>(null);
  const [prevPage, setPrevPage] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchInput, setSearchInput] = useState('');

  // Lookups
  const [wards, setWards] = useState<Ward[]>([]);
  const [dipendenti, setDipendenti] = useState<HumanResource[]>([]);
  const [lookupsLoaded, setLookupsLoaded] = useState(false);

  // Create/Edit modal state
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<AttrezzaturaDetail | null>(null);
  const [saving, setSaving] = useState(false);

  // Form fields
  const [formCodice, setFormCodice] = useState('');
  const [formDescrizione, setFormDescrizione] = useState('');
  const [formModello, setFormModello] = useState('');
  const [formSerieMatricola, setFormSerieMatricola] = useState('');
  const [formWard, setFormWard] = useState<number | ''>('');
  const [formIsDismesso, setFormIsDismesso] = useState(false);
  const [formDataDismissione, setFormDataDismissione] = useState('');
  const [formIsTaratura, setFormIsTaratura] = useState(false);
  const [formPeriodoTaratura, setFormPeriodoTaratura] = useState<number | ''>('');
  const [formProceduraControlli, setFormProceduraControlli] = useState('');
  const [formPeriodoControlli, setFormPeriodoControlli] = useState<number | ''>('');
  const [formRiferimentoNormativo, setFormRiferimentoNormativo] = useState('');
  const [formHR, setFormHR] = useState<number | ''>('');
  const [formImage, setFormImage] = useState<File | null>(null);
  const [formNote, setFormNote] = useState('');

  // Delete modal state
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  // Load lookups (wards, dipendenti)
  const loadLookups = useCallback(async () => {
    try {
      const [wardsRes, dipRes] = await Promise.all([
        getWardsForSelect(),
        getDipendentiForSelect(),
      ]);
      setWards(wardsRes.data.results);
      setDipendenti(dipRes.data.results);
      setLookupsLoaded(true);
    } catch {
      toast.error('Errore caricamento lookup');
    }
  }, []);

  useEffect(() => {
    loadLookups();
  }, [loadLookups]);

  // Fetch attrezzature
  const fetchAttrezzature = useCallback(async () => {
    try {
      setLoading(true);
      const params: Record<string, unknown> = {
        page,
        page_size: PAGE_SIZE,
        ordering: 'codice_attrezzatura',
      };

      if (searchQuery) {
        params.q = searchQuery;
      }

      const res = await getAttrezzature(params);
      const data = res.data;

      setAttrezzature(data.results);
      setTotalCount(data.count);
      setNextPage(data.next);
      setPrevPage(data.previous);
    } catch {
      toast.error('Errore nel caricamento delle attrezzature');
    } finally {
      setLoading(false);
    }
  }, [page, searchQuery]);

  useEffect(() => {
    fetchAttrezzature();
  }, [fetchAttrezzature]);

  // Search handler
  const handleSearch = () => {
    setSearchQuery(searchInput);
    setPage(1);
  };

  const handleSearchKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleClearSearch = () => {
    setSearchInput('');
    setSearchQuery('');
    setPage(1);
  };

  // Modal handlers
  const handleAddNew = () => {
    if (!lookupsLoaded) {
      toast.warning('Attendere il caricamento dei dati...');
      return;
    }
    setEditing(null);
    resetForm();
    setShowModal(true);
  };

  const handleViewDetails = (id: number) => {
    navigate(`/manutenzioni/${id}`);
  };

  const handleEdit = async (attrezzatura: AttrezzaturaList) => {
    if (!lookupsLoaded) {
      toast.warning('Attendere il caricamento dei dati...');
      return;
    }
    // Per edit, carichiamo il dettaglio completo (non abbiamo tutti i campi in List)
    // In questo caso AttrezzaturaList ha già tutti i campi necessari, ma per coerenza
    // con il pattern potremmo fare una chiamata API. Per ora usiamo direttamente i dati.
    setEditing(attrezzatura as unknown as AttrezzaturaDetail);
    setFormCodice(attrezzatura.codice_attrezzatura);
    setFormDescrizione(attrezzatura.descrizione);
    setFormModello(attrezzatura.modello || '');
    setFormSerieMatricola(''); // Non presente in List, lasciamo vuoto
    setFormWard(attrezzatura.fk_ward || '');
    setFormIsDismesso(attrezzatura.is_dismesso);
    setFormDataDismissione(''); // Non presente in List
    setFormIsTaratura(attrezzatura.is_taratura);
    setFormPeriodoTaratura('');
    setFormProceduraControlli('');
    setFormPeriodoControlli('');
    setFormRiferimentoNormativo('');
    setFormHR(attrezzatura.fk_human_resource || '');
    setFormImage(null);
    setFormNote('');
    setShowModal(true);
  };

  const resetForm = () => {
    setFormCodice('');
    setFormDescrizione('');
    setFormModello('');
    setFormSerieMatricola('');
    setFormWard('');
    setFormIsDismesso(false);
    setFormDataDismissione('');
    setFormIsTaratura(false);
    setFormPeriodoTaratura('');
    setFormProceduraControlli('');
    setFormPeriodoControlli('');
    setFormRiferimentoNormativo('');
    setFormHR('');
    setFormImage(null);
    setFormNote('');
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formCodice.trim()) {
      toast.warning('Il codice attrezzatura è obbligatorio');
      return;
    }
    if (!formDescrizione.trim()) {
      toast.warning('La descrizione è obbligatoria');
      return;
    }

    try {
      setSaving(true);

      // Costruisci FormData per supportare upload image
      const formData = new FormData();
      formData.append('codice_attrezzatura', formCodice.trim());
      formData.append('descrizione', formDescrizione.trim());
      if (formModello) formData.append('modello', formModello.trim());
      if (formSerieMatricola) formData.append('serie_matricola', formSerieMatricola.trim());
      if (formWard) formData.append('fk_ward', String(formWard));
      formData.append('is_dismesso', String(formIsDismesso));
      if (formIsDismesso && formDataDismissione) {
        formData.append('data_dismissione', formDataDismissione);
      }
      formData.append('is_taratura', String(formIsTaratura));
      if (formIsTaratura && formPeriodoTaratura) {
        formData.append('periodo_taratura', String(formPeriodoTaratura));
      }
      if (formProceduraControlli) {
        formData.append('procedura_controlli_periodici', formProceduraControlli.trim());
      }
      if (formPeriodoControlli) {
        formData.append('periodo_controlli_periodici', String(formPeriodoControlli));
      }
      if (formRiferimentoNormativo) {
        formData.append(
          'riferimento_normativo_controlli_periodici',
          formRiferimentoNormativo.trim()
        );
      }
      if (formHR) formData.append('fk_human_resource', String(formHR));
      if (formImage) formData.append('image', formImage);
      if (formNote) formData.append('note', formNote.trim());

      if (editing) {
        await updateAttrezzatura(editing.id, formData);
        toast.success('Attrezzatura aggiornata');
      } else {
        await createAttrezzatura(formData);
        toast.success('Attrezzatura creata');
      }

      setShowModal(false);
      await fetchAttrezzature();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore salvataggio attrezzatura'));
    } finally {
      setSaving(false);
    }
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
      await deleteAttrezzatura(deletingId);
      toast.success('Attrezzatura eliminata');
      setShowDeleteModal(false);
      setDeletingId(null);
      await fetchAttrezzature();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore durante l\'eliminazione'));
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleDeleteCancel = () => {
    setShowDeleteModal(false);
    setDeletingId(null);
  };

  // Calcolo pagine
  const totalPages = Math.ceil(totalCount / PAGE_SIZE);

  return (
    <Container className="my-4">
      <Card>
        <Card.Header className="d-flex justify-content-between align-items-center">
          <span className="d-flex align-items-center">
            <FaCog className="me-2" />
            <strong>Attrezzature</strong>
            <Badge bg="secondary" className="ms-2">
              {totalCount}
            </Badge>
          </span>
          <Button variant="primary" size="sm" onClick={handleAddNew}>
            <FaPlus className="me-1" /> Aggiungi Attrezzatura
          </Button>
        </Card.Header>

        <Card.Body>
          {/* Search bar */}
          <Row className="mb-3">
            <Col md={6}>
              <InputGroup>
                <Form.Control
                  placeholder="Cerca per codice, descrizione o modello..."
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  onKeyDown={handleSearchKeyDown}
                />
                <Button variant="outline-secondary" onClick={handleSearch}>
                  <FaSearch />
                </Button>
                {searchQuery && (
                  <Button variant="outline-danger" onClick={handleClearSearch}>
                    ✕
                  </Button>
                )}
              </InputGroup>
            </Col>
          </Row>

          {loading ? (
            <div className="text-center py-4">
              <Spinner animation="border" />
              <p className="mt-2 text-muted">Caricamento...</p>
            </div>
          ) : attrezzature.length === 0 ? (
            <p className="text-muted">
              {searchQuery
                ? 'Nessuna attrezzatura trovata per la ricerca.'
                : 'Nessuna attrezzatura presente.'}
            </p>
          ) : (
            <>
              <Table hover responsive bordered>
                <thead className="table-light">
                  <tr>
                    <th style={{ width: '120px' }}>Codice</th>
                    <th>Descrizione</th>
                    <th style={{ width: '150px' }}>Modello</th>
                    <th style={{ width: '150px' }}>Reparto</th>
                    <th style={{ width: '150px' }}>Responsabile</th>
                    <th style={{ width: '80px' }}>Dismesso</th>
                    <th style={{ width: '80px' }}>Taratura</th>
                    <th style={{ width: '120px' }}>Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  {attrezzature.map((a) => (
                    <tr
                      key={a.id}
                      onClick={() => handleViewDetails(a.id)}
                      style={{ cursor: 'pointer' }}
                      className="align-middle"
                    >
                      <td>
                        <strong>{a.codice_attrezzatura}</strong>
                      </td>
                      <td>{a.descrizione}</td>
                      <td>{a.modello || '—'}</td>
                      <td>{a.fk_ward_display || '—'}</td>
                      <td>{a.fk_human_resource_display || '—'}</td>
                      <td>
                        {a.is_dismesso ? (
                          <Badge bg="danger">Sì</Badge>
                        ) : (
                          <Badge bg="success">No</Badge>
                        )}
                      </td>
                      <td>
                        {a.is_taratura ? (
                          <Badge bg="info">Sì</Badge>
                        ) : (
                          <Badge bg="secondary">No</Badge>
                        )}
                      </td>
                      <td>
                        <ButtonGroup size="sm">
                          <Button
                            variant="outline-info"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleViewDetails(a.id);
                            }}
                            title="Dettagli"
                          >
                            <FaEye />
                          </Button>
                          <Button
                            variant="outline-primary"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleEdit(a);
                            }}
                            title="Modifica"
                          >
                            <FaEdit />
                          </Button>
                          <Button
                            variant="outline-danger"
                            onClick={(e) => handleDeleteClick(e, a.id)}
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

      {/* Create/Edit Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)} size="lg" backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>{editing ? 'Modifica Attrezzatura' : 'Nuova Attrezzatura'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>
                    Codice Attrezzatura <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Control
                    value={formCodice}
                    onChange={(e) => setFormCodice(e.target.value)}
                    required
                    autoFocus
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>
                    Descrizione <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Control
                    value={formDescrizione}
                    onChange={(e) => setFormDescrizione(e.target.value)}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Modello</Form.Label>
                  <Form.Control
                    value={formModello}
                    onChange={(e) => setFormModello(e.target.value)}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Serie / Matricola</Form.Label>
                  <Form.Control
                    value={formSerieMatricola}
                    onChange={(e) => setFormSerieMatricola(e.target.value)}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Reparto</Form.Label>
                  <Form.Select
                    value={formWard}
                    onChange={(e) => setFormWard(e.target.value ? Number(e.target.value) : '')}
                  >
                    <option value="">-- Seleziona --</option>
                    {wards.map((w) => (
                      <option key={w.id} value={w.id}>
                        {w.description}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Responsabile</Form.Label>
                  <Form.Select
                    value={formHR}
                    onChange={(e) => setFormHR(e.target.value ? Number(e.target.value) : '')}
                  >
                    <option value="">-- Seleziona --</option>
                    {dipendenti.map((d) => (
                      <option key={d.id} value={d.id}>
                        {d.full_name || `${d.cognomedipendente} ${d.nomedipendente}`}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Check
                    type="checkbox"
                    label="Attrezzatura dismessa"
                    checked={formIsDismesso}
                    onChange={(e) => setFormIsDismesso(e.target.checked)}
                  />
                </Form.Group>
                {formIsDismesso && (
                  <Form.Group className="mb-3">
                    <Form.Label>Data Dismissione</Form.Label>
                    <Form.Control
                      type="date"
                      value={formDataDismissione}
                      onChange={(e) => setFormDataDismissione(e.target.value)}
                    />
                  </Form.Group>
                )}
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Check
                    type="checkbox"
                    label="Richiede taratura"
                    checked={formIsTaratura}
                    onChange={(e) => setFormIsTaratura(e.target.checked)}
                  />
                </Form.Group>
                {formIsTaratura && (
                  <Form.Group className="mb-3">
                    <Form.Label>Periodo Taratura (mesi)</Form.Label>
                    <Form.Control
                      type="number"
                      value={formPeriodoTaratura}
                      onChange={(e) =>
                        setFormPeriodoTaratura(e.target.value ? Number(e.target.value) : '')
                      }
                      min="1"
                    />
                  </Form.Group>
                )}
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Procedura Controlli Periodici</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                value={formProceduraControlli}
                onChange={(e) => setFormProceduraControlli(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Periodo Controlli Periodici (mesi)</Form.Label>
              <Form.Control
                type="number"
                value={formPeriodoControlli}
                onChange={(e) =>
                  setFormPeriodoControlli(e.target.value ? Number(e.target.value) : '')
                }
                min="1"
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Riferimento Normativo Controlli Periodici</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                value={formRiferimentoNormativo}
                onChange={(e) => setFormRiferimentoNormativo(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Immagine</Form.Label>
              <Form.Control
                type="file"
                accept="image/*"
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                  const file = e.target.files?.[0] || null;
                  setFormImage(file);
                }}
              />
              <Form.Text className="text-muted">Formati supportati: JPG, PNG</Form.Text>
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
            <Button variant="secondary" onClick={() => setShowModal(false)} disabled={saving}>
              Annulla
            </Button>
            <Button variant="primary" type="submit" disabled={saving}>
              {saving ? <Spinner animation="border" size="sm" /> : 'Salva'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal show={showDeleteModal} onHide={handleDeleteCancel} centered>
        <Modal.Header closeButton>
          <Modal.Title>Conferma eliminazione</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Sei sicuro di voler eliminare questa attrezzatura?
          <br />
          <small className="text-muted">
            Verranno eliminati anche tutti i record di manutenzioni, tarature e controlli associati.
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
    </Container>
  );
}
