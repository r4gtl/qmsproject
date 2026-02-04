/**
 * DettaglioFormazioneFormPage - Form per creare/modificare dettaglio formazione (operatore)
 *
 * Features:
 * - Campi: fk_hr (select), presenza (select), ore, note, efficace (checkbox),
 *   scadenza_override (date opzionale), certificato (file)
 * - Se certificato selezionato, manda multipart/form-data
 * - Altrimenti manda JSON
 */
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Card,
  Form,
  Button,
  Spinner,
  Row,
  Col,
  Alert,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import { FaUserGraduate, FaSave, FaTimes, FaFileUpload } from 'react-icons/fa';
import {
  getDettaglioFormazione,
  createDettaglioFormazione,
  updateDettaglioFormazione,
  getDipendentiForSelect,
} from '../api/formazioneApi';
import type { DettaglioRegistroFormazione } from '../types';
import type { HumanResourceList } from '../../types';
import { PRESENZA_CHOICES } from '../types';
import { extractErrorMessage, parseOreOrNull } from '../utils/drfErrors';

interface FormData {
  fk_hr: string;
  presenza: 'presente' | 'assente';
  ore: string;
  note: string;
  efficace: boolean;
  scadenza_override: string;
}

const initialFormData: FormData = {
  fk_hr: '',
  presenza: 'presente',
  ore: '',
  note: '',
  efficace: true,
  scadenza_override: '',
};

