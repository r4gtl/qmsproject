/**
 * Manuale Procedure - Dettaglio Modulo
 */
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Card, Row, Col, Table, Button, Form, Modal, ButtonGroup } from 'react-bootstrap';
import { toast } from 'react-toastify';
import { FaEdit, FaTrash } from 'react-icons/fa';
import {
  getModulo,
  updateModulo,
  getRevisioniModulo,
  createRevisioneModulo,
  updateRevisioneModulo,
  deleteRevisioneModulo,
} from '../api/manualeprocedureApi';
import type { Modulo, RevisioneModulo } from '../types';

const ModuloDetailPage = () => {
  const { id } = useParams<{ id: string }>();

  // Modulo state
  const [modulo, setModulo] = useState<Modulo | null>(null);

  // Edit modulo form
  const [editMode, setEditMode] = useState(false);
  const [formIdentificativo, setFormIdentificativo] = useState('');
  const [formDataModulo, setFormDataModulo] = useState('');
  const [formDescrizione, setFormDescrizione] = useState('');
  const [formNote, setFormNote] = useState('');

  // Revisioni state
  const [revisioni, setRevisioni] = useState<RevisioneModulo[]>([]);
  const [showRevModal, setShowRevModal] = useState(false);
  const [editingRev, setEditingRev] = useState<RevisioneModulo | null>(null);
  const [revNRevisione, setRevNRevisione] = useState<number>(1);
  const [revDataRevisione, setRevDataRevisione] = useState('');
  const [revDocumento, setRevDocumento] = useState<File | null>(null);
  const [revNote, setRevNote] = useState('');

  // Delete modal
  const [showDeleteRev, setShowDeleteRev] = useState(false);
  const [deleteRevId, setDeleteRevId] = useState<number | null>(null);

  // Load data
  useEffect(() => {
    if (!id) return;
    getModulo(Number(id))
      .then((res) => {
        setModulo(res.data);
        setFormIdentificativo(res.data.identificativo);
        setFormDataModulo(res.data.data_modulo);
        setFormDescrizione(res.data.descrizione);
        setFormNote(res.data.note || '');
      })
      .catch((err) => {
        console.error('Error loading modulo:', err);
        toast.error('Errore caricamento modulo');
      });

    fetchRevisioni();
  }, [id]);

  const fetchRevisioni = () => {
    if (!id) return;
    getRevisioniModulo({ fk_modulo: id })
      .then((res) => setRevisioni(res.data.results))
      .catch((err) => console.error('Error loading revisioni:', err));
  };

  // Save modulo
  const handleSaveModulo = (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    updateModulo(Number(id), {
      identificativo: formIdentificativo,
      data_modulo: formDataModulo,
      descrizione: formDescrizione,
      note: formNote,
    })
      .then((res) => {
        setModulo(res.data);
        setEditMode(false);
        toast.success('Modulo aggiornato');
      })
      .catch((err) => {
        console.error('Error updating modulo:', err);
        toast.error('Errore aggiornamento modulo');
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

  const handleEditRevisione = (rev: RevisioneModulo) => {
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
    formData.append('fk_modulo', id);
    formData.append('n_revisione', String(revNRevisione));
    formData.append('data_revisione', revDataRevisione);
    if (revDocumento) formData.append('documento', revDocumento);
    formData.append('note', revNote);

    const promise = editingRev
      ? updateRevisioneModulo(editingRev.id, formData)
      : createRevisioneModulo(formData);

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
    deleteRevisioneModulo(deleteRevId)
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

  if (!modulo) return <Container className="mt-4">Caricamento...</Container>;

  return (
    <Container className="mt-4">
      <h2>Dettaglio Modulo</h2>

      {/* Modulo Info Card */}
      <Card className="mb-4">
        <Card.Header>
          <div className="d-flex justify-content-between align-items-center">
            <span>Informazioni Modulo</span>
            <Button size="sm" onClick={() => setEditMode(!editMode)}>
              {editMode ? 'Annulla' : 'Modifica'}
            </Button>
          </div>
        </Card.Header>
        <Card.Body>
          {editMode ? (
            <Form onSubmit={handleSaveModulo}>
              <Row>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Identificativo</Form.Label>
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
                    <Form.Label>Data Modulo</Form.Label>
                    <Form.Control
                      type="date"
                      value={formDataModulo}
                      onChange={(e) => setFormDataModulo(e.target.value)}
                      required
                    />
                  </Form.Group>
                </Col>
              </Row>
              <Form.Group className="mb-3">
                <Form.Label>Descrizione</Form.Label>
                <Form.Control
                  type="text"
                  value={formDescrizione}
                  onChange={(e) => setFormDescrizione(e.target.value)}
                  required
                />
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
              <Button type="submit" variant="primary">
                Salva
              </Button>
            </Form>
          ) : (
            <Row>
              <Col md={6}>
                <p>
                  <strong>Identificativo:</strong> {modulo.identificativo}
                </p>
                <p>
                  <strong>Data modulo:</strong>{' '}
                  {new Date(modulo.data_modulo).toLocaleDateString('it-IT')}
                </p>
              </Col>
              <Col md={6}>
                <p>
                  <strong>Descrizione:</strong> {modulo.descrizione}
                </p>
                <p>
                  <strong>Procedura:</strong> {modulo.fk_procedura_display}
                </p>
              </Col>
              {modulo.note && (
                <Col md={12}>
                  <p>
                    <strong>Note:</strong> {modulo.note}
                  </p>
                </Col>
              )}
            </Row>
          )}
        </Card.Body>
      </Card>

      {/* Revisioni Modulo */}
      <Card>
        <Card.Header>
          <div className="d-flex justify-content-between align-items-center">
            <span>Revisioni Modulo</span>
            <Button size="sm" onClick={handleAddRevisione}>
              + Aggiungi Revisione
            </Button>
          </div>
        </Card.Header>
        <Card.Body>
          <Table striped hover responsive>
            <thead>
              <tr>
                <th>N. Revisione</th>
                <th>Data</th>
                <th>Documento</th>
                <th>Note</th>
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
                  <td>{rev.note || '—'}</td>
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
                  <td colSpan={5} className="text-center text-muted">
                    Nessuna revisione presente
                  </td>
                </tr>
              )}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

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

      {/* Delete Modal */}
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
    </Container>
  );
};

export default ModuloDetailPage;
