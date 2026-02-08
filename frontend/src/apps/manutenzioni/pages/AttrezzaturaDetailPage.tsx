/**
 * AttrezzaturaDetailPage - Dettaglio attrezzatura con 4 tabelle figlie
 *
 * Layout:
 * - Info attrezzatura (top)
 * - 4 card in 2x2 grid:
 *   1. Manutenzioni Straordinarie
 *   2. Manutenzioni Ordinarie
 *   3. Tarature
 *   4. Controlli Periodici
 */
import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Row,
  Col,
  Card,
  Button,
  Spinner,
  Badge,
  Alert,
  Table,
  Modal,
  Form,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import {
  FaCog,
  FaArrowLeft,
  FaWrench,
  FaTools,
  FaBalanceScale,
  FaCheckCircle,
} from 'react-icons/fa';
import {
  getAttrezzatura,
  getManutenzioniStraordinarie,
  createManutenzioneStraordinaria,
  updateManutenzioneStraordinaria,
  deleteManutenzioneStraordinaria,
  getManutenzioniOrdinarie,
  createManutenzioneOrdinaria,
  updateManutenzioneOrdinaria,
  deleteManutenzioneOrdinaria,
  getTarature,
  createTaratura,
  updateTaratura,
  deleteTaratura,
  getControlliPeriodici,
  createControlloPeriodico,
  updateControlloPeriodico,
  deleteControlloPeriodico,
  getFornitoriForSelect,
  getDipendentiForSelect,
} from '../api/manutenzioniApi';
import type {
  AttrezzaturaDetail,
  ManutenzioneStraordinaria,
  ManutenzioneOrdinaria,
  Taratura,
  ControlloPeriodico,
  Fornitore,
  HumanResource,
} from '../types';
import { extractErrorMessage } from '../utils/drfErrors';