export default function DettaglioFormazioneFormPage() {
  const { registroId, id } = useParams<{ registroId: string; id: string }>();
  const navigate = useNavigate();
  const isEdit = !!id && id !== 'new';

  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [certificatoFile, setCertificatoFile] = useState<File | null>(null);
  const [existingCertificatoUrl, setExistingCertificatoUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Lookups
  const [dipendenti, setDipendenti] = useState<HumanResourceList[]>([]);
  const [loadingLookups, setLoadingLookups] = useState(true);

  // Load lookups
  useEffect(() => {
    const loadLookups = async () => {
      try {
        setLoadingLookups(true);
        const res = await getDipendentiForSelect();
        setDipendenti(res.data.results);
      } catch {
        toast.error('Errore nel caricamento degli operatori');
      } finally {
        setLoadingLookups(false);
      }
    };
    loadLookups();
  }, []);

  // Load existing record if editing
  useEffect(() => {
    if (isEdit) {
      loadRecord();
    }
  }, [id, isEdit]);

  const loadRecord = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getDettaglioFormazione(Number(id));
      const data: DettaglioRegistroFormazione = res.data;
      setFormData({
        fk_hr: data.fk_hr?.toString() ?? '',
        presenza: data.presenza,
        ore: data.ore?.toString() ?? '',
        note: data.note ?? '',
        efficace: data.efficace,
        scadenza_override: data.scadenza_override ?? '',
      });
      setExistingCertificatoUrl(data.certificato_url);
    } catch (err: any) {
      setError('Errore nel caricamento del dettaglio.');
      toast.error('Errore caricamento dati');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: keyof FormData, value: string | boolean) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setCertificatoFile(file);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (!formData.fk_hr) {
      toast.warning("L'operatore è obbligatorio");
      return;
    }
    if (!formData.presenza) {
      toast.warning('La presenza è obbligatoria');
      return;
    }

    try {
      setSaving(true);

      // Decide if we need FormData (for file upload) or JSON
      if (certificatoFile) {
        // Use FormData for multipart upload
        // IMPORTANTE: Includi sempre i campi required dal serializer
        const fd = new FormData();
        fd.append('fk_registro_formazione', registroId!);
        fd.append('fk_hr', formData.fk_hr);
        fd.append('presenza', formData.presenza);
        fd.append('efficace', formData.efficace ? 'true' : 'false');
        // ore: solo se valorizzato (DRF accetta stringa per DecimalField)
        const oreVal = parseOreOrNull(formData.ore);
        if (oreVal !== null) fd.append('ore', oreVal);
        if (formData.note?.trim()) fd.append('note', formData.note.trim());
        if (formData.scadenza_override) fd.append('scadenza_override', formData.scadenza_override);
        fd.append('certificato', certificatoFile);

        if (isEdit) {
          await updateDettaglioFormazione(Number(id), fd);
          toast.success('Dettaglio aggiornato');
        } else {
          await createDettaglioFormazione(fd);
          toast.success('Operatore aggiunto');
        }
      } else {
        // Use JSON
        const payload = {
          fk_registro_formazione: parseInt(registroId!, 10),
          fk_hr: parseInt(formData.fk_hr, 10),
          presenza: formData.presenza,
          ore: parseOreOrNull(formData.ore),
          note: formData.note?.trim() || null,
          efficace: formData.efficace,
          scadenza_override: formData.scadenza_override || null,
        };

        if (isEdit) {
          await updateDettaglioFormazione(Number(id), payload);
          toast.success('Dettaglio aggiornato');
        } else {
          await createDettaglioFormazione(payload);
          toast.success('Operatore aggiunto');
        }
      }

      // Redirect back to registro
      navigate(`/human-resources/formazione/registri/${registroId}`);
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Errore durante il salvataggio'));
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    navigate(`/human-resources/formazione/registri/${registroId}`);
  };

  if (loading || loadingLookups) {
    return (
      <Container className="my-4 text-center">
        <Spinner animation="border" />
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="my-4">
        <Alert variant="danger">{error}</Alert>
        <Button variant="secondary" onClick={handleCancel}>
          Torna al registro
        </Button>
      </Container>
    );
  }

  return (
    <Container className="my-4">
      <Card className="shadow-sm">
        <Card.Header className="d-flex align-items-center">
          <FaUserGraduate className="me-2" />
          <span className="fw-bold">
            {isEdit ? 'Modifica Operatore Formato' : 'Aggiungi Operatore'}
          </span>
        </Card.Header>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            <Row className="mb-3">
              <Col md={6}>
                <Form.Group>
                  <Form.Label>
                    Operatore <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Select
                    value={formData.fk_hr}
                    onChange={(e) => handleChange('fk_hr', e.target.value)}
                    required
                  >
                    <option value="">-- Seleziona operatore --</option>
                    {dipendenti.map((d) => (
                      <option key={d.id} value={d.id}>
                        {d.full_name}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>
                    Presenza <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Select
                    value={formData.presenza}
                    onChange={(e) =>
                      handleChange('presenza', e.target.value as 'presente' | 'assente')
                    }
                    required
                  >
                    {PRESENZA_CHOICES.map((p) => (
                      <option key={p.value} value={p.value}>
                        {p.label}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Ore</Form.Label>
                  <Form.Control
                    type="number"
                    step="0.5"
                    min="0"
                    value={formData.ore}
                    onChange={(e) => handleChange('ore', e.target.value)}
                    placeholder="Es: 8"
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row className="mb-3">
              <Col md={4}>
                <Form.Group>
                  <Form.Label>Scadenza Override</Form.Label>
                  <Form.Control
                    type="date"
                    value={formData.scadenza_override}
                    onChange={(e) => handleChange('scadenza_override', e.target.value)}
                  />
                  <Form.Text className="text-muted">
                    Lasciare vuoto per usare la scadenza calcolata automaticamente
                  </Form.Text>
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group>
                  <Form.Label>Certificato</Form.Label>
                  <Form.Control
                    type="file"
                    onChange={handleFileChange}
                    accept=".pdf,.jpg,.jpeg,.png"
                  />
                  {existingCertificatoUrl && !certificatoFile && (
                    <Form.Text>
                      <a
                        href={existingCertificatoUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="d-flex align-items-center mt-1"
                      >
                        <FaFileUpload className="me-1" /> Certificato esistente
                      </a>
                    </Form.Text>
                  )}
                  {certificatoFile && (
                    <Form.Text className="text-success">
                      File selezionato: {certificatoFile.name}
                    </Form.Text>
                  )}
                </Form.Group>
              </Col>
              <Col md={4} className="d-flex align-items-center pt-4">
                <Form.Group>
                  <Form.Check
                    type="checkbox"
                    id="efficace"
                    label="Formazione efficace"
                    checked={formData.efficace}
                    onChange={(e) => handleChange('efficace', e.target.checked)}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row className="mb-3">
              <Col md={12}>
                <Form.Group>
                  <Form.Label>Note</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={2}
                    value={formData.note}
                    onChange={(e) => handleChange('note', e.target.value)}
                    placeholder="Note aggiuntive..."
                  />
                </Form.Group>
              </Col>
            </Row>

            {/* Buttons */}
            <div className="d-flex justify-content-end gap-2">
              <Button variant="secondary" onClick={handleCancel} disabled={saving}>
                <FaTimes className="me-1" /> Annulla
              </Button>
              <Button variant="primary" type="submit" disabled={saving}>
                {saving ? (
                  <Spinner animation="border" size="sm" />
                ) : (
                  <>
                    <FaSave className="me-1" /> Salva
                  </>
                )}
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
}
