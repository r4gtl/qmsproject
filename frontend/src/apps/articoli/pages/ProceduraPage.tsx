/**
 * ProceduraPage - Pagina dedicata per visualizzare/modificare una procedura
 *
 * Route: /articoli/:articoloId/procedure/:proceduraId
 */
import { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Form,
  Button,
  Spinner,
  Row,
  Col,
  Badge,
  ButtonGroup,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import {
  getProcedura,
  updateProcedura,
  deleteProcedura,
  cloneProcedura,
} from '../api/procedure';
import type { ProceduraDetail, DettaglioProcedura } from '../types/procedure';
import { DettagliTable, DettaglioModal } from '../components/Procedure';

export default function ProceduraPage() {
  const { articoloId, proceduraId } = useParams<{
    articoloId: string;
    proceduraId: string;
  }>();
  const navigate = useNavigate();

  // Data state
  const [procedura, setProcedura] = useState<ProceduraDetail | null>(null);
  const [dettagli, setDettagli] = useState<DettaglioProcedura[]>([]);

  // Form state
  const [note, setNote] = useState('');
  const [dataRevisione, setDataRevisione] = useState('');

  // UI state
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [cloning, setCloning] = useState(false);

  // Modal state
  const [showDettaglioModal, setShowDettaglioModal] = useState(false);
  const [selectedDettaglioId, setSelectedDettaglioId] = useState<number | null>(
    null
  );

  // Carica procedura
  const fetchProcedura = useCallback(async () => {
    if (!proceduraId) return;
    try {
      setLoading(true);
      const res = await getProcedura(Number(proceduraId));
      const p = res.data;
      setProcedura(p);
      setDettagli(p.dettagli || []);
      setNote(p.note || '');
      setDataRevisione(p.data_revisione);
    } catch {
      toast.error('Errore caricamento procedura');
      navigate(`/articoli/${articoloId}`);
    } finally {
      setLoading(false);
    }
  }, [proceduraId, articoloId, navigate]);

  useEffect(() => {
    fetchProcedura();
  }, [fetchProcedura]);

  // Salva modifiche (note e data revisione)
  const handleSave = async () => {
    if (!proceduraId) return;
    try {
      setSaving(true);
      await updateProcedura(Number(proceduraId), {
        note,
        data_revisione: dataRevisione,
      });
      toast.success('Procedura salvata');
    } catch {
      toast.error('Errore salvataggio');
    } finally {
      setSaving(false);
    }
  };

  // Elimina procedura
  const handleDelete = async () => {
    if (!proceduraId) return;
    if (
      !confirm(
        'Eliminare questa procedura e tutte le sue righe? Azione irreversibile.'
      )
    )
      return;
    try {
      await deleteProcedura(Number(proceduraId));
      toast.success('Procedura eliminata');
      navigate(`/articoli/${articoloId}`);
    } catch {
      toast.error('Errore eliminazione');
    }
  };

  // Clona come nuova revisione
  const handleClone = async () => {
    if (!proceduraId) return;
    if (!confirm('Creare una nuova revisione clonando questa procedura?'))
      return;
    try {
      setCloning(true);
      const res = await cloneProcedura(Number(proceduraId));
      toast.success(`Creata Rev. ${res.data.nr_revisione}`);
      // Naviga alla nuova revisione
      navigate(`/articoli/${articoloId}/procedure/${res.data.id}`);
    } catch {
      toast.error('Errore clonazione');
    } finally {
      setCloning(false);
    }
  };

  // Callback per cambio dettagli (da DettagliTable)
  const handleDettagliChange = (newDettagli: DettaglioProcedura[]) => {
    setDettagli(newDettagli);
  };

  // Apri modal per nuova riga
  const handleAddDettaglio = () => {
    setSelectedDettaglioId(null);
    setShowDettaglioModal(true);
  };

  // Apri modal per modifica riga
  const handleRowClick = (det: DettaglioProcedura) => {
    setSelectedDettaglioId(det.id);
    setShowDettaglioModal(true);
  };

  // Callback dopo salvataggio nel modal
  const handleDettaglioSaved = () => {
    fetchProcedura(); // Ricarica tutto per avere dati aggiornati
  };

  // Formatta data
  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('it-IT');
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" />
        <p className="mt-2">Caricamento procedura...</p>
      </div>
    );
  }

  if (!procedura) {
    return (
      <div className="text-center py-5">
        <p>Procedura non trovata.</p>
        <Button onClick={() => navigate(`/articoli/${articoloId}`)}>
          Torna all'articolo
        </Button>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <Button
            variant="link"
            className="p-0 mb-2"
            onClick={() => navigate(`/articoli/${articoloId}`)}
          >
            ← Torna all'articolo
          </Button>
          <h4 className="mb-0">
            Procedura{' '}
            <Badge bg="primary" className="me-2">
              Nr. {procedura.nr_procedura}
            </Badge>
            <Badge bg="info">Rev. {procedura.nr_revisione}</Badge>
          </h4>
          <small className="text-muted">
            Articolo: {procedura.fk_articolo_descrizione}
          </small>
        </div>
        <ButtonGroup>
          <Button
            variant="outline-primary"
            onClick={handleClone}
            disabled={cloning}
          >
            {cloning ? <Spinner animation="border" size="sm" /> : 'Clona Revisione'}
          </Button>
          <Button variant="outline-danger" onClick={handleDelete}>
            Elimina
          </Button>
        </ButtonGroup>
      </div>

      {/* Card intestazione */}
      <Card className="mb-4">
        <Card.Header>
          <strong>Intestazione Procedura</strong>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={3}>
              <Form.Group className="mb-3">
                <Form.Label>Nr. Procedura</Form.Label>
                <Form.Control value={procedura.nr_procedura} disabled />
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group className="mb-3">
                <Form.Label>Data Procedura</Form.Label>
                <Form.Control
                  value={formatDate(procedura.data_procedura)}
                  disabled
                />
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group className="mb-3">
                <Form.Label>Nr. Revisione</Form.Label>
                <Form.Control value={procedura.nr_revisione} disabled />
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group className="mb-3">
                <Form.Label>Data Revisione</Form.Label>
                <Form.Control
                  type="date"
                  value={dataRevisione}
                  onChange={(e) => setDataRevisione(e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col>
              <Form.Group className="mb-3">
                <Form.Label>Note</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={2}
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>
          <div className="text-end">
            <Button
              variant="primary"
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? (
                <Spinner animation="border" size="sm" />
              ) : (
                'Salva Intestazione'
              )}
            </Button>
          </div>
        </Card.Body>
      </Card>

      {/* Tabella dettagli */}
      <Card>
        <Card.Body>
          <DettagliTable
            proceduraId={Number(proceduraId)}
            dettagli={dettagli}
            onDettagliChange={handleDettagliChange}
            onRowClick={handleRowClick}
            onAddClick={handleAddDettaglio}
          />
        </Card.Body>
      </Card>

      {/* Modal dettaglio */}
      <DettaglioModal
        show={showDettaglioModal}
        onHide={() => setShowDettaglioModal(false)}
        proceduraId={Number(proceduraId)}
        dettaglioId={selectedDettaglioId}
        onSave={handleDettaglioSaved}
      />
    </div>
  );
}