export default function AttrezzaturaDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [attrezzatura, setAttrezzatura] = useState<AttrezzaturaDetail | null>(null);
  const [loading, setLoading] = useState(true);

  // Lookups
  const [fornitori, setFornitori] = useState<Fornitore[]>([]);
  const [dipendenti, setDipendenti] = useState<HumanResource[]>([]);

  const loadAttrezzatura = useCallback(async () => {
    if (!id) return;
    try {
      setLoading(true);
      const [attrRes, fornRes, dipRes] = await Promise.all([
        getAttrezzatura(Number(id)),
        getFornitoriForSelect(),
        getDipendentiForSelect(),
      ]);
      setAttrezzatura(attrRes.data);
      setFornitori(fornRes.data.results);
      setDipendenti(dipRes.data.results);
    } catch {
      toast.error('Errore caricamento attrezzatura');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    loadAttrezzatura();
  }, [loadAttrezzatura]);

  if (loading) {
    return (
      <Container className="my-4 text-center">
        <Spinner animation="border" />
        <p className="mt-2 text-muted">Caricamento...</p>
      </Container>
    );
  }

  if (!attrezzatura) {
    return (
      <Container className="my-4">
        <Alert variant="danger">Attrezzatura non trovata</Alert>
        <Button variant="secondary" onClick={() => navigate('/manutenzioni/attrezzature')}>
          <FaArrowLeft className="me-1" /> Torna alla lista
        </Button>
      </Container>
    );
  }

  return (
    <Container className="my-4">
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h3>
          <FaCog className="me-2" />
          {attrezzatura.codice_attrezzatura} - {attrezzatura.descrizione}
        </h3>
        <Button variant="secondary" size="sm" onClick={() => navigate('/manutenzioni/attrezzature')}>
          <FaArrowLeft className="me-1" /> Torna alla lista
        </Button>
      </div>

      {/* Info Attrezzatura Card */}
      <Card className="mb-4 shadow-sm">
        <Card.Header>
          <strong>Informazioni Attrezzatura</strong>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={6}>
              <p>
                <strong>Codice:</strong> {attrezzatura.codice_attrezzatura}
              </p>
              <p>
                <strong>Descrizione:</strong> {attrezzatura.descrizione}
              </p>
              <p>
                <strong>Modello:</strong> {attrezzatura.modello || '—'}
              </p>
              <p>
                <strong>Serie/Matricola:</strong> {attrezzatura.serie_matricola || '—'}
              </p>
              <p>
                <strong>Reparto:</strong> {attrezzatura.fk_ward_display || '—'}
              </p>
            </Col>
            <Col md={6}>
              <p>
                <strong>Responsabile:</strong> {attrezzatura.fk_human_resource_display || '—'}
              </p>
              <p>
                <strong>Dismesso:</strong>{' '}
                {attrezzatura.is_dismesso ? (
                  <Badge bg="danger">Sì</Badge>
                ) : (
                  <Badge bg="success">No</Badge>
                )}
                {attrezzatura.data_dismissione && (
                  <span className="ms-2">
                    ({new Date(attrezzatura.data_dismissione).toLocaleDateString('it-IT')})
                  </span>
                )}
              </p>
              <p>
                <strong>Richiede Taratura:</strong>{' '}
                {attrezzatura.is_taratura ? (
                  <Badge bg="info">Sì</Badge>
                ) : (
                  <Badge bg="secondary">No</Badge>
                )}
                {attrezzatura.periodo_taratura && (
                  <span className="ms-2">({attrezzatura.periodo_taratura} mesi)</span>
                )}
              </p>
              <p>
                <strong>Periodo Controlli:</strong>{' '}
                {attrezzatura.periodo_controlli_periodici
                  ? `${attrezzatura.periodo_controlli_periodici} mesi`
                  : '—'}
              </p>
            </Col>
          </Row>
          {attrezzatura.note && (
            <p className="mb-0">
              <strong>Note:</strong> {attrezzatura.note}
            </p>
          )}
        </Card.Body>
      </Card>

      {/* 4 Tabelle Figlie - Layout 2x2 */}
      <Row className="g-4">
        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaWrench className="me-2" />
              Manutenzioni Straordinarie
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <ManutenzioniStraordinarieCard
                attrezzaturaId={Number(id)}
                fornitori={fornitori}
              />
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaTools className="me-2" />
              Manutenzioni Ordinarie
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <ManutenzioniOrdinarieCard attrezzaturaId={Number(id)} fornitori={fornitori} />
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaBalanceScale className="me-2" />
              Tarature
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <TaratureCard attrezzaturaId={Number(id)} fornitori={fornitori} />
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaCheckCircle className="me-2" />
              Controlli Periodici
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <ControlliPeriodiciCard attrezzaturaId={Number(id)} dipendenti={dipendenti} />
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

// =============================================================================
// MANUTENZIONI STRAORDINARIE CARD
// =============================================================================

interface ManutenzioniStraordinarieCardProps {
  attrezzaturaId: number;
  fornitori: Fornitore[];
}

function ManutenzioniStraordinarieCard({
  attrezzaturaId,
  fornitori,
}: ManutenzioniStraordinarieCardProps) {
  const [items, setItems] = useState<ManutenzioneStraordinaria[]>([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<ManutenzioneStraordinaria | null>(null);
  const [saving, setSaving] = useState(false);

  // Form fields
  const [formData, setFormData] = useState('');
  const [formDescrizione, setFormDescrizione] = useState('');
  const [formImporto, setFormImporto] = useState('');
  const [formOreFermo, setFormOreFermo] = useState('');
  const [formFornitore, setFormFornitore] = useState<number | ''>('');
  const [formFtProt, setFormFtProt] = useState('');
  const [formDataFattura, setFormDataFattura] = useState('');
  const [formNote, setFormNote] = useState('');

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getManutenzioniStraordinarie({
        fk_attrezzatura: attrezzaturaId,
        page_size: 1000,
      });
      setItems(res.data.results);
    } catch {
      toast.error('Errore caricamento manutenzioni straordinarie');
    } finally {
      setLoading(false);
    }
  }, [attrezzaturaId]);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormData('');
    setFormDescrizione('');
    setFormImporto('');
    setFormOreFermo('');
    setFormFornitore('');
    setFormFtProt('');
    setFormDataFattura('');
    setFormNote('');
    setShowModal(true);
  };

  const handleEdit = (item: ManutenzioneStraordinaria) => {
    setEditing(item);
    setFormData(item.data_manutenzione);
    setFormDescrizione(item.descrizione || '');
    setFormImporto(item.importo || '');
    setFormOreFermo(item.ore_fermo || '');
    setFormFornitore(item.fk_fornitore || '');
    setFormFtProt(item.ft_prot || '');
    setFormDataFattura(item.data_fattura || '');
    setFormNote(item.note || '');
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData) {
      toast.warning('La data è obbligatoria');
      return;
    }

    try {
      setSaving(true);
      const data: any = {
        fk_attrezzatura: attrezzaturaId,
        data_manutenzione: formData,
        descrizione: formDescrizione || null,
        importo: formImporto || null,
        ore_fermo: formOreFermo || null,
        fk_fornitore: formFornitore || null,
        ft_prot: formFtProt || null,
        data_fattura: formDataFattura || null,
        note: formNote || null,
      };

      if (editing) {
        await updateManutenzioneStraordinaria(editing.id, data);
        toast.success('Manutenzione aggiornata');
      } else {
        await createManutenzioneStraordinaria(data);
        toast.success('Manutenzione creata');
      }
      setShowModal(false);
      await loadItems();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore salvataggio'));
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Eliminare questa manutenzione straordinaria?')) return;
    try {
      await deleteManutenzioneStraordinaria(id);
      toast.success('Manutenzione eliminata');
      await loadItems();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore eliminazione'));
    }
  };

  if (loading) {
    return (
      <div className="text-center py-4">
        <Spinner animation="border" size="sm" />
      </div>
    );
  }

  return (
    <>
      <div className="text-end mb-2">
        <Button size="sm" onClick={handleAdd}>
          + Aggiungi
        </Button>
      </div>
      <Table size="sm" striped hover responsive>
        <thead>
          <tr>
            <th>Data</th>
            <th>Descrizione</th>
            <th>Importo</th>
            <th style={{ width: '100px' }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{new Date(item.data_manutenzione).toLocaleDateString('it-IT')}</td>
              <td>{item.descrizione || '—'}</td>
              <td>{item.importo ? `€ ${item.importo}` : '—'}</td>
              <td>
                <Button
                  size="sm"
                  variant="outline-primary"
                  className="me-1"
                  onClick={() => handleEdit(item)}
                >
                  ✏️
                </Button>
                <Button
                  size="sm"
                  variant="outline-danger"
                  onClick={() => handleDelete(item.id)}
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
          {items.length === 0 && (
            <tr>
              <td colSpan={4} className="text-center text-muted">
                Nessuna manutenzione straordinaria presente
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>
            {editing ? 'Modifica Manutenzione Straordinaria' : 'Nuova Manutenzione Straordinaria'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>
                Data Manutenzione <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                type="date"
                value={formData}
                onChange={(e) => setFormData(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Descrizione</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                value={formDescrizione}
                onChange={(e) => setFormDescrizione(e.target.value)}
              />
            </Form.Group>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Importo (€)</Form.Label>
                  <Form.Control
                    type="text"
                    value={formImporto}
                    onChange={(e) => setFormImporto(e.target.value)}
                    placeholder="0.00"
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Ore Fermo</Form.Label>
                  <Form.Control
                    type="text"
                    value={formOreFermo}
                    onChange={(e) => setFormOreFermo(e.target.value)}
                    placeholder="0.00"
                  />
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Fornitore</Form.Label>
              <Form.Select
                value={formFornitore}
                onChange={(e) => setFormFornitore(e.target.value ? Number(e.target.value) : '')}
              >
                <option value="">-- Seleziona --</option>
                {fornitori.map((f) => (
                  <option key={f.id} value={f.id}>
                    {f.ragionesociale}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>FT / Protocollo</Form.Label>
                  <Form.Control
                    value={formFtProt}
                    onChange={(e) => setFormFtProt(e.target.value)}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Data Fattura</Form.Label>
                  <Form.Control
                    type="date"
                    value={formDataFattura}
                    onChange={(e) => setFormDataFattura(e.target.value)}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
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
    </>
  );
}

// =============================================================================
// MANUTENZIONI ORDINARIE CARD
// =============================================================================

interface ManutenzioniOrdinarieCardProps {
  attrezzaturaId: number;
  fornitori: Fornitore[];
}

function ManutenzioniOrdinarieCard({ attrezzaturaId, fornitori }: ManutenzioniOrdinarieCardProps) {
  const [items, setItems] = useState<ManutenzioneOrdinaria[]>([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<ManutenzioneOrdinaria | null>(null);
  const [saving, setSaving] = useState(false);

  // Form fields
  const [formData, setFormData] = useState('');
  const [formDescrizione, setFormDescrizione] = useState('');
  const [formFornitore, setFormFornitore] = useState<number | ''>('');
  const [formIsEseguita, setFormIsEseguita] = useState(false);
  const [formProssimaScadenza, setFormProssimaScadenza] = useState('');
  const [formNote, setFormNote] = useState('');

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getManutenzioniOrdinarie({
        fk_attrezzatura: attrezzaturaId,
        page_size: 1000,
      });
      setItems(res.data.results);
    } catch {
      toast.error('Errore caricamento manutenzioni ordinarie');
    } finally {
      setLoading(false);
    }
  }, [attrezzaturaId]);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormData('');
    setFormDescrizione('');
    setFormFornitore('');
    setFormIsEseguita(false);
    setFormProssimaScadenza('');
    setFormNote('');
    setShowModal(true);
  };

  const handleEdit = (item: ManutenzioneOrdinaria) => {
    setEditing(item);
    setFormData(item.data_manutenzione);
    setFormDescrizione(item.descrizione || '');
    setFormFornitore(item.fk_fornitore || '');
    setFormIsEseguita(item.is_eseguita);
    setFormProssimaScadenza(item.prossima_scadenza || '');
    setFormNote(item.note || '');
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData) {
      toast.warning('La data è obbligatoria');
      return;
    }

    try {
      setSaving(true);
      const data: any = {
        fk_attrezzatura: attrezzaturaId,
        data_manutenzione: formData,
        descrizione: formDescrizione || null,
        fk_fornitore: formFornitore || null,
        is_eseguita: formIsEseguita,
        prossima_scadenza: formProssimaScadenza || null,
        note: formNote || null,
      };

      if (editing) {
        await updateManutenzioneOrdinaria(editing.id, data);
        toast.success('Manutenzione aggiornata');
      } else {
        await createManutenzioneOrdinaria(data);
        toast.success('Manutenzione creata');
      }
      setShowModal(false);
      await loadItems();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore salvataggio'));
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Eliminare questa manutenzione ordinaria?')) return;
    try {
      await deleteManutenzioneOrdinaria(id);
      toast.success('Manutenzione eliminata');
      await loadItems();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore eliminazione'));
    }
  };

  if (loading) {
    return (
      <div className="text-center py-4">
        <Spinner animation="border" size="sm" />
      </div>
    );
  }

  return (
    <>
      <div className="text-end mb-2">
        <Button size="sm" onClick={handleAdd}>
          + Aggiungi
        </Button>
      </div>
      <Table size="sm" striped hover responsive>
        <thead>
          <tr>
            <th>Data</th>
            <th>Descrizione</th>
            <th>Eseguita</th>
            <th style={{ width: '100px' }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{new Date(item.data_manutenzione).toLocaleDateString('it-IT')}</td>
              <td>{item.descrizione || '—'}</td>
              <td>
                {item.is_eseguita ? (
                  <Badge bg="success">Sì</Badge>
                ) : (
                  <Badge bg="warning">No</Badge>
                )}
              </td>
              <td>
                <Button
                  size="sm"
                  variant="outline-primary"
                  className="me-1"
                  onClick={() => handleEdit(item)}
                >
                  ✏️
                </Button>
                <Button
                  size="sm"
                  variant="outline-danger"
                  onClick={() => handleDelete(item.id)}
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
          {items.length === 0 && (
            <tr>
              <td colSpan={4} className="text-center text-muted">
                Nessuna manutenzione ordinaria presente
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>
            {editing ? 'Modifica Manutenzione Ordinaria' : 'Nuova Manutenzione Ordinaria'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>
                Data Manutenzione <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                type="date"
                value={formData}
                onChange={(e) => setFormData(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Descrizione</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                value={formDescrizione}
                onChange={(e) => setFormDescrizione(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Fornitore</Form.Label>
              <Form.Select
                value={formFornitore}
                onChange={(e) => setFormFornitore(e.target.value ? Number(e.target.value) : '')}
              >
                <option value="">-- Seleziona --</option>
                {fornitori.map((f) => (
                  <option key={f.id} value={f.id}>
                    {f.ragionesociale}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Check
                type="checkbox"
                label="Manutenzione eseguita"
                checked={formIsEseguita}
                onChange={(e) => setFormIsEseguita(e.target.checked)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Prossima Scadenza</Form.Label>
              <Form.Control
                type="date"
                value={formProssimaScadenza}
                onChange={(e) => setFormProssimaScadenza(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
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
    </>
  );
}

// =============================================================================
// TARATURE CARD
// =============================================================================

interface TaratureCardProps {
  attrezzaturaId: number;
  fornitori: Fornitore[];
}

function TaratureCard({ attrezzaturaId, fornitori }: TaratureCardProps) {
  const [items, setItems] = useState<Taratura[]>([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<Taratura | null>(null);
  const [saving, setSaving] = useState(false);

  // Form fields
  const [formData, setFormData] = useState('');
  const [formFornitore, setFormFornitore] = useState<number | ''>('');
  const [formDocumento, setFormDocumento] = useState<File | null>(null);
  const [formIsConforme, setFormIsConforme] = useState(false);
  const [formProssimaScadenza, setFormProssimaScadenza] = useState('');
  const [formNote, setFormNote] = useState('');

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getTarature({
        fk_attrezzatura: attrezzaturaId,
        page_size: 1000,
      });
      setItems(res.data.results);
    } catch {
      toast.error('Errore caricamento tarature');
    } finally {
      setLoading(false);
    }
  }, [attrezzaturaId]);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormData('');
    setFormFornitore('');
    setFormDocumento(null);
    setFormIsConforme(false);
    setFormProssimaScadenza('');
    setFormNote('');
    setShowModal(true);
  };

  const handleEdit = (item: Taratura) => {
    setEditing(item);
    setFormData(item.data_taratura);
    setFormFornitore(item.fk_fornitore || '');
    setFormDocumento(null);
    setFormIsConforme(item.is_conforme);
    setFormProssimaScadenza(item.prossima_scadenza || '');
    setFormNote(item.note || '');
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData) {
      toast.warning('La data è obbligatoria');
      return;
    }

    try {
      setSaving(true);

      const formDataObj = new FormData();
      formDataObj.append('fk_attrezzatura', String(attrezzaturaId));
      formDataObj.append('data_taratura', formData);
      if (formFornitore) formDataObj.append('fk_fornitore', String(formFornitore));
      if (formDocumento) formDataObj.append('documento', formDocumento);
      formDataObj.append('is_conforme', String(formIsConforme));
      if (formProssimaScadenza) formDataObj.append('prossima_scadenza', formProssimaScadenza);
      if (formNote) formDataObj.append('note', formNote);

      if (editing) {
        await updateTaratura(editing.id, formDataObj);
        toast.success('Taratura aggiornata');
      } else {
        await createTaratura(formDataObj);
        toast.success('Taratura creata');
      }
      setShowModal(false);
      await loadItems();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore salvataggio'));
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Eliminare questa taratura?')) return;
    try {
      await deleteTaratura(id);
      toast.success('Taratura eliminata');
      await loadItems();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore eliminazione'));
    }
  };

  if (loading) {
    return (
      <div className="text-center py-4">
        <Spinner animation="border" size="sm" />
      </div>
    );
  }

  return (
    <>
      <div className="text-end mb-2">
        <Button size="sm" onClick={handleAdd}>
          + Aggiungi
        </Button>
      </div>
      <Table size="sm" striped hover responsive>
        <thead>
          <tr>
            <th>Data</th>
            <th>Conforme</th>
            <th>Scadenza</th>
            <th>Doc</th>
            <th style={{ width: '100px' }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{new Date(item.data_taratura).toLocaleDateString('it-IT')}</td>
              <td>
                {item.is_conforme ? (
                  <Badge bg="success">Sì</Badge>
                ) : (
                  <Badge bg="danger">No</Badge>
                )}
              </td>
              <td>
                {item.prossima_scadenza
                  ? new Date(item.prossima_scadenza).toLocaleDateString('it-IT')
                  : '—'}
              </td>
              <td>
                {item.documento ? (
                  <a
                    href={`/api/manutenzioni/tarature/${item.id}/download/`}
                    target="_blank"
                    rel="noopener noreferrer"
                    title="Scarica documento"
                  >
                    📄 PDF
                  </a>
                ) : (
                  <span className="text-muted">—</span>
                )}
              </td>
              <td>
                <Button
                  size="sm"
                  variant="outline-primary"
                  className="me-1"
                  onClick={() => handleEdit(item)}
                >
                  ✏️
                </Button>
                <Button
                  size="sm"
                  variant="outline-danger"
                  onClick={() => handleDelete(item.id)}
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
          {items.length === 0 && (
            <tr>
              <td colSpan={5} className="text-center text-muted">
                Nessuna taratura presente
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>{editing ? 'Modifica Taratura' : 'Nuova Taratura'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>
                Data Taratura <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                type="date"
                value={formData}
                onChange={(e) => setFormData(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Fornitore</Form.Label>
              <Form.Select
                value={formFornitore}
                onChange={(e) => setFormFornitore(e.target.value ? Number(e.target.value) : '')}
              >
                <option value="">-- Seleziona --</option>
                {fornitori.map((f) => (
                  <option key={f.id} value={f.id}>
                    {f.ragionesociale}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Documento</Form.Label>
              <Form.Control
                type="file"
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                  const file = e.target.files?.[0] || null;
                  setFormDocumento(file);
                }}
              />
              <Form.Text className="text-muted">Carica certificato di taratura (PDF)</Form.Text>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Check
                type="checkbox"
                label="Taratura conforme"
                checked={formIsConforme}
                onChange={(e) => setFormIsConforme(e.target.checked)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Prossima Scadenza</Form.Label>
              <Form.Control
                type="date"
                value={formProssimaScadenza}
                onChange={(e) => setFormProssimaScadenza(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
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
    </>
  );
}

// =============================================================================
// CONTROLLI PERIODICI CARD
// =============================================================================

interface ControlliPeriodiciCardProps {
  attrezzaturaId: number;
  dipendenti: HumanResource[];
}

function ControlliPeriodiciCard({ attrezzaturaId, dipendenti }: ControlliPeriodiciCardProps) {
  const [items, setItems] = useState<ControlloPeriodico[]>([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<ControlloPeriodico | null>(null);
  const [saving, setSaving] = useState(false);

  // Form fields
  const [formData, setFormData] = useState('');
  const [formDescrizione, setFormDescrizione] = useState('');
  const [formHR, setFormHR] = useState<number | ''>('');
  const [formIsEseguita, setFormIsEseguita] = useState(false);
  const [formProssimaScadenza, setFormProssimaScadenza] = useState('');
  const [formNote, setFormNote] = useState('');

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getControlliPeriodici({
        fk_attrezzatura: attrezzaturaId,
        page_size: 1000,
      });
      setItems(res.data.results);
    } catch {
      toast.error('Errore caricamento controlli periodici');
    } finally {
      setLoading(false);
    }
  }, [attrezzaturaId]);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormData('');
    setFormDescrizione('');
    setFormHR('');
    setFormIsEseguita(false);
    setFormProssimaScadenza('');
    setFormNote('');
    setShowModal(true);
  };

  const handleEdit = (item: ControlloPeriodico) => {
    setEditing(item);
    setFormData(item.data_controllo);
    setFormDescrizione(item.descrizione || '');
    setFormHR(item.fk_human_resource || '');
    setFormIsEseguita(item.is_eseguita);
    setFormProssimaScadenza(item.prossima_scadenza || '');
    setFormNote(item.note || '');
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData) {
      toast.warning('La data è obbligatoria');
      return;
    }

    try {
      setSaving(true);
      const data: any = {
        fk_attrezzatura: attrezzaturaId,
        data_controllo: formData,
        descrizione: formDescrizione || null,
        fk_human_resource: formHR || null,
        is_eseguita: formIsEseguita,
        prossima_scadenza: formProssimaScadenza || null,
        note: formNote || null,
      };

      if (editing) {
        await updateControlloPeriodico(editing.id, data);
        toast.success('Controllo aggiornato');
      } else {
        await createControlloPeriodico(data);
        toast.success('Controllo creato');
      }
      setShowModal(false);
      await loadItems();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore salvataggio'));
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Eliminare questo controllo periodico?')) return;
    try {
      await deleteControlloPeriodico(id);
      toast.success('Controllo eliminato');
      await loadItems();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore eliminazione'));
    }
  };

  if (loading) {
    return (
      <div className="text-center py-4">
        <Spinner animation="border" size="sm" />
      </div>
    );
  }

  return (
    <>
      <div className="text-end mb-2">
        <Button size="sm" onClick={handleAdd}>
          + Aggiungi
        </Button>
      </div>
      <Table size="sm" striped hover responsive>
        <thead>
          <tr>
            <th>Data</th>
            <th>Descrizione</th>
            <th>Eseguita</th>
            <th style={{ width: '100px' }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{new Date(item.data_controllo).toLocaleDateString('it-IT')}</td>
              <td>{item.descrizione || '—'}</td>
              <td>
                {item.is_eseguita ? (
                  <Badge bg="success">Sì</Badge>
                ) : (
                  <Badge bg="warning">No</Badge>
                )}
              </td>
              <td>
                <Button
                  size="sm"
                  variant="outline-primary"
                  className="me-1"
                  onClick={() => handleEdit(item)}
                >
                  ✏️
                </Button>
                <Button
                  size="sm"
                  variant="outline-danger"
                  onClick={() => handleDelete(item.id)}
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
          {items.length === 0 && (
            <tr>
              <td colSpan={4} className="text-center text-muted">
                Nessun controllo periodico presente
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>
            {editing ? 'Modifica Controllo Periodico' : 'Nuovo Controllo Periodico'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>
                Data Controllo <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                type="date"
                value={formData}
                onChange={(e) => setFormData(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Descrizione</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                value={formDescrizione}
                onChange={(e) => setFormDescrizione(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Operatore</Form.Label>
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

            <Form.Group className="mb-3">
              <Form.Check
                type="checkbox"
                label="Controllo eseguito"
                checked={formIsEseguita}
                onChange={(e) => setFormIsEseguita(e.target.checked)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Prossima Scadenza</Form.Label>
              <Form.Control
                type="date"
                value={formProssimaScadenza}
                onChange={(e) => setFormProssimaScadenza(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
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
    </>
  );
}
