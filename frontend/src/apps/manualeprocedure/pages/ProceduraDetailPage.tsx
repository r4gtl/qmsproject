/**
 * Manuale Procedure - Dettaglio Procedura
 */
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Card,
  Row,
  Col,
  Table,
  Button,
  Form,
  Modal,
  ButtonGroup,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import { FaEdit, FaTrash } from 'react-icons/fa';
import {
  getProcedura,
  updateProcedura,
  getSezioniLWG,
  getRevisioniProcedura,
  createRevisioneProcedura,
  updateRevisioneProcedura,
  deleteRevisioneProcedura,
  getModuli,
  createModulo,
  updateModulo,
  deleteModulo,
} from '../api/manualeprocedureApi';
import type { Procedura, SezioneLWG, RevisioneProcedura, Modulo } from '../types';

const ProceduraDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  // Procedura state
  const [procedura, setProcedura] = useState<Procedura | null>(null);
  const [sezioni, setSezioni] = useState<SezioneLWG[]>([]);

  // Edit procedura form
  const [editMode, setEditMode] = useState(false);
  const [formIdentificativo, setFormIdentificativo] = useState('');
  const [formDataProcedura, setFormDataProcedura] = useState('');
  const [formDescrizione, setFormDescrizione] = useState('');
  const [formSezione, setFormSezione] = useState<number | ''>('');
  const [formNote, setFormNote] = useState('');

  // Revisioni state
  const [revisioni, setRevisioni] = useState<RevisioneProcedura[]>([]);
  const [showRevModal, setShowRevModal] = useState(false);
  const [editingRev, setEditingRev] = useState<RevisioneProcedura | null>(null);
  const [revNRevisione, setRevNRevisione] = useState<number>(1);
  const [revDataRevisione, setRevDataRevisione] = useState('');
  const [revDocumento, setRevDocumento] = useState<File | null>(null);
  const [revNote, setRevNote] = useState('');

  // Moduli state
  const [moduli, setModuli] = useState<Modulo[]>([]);
  const [showModModal, setShowModModal] = useState(false);
  const [editingMod, setEditingMod] = useState<Modulo | null>(null);
  const [modIdentificativo, setModIdentificativo] = useState('');
  const [modDataModulo, setModDataModulo] = useState('');
  const [modDescrizione, setModDescrizione] = useState('');
  const [modNote, setModNote] = useState('');

  // Delete modals
  const [showDeleteRev, setShowDeleteRev] = useState(false);
  const [deleteRevId, setDeleteRevId] = useState<number | null>(null);
  const [showDeleteMod, setShowDeleteMod] = useState(false);
  const [deleteModId, setDeleteModId] = useState<number | null>(null);

  // Load data
  useEffect(() => {
    if (!id) return;
    getProcedura(Number(id))
      .then((res) => {
        setProcedura(res.data);
        setFormIdentificativo(res.data.identificativo);
        setFormDataProcedura(res.data.data_procedura);
        setFormDescrizione(res.data.descrizione);
        setFormSezione(res.data.fk_lwgsection || '');
        setFormNote(res.data.note || '');
      })
      .catch((err) => {
        console.error('Error loading procedura:', err);
        toast.error('Errore caricamento procedura');
      });

    getSezioniLWG()
      .then((res) => setSezioni(res.data))
      .catch((err) => console.error('Error loading sezioni:', err));

    fetchRevisioni();
    fetchModuli();
  }, [id]);

  const fetchRevisioni = () => {
    if (!id) return;
    getRevisioniProcedura({ fk_procedura: id })
      .then((res) => setRevisioni(res.data.results))
      .catch((err) => console.error('Error loading revisioni:', err));
  };

  const fetchModuli = () => {
    if (!id) return;
    getModuli({ fk_procedura: id })
      .then((res) => setModuli(res.data.results))
      .catch((err) => console.error('Error loading moduli:', err));
  };

  // Save procedura
  const handleSaveProcedura = (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    updateProcedura(Number(id), {
      identificativo: formIdentificativo,
      data_procedura: formDataProcedura,
      descrizione: formDescrizione,
      fk_lwgsection: formSezione || null,
      note: formNote,
    })
      .then((res) => {
        setProcedura(res.data);
        setEditMode(false);
        toast.success('Procedura aggiornata');
      })
      .catch((err) => {
        console.error('Error updating procedura:', err);
        toast.error('Errore aggiornamento procedura');
      });
  };

  // Revisione handlers
  const handleAddRevisione = () => {
    setEditingRev(null);
    setRevNRevisione(1);
    setRevDataRevisione('');
    setRevDocumento(null);
    setRevNote('');
    setShowRevModal(true);
  };

  const handleEditRevisione = (rev: RevisioneProcedura) => {
    setEditingRev(rev);
    setRevNRevisione(rev.n_revisione);
    setRevDataRevisione(rev.data_revisione);
    setRevDocumento(null);
    setRevNote(rev.note || '');
    setShowRevModal(true);
  };

  const handleSaveRevisione = (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;

    const formData = new FormData();
    formData.append('fk_procedura', id);
    formData.append('n_revisione', String(revNRevisione));
    formData.append('data_revisione', revDataRevisione);
    if (revDocumento) formData.append('documento', revDocumento);
    formData.append('note', revNote);

    const promise = editingRev
      ? updateRevisioneProcedura(editingRev.id, formData)
      : createRevisioneProcedura(formData);

    promise
      .then(() => {
        toast.success(editingRev ? 'Revisione aggiornata' : 'Revisione creata');
        setShowRevModal(false);
        fetchRevisioni();
      })
      .catch((err) => {
        console.error('Error saving revisione:', err);
        toast.error('Errore salvataggio revisione');
      });
  };

  const handleDeleteRevConfirm = () => {
    if (!deleteRevId) return;
    deleteRevisioneProcedura(deleteRevId)
      .then(() => {
        toast.success('Revisione eliminata');
        setShowDeleteRev(false);
        fetchRevisioni();
      })
      .catch((err) => {
        console.error('Error deleting revisione:', err);
        toast.error('Errore eliminazione revisione');
      });
  };

  // Modulo handlers
  const handleAddModulo = () => {
    setEditingMod(null);
    setModIdentificativo('');
    setModDataModulo('');
    setModDescrizione('');
    setModNote('');
    setShowModModal(true);
  };

  const handleEditModulo = (mod: Modulo) => {
    setEditingMod(mod);
    setModIdentificativo(mod.identificativo);
    setModDataModulo(mod.data_modulo);
    setModDescrizione(mod.descrizione);
    setModNote(mod.note || '');
    setShowModModal(true);
  };

  const handleSaveModulo = (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;

    const data = {
      fk_procedura: Number(id),
      identificativo: modIdentificativo,
      data_modulo: modDataModulo,
      descrizione: modDescrizione,
      note: modNote,
    };

    const promise = editingMod ? updateModulo(editingMod.id, data) : createModulo(data);

    promise
      .then(() => {
        toast.success(editingMod ? 'Modulo aggiornato' : 'Modulo creato');
        setShowModModal(false);
        fetchModuli();
      })
      .catch((err) => {
        console.error('Error saving modulo:', err);
        toast.error('Errore salvataggio modulo');
      });
  };

  const handleDeleteModConfirm = () => {
    if (!deleteModId) return;
    deleteModulo(deleteModId)
      .then(() => {
        toast.success('Modulo eliminato');
        setShowDeleteMod(false);
        fetchModuli();
      })
      .catch((err) => {
        console.error('Error deleting modulo:', err);
        toast.error('Errore eliminazione modulo');
      });
  };

  if (!procedura) return <Container className="mt-4">Caricamento...</Container>;

  return (
    <Container className="mt-4">
      <h2>Dettaglio Procedura</h2>

      {/* Procedura Info Card */}
      <Card className="mb-4">
        <Card.Header>
          <div className="d-flex justify-content-between align-items-center">
            <span>Informazioni Procedura</span>
            <Button size="sm" onClick={() => setEditMode(!editMode)}>
              {editMode ? 'Annulla' : 'Modifica'}
            </Button>
          </div>
        </Card.Header>
        <Card.Body>
          {editMode ? (
            <Form onSubmit={handleSaveProcedura}>
              <Row>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Numero procedura</Form.Label>
                    <Form.Control
                      type="text"
                      value={formIdentificativo}
                      onChange={(e) => setFormIdentificativo(e.target.value)}
                      required
                    />
                  </Form.Group>
                </Col>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Data procedura</Form.Label>
                    <Form.Control
                      type="date"
                      value={formDataProcedura}
                      onChange={(e) => setFormDataProcedura(e.target.value)}
                      required
                    />
                  </Form.Group>
                </Col>
              </Row>
              <Row>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Descrizione</Form.Label>
                    <Form.Control
                      type="text"
                      value={formDescrizione}
                      onChange={(e) => setFormDescrizione(e.target.value)}
                      required
                    />
                  </Form.Group>
                </Col>
                <Col md={6}>
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
                </Col>
              </Row>
              <Form.Group className="mb-3">
                <Form.Label>Note</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  value={formNote}
                  onChange={(e) => setFormNote(e.target.value)}
                />
              </Form.Group>
              <Button type="submit" variant="primary">
                Salva
              </Button>
            </Form>
          ) : (
            <Row>
              <Col md={6}>
                <p>
                  <strong>Numero procedura:</strong> {procedura.identificativo}
                </p>
                <p>
                  <strong>Data procedura:</strong>{' '}
                  {new Date(procedura.data_procedura).toLocaleDateString('it-IT')}
                </p>
              </Col>
              <Col md={6}>
                <p>
                  <strong>Descrizione:</strong> {procedura.descrizione}
                </p>
                <p>
                  <strong>Sezione LWG:</strong> {procedura.fk_lwgsection_display || '—'}
                </p>
              </Col>
              {procedura.note && (
                <Col md={12}>
                  <p>
                    <strong>Note:</strong> {procedura.note}
                  </p>
                </Col>
              )}
            </Row>
          )}
        </Card.Body>
      </Card>

      {/* Revisioni + Moduli in 2x2 grid */}
      <Row className="g-4">
        {/* Revisioni Procedura */}
        <Col md={6}>
          <Card style={{ height: '450px' }}>
            <Card.Header>
              <div className="d-flex justify-content-between align-items-center">
                <span>Revisioni Procedura</span>
                <Button size="sm" onClick={handleAddRevisione}>
                  + Aggiungi
                </Button>
              </div>
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '380px' }}>
              <Table size="sm" striped hover>
                <thead>
                  <tr>
                    <th>N.</th>
                    <th>Data</th>
                    <th>Doc</th>
                    <th>Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  {revisioni.map((rev) => (
                    <tr key={rev.id}>
                      <td>{rev.n_revisione}</td>
                      <td>{new Date(rev.data_revisione).toLocaleDateString('it-IT')}</td>
                      <td>
                        {rev.documento ? (
                          <a href={rev.documento} target="_blank" rel="noopener noreferrer">
                            📄 PDF
                          </a>
                        ) : (
                          '—'
                        )}
                      </td>
                      <td>
                        <ButtonGroup size="sm">
                          <Button variant="outline-primary" onClick={() => handleEditRevisione(rev)}>
                            <FaEdit />
                          </Button>
                          <Button
                            variant="outline-danger"
                            onClick={() => {
                              setDeleteRevId(rev.id);
                              setShowDeleteRev(true);
                            }}
                          >
                            <FaTrash />
                          </Button>
                        </ButtonGroup>
                      </td>
                    </tr>
                  ))}
                  {revisioni.length === 0 && (
                    <tr>
                      <td colSpan={4} className="text-center text-muted">
                        Nessuna revisione presente
                      </td>
                    </tr>
                  )}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>

        {/* Moduli */}
        <Col md={6}>
          <Card style={{ height: '450px' }}>
            <Card.Header>
              <div className="d-flex justify-content-between align-items-center">
                <span>Moduli</span>
                <Button size="sm" onClick={handleAddModulo}>
                  + Aggiungi
                </Button>
              </div>
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '380px' }}>
              <Table
                size="sm"
                striped
                hover
                responsive
                style={{ cursor: 'pointer' }}
              >
                <thead>
                  <tr>
                    <th>N.</th>
                    <th>Data</th>
                    <th>Descrizione</th>
                    <th>Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  {moduli.map((mod) => (
                    <tr
                      key={mod.id}
                      onClick={() => navigate(`/manualeprocedure/moduli/${mod.id}`)}
                    >
                      <td>{mod.identificativo}</td>
                      <td>{new Date(mod.data_modulo).toLocaleDateString('it-IT')}</td>
                      <td>{mod.descrizione}</td>
                      <td>
                        <ButtonGroup size="sm">
                          <Button
                            variant="outline-primary"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleEditModulo(mod);
                            }}
                          >
                            <FaEdit />
                          </Button>
                          <Button
                            variant="outline-danger"
                            onClick={(e) => {
                              e.stopPropagation();
                              setDeleteModId(mod.id);
                              setShowDeleteMod(true);
                            }}
                          >
                            <FaTrash />
                          </Button>
                        </ButtonGroup>
                      </td>
                    </tr>
                  ))}
                  {moduli.length === 0 && (
                    <tr>
                      <td colSpan={4} className="text-center text-muted">
                        Nessun modulo presente
                      </td>
                    </tr>
                  )}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Revisione Modal */}
      <Modal show={showRevModal} onHide={() => setShowRevModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>{editingRev ? 'Modifica Revisione' : 'Nuova Revisione'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSaveRevisione}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>N. Revisione</Form.Label>
              <Form.Control
                type="number"
                value={revNRevisione}
                onChange={(e) => setRevNRevisione(Number(e.target.value))}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Data Revisione</Form.Label>
              <Form.Control
                type="date"
                value={revDataRevisione}
                onChange={(e) => setRevDataRevisione(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Documento</Form.Label>
              <Form.Control
                type="file"
                accept=".pdf"
                onChange={(e) => {
                  const files = (e.target as HTMLInputElement).files;
                  setRevDocumento(files ? files[0] : null);
                }}
              />
              {editingRev?.documento && <small>Attuale: {editingRev.documento}</small>}
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={revNote}
                onChange={(e) => setRevNote(e.target.value)}
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowRevModal(false)}>
              Annulla
            </Button>
            <Button type="submit" variant="primary">
              Salva
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      {/* Modulo Modal */}
      <Modal show={showModModal} onHide={() => setShowModModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>{editingMod ? 'Modifica Modulo' : 'Nuovo Modulo'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSaveModulo}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>Identificativo</Form.Label>
              <Form.Control
                type="text"
                value={modIdentificativo}
                onChange={(e) => setModIdentificativo(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Data Modulo</Form.Label>
              <Form.Control
                type="date"
                value={modDataModulo}
                onChange={(e) => setModDataModulo(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Descrizione</Form.Label>
              <Form.Control
                type="text"
                value={modDescrizione}
                onChange={(e) => setModDescrizione(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={modNote}
                onChange={(e) => setModNote(e.target.value)}
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModModal(false)}>
              Annulla
            </Button>
            <Button type="submit" variant="primary">
              Salva
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>

      {/* Delete Modals */}
      <Modal show={showDeleteRev} onHide={() => setShowDeleteRev(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Conferma eliminazione</Modal.Title>
        </Modal.Header>
        <Modal.Body>Sei sicuro di voler eliminare questa revisione?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDeleteRev(false)}>
            Annulla
          </Button>
          <Button variant="danger" onClick={handleDeleteRevConfirm}>
            Elimina
          </Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showDeleteMod} onHide={() => setShowDeleteMod(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Conferma eliminazione</Modal.Title>
        </Modal.Header>
        <Modal.Body>Sei sicuro di voler eliminare questo modulo?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDeleteMod(false)}>
            Annulla
          </Button>
          <Button variant="danger" onClick={handleDeleteModConfirm}>
            Elimina
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default ProceduraDetailPage;
