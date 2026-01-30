import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Card, Spinner, Row, Col } from 'react-bootstrap';
import { toast } from 'react-toastify';
import {
  getLavorazioneEsterna,
  createLavorazioneEsterna,
  updateLavorazioneEsterna,
} from '@articoli/api/articoli';

const CodiceLavorazioneForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = id !== undefined && id !== 'new';

  const [loading, setLoading] = useState(false);
  const [descrizione, setDescrizione] = useState('');
  const [codice, setCodice] = useState('');
  const [note, setNote] = useState('');

  useEffect(() => {
    if (!isEditMode) return;
    const loadLavorazione = async () => {
      try {
        const res = await getLavorazioneEsterna(Number(id));
        const data = res.data;
        setDescrizione(data.descrizione ?? '');
        setCodice(data.codice ?? '');
        setNote(data.note ?? '');
      } catch (error) {
        toast.error('Errore nel caricamento lavorazione');
        console.error(error);
      }
    };
    loadLavorazione();
  }, [id, isEditMode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append('descrizione', descrizione);
    formData.append('codice', codice);
    formData.append('note', note);

    try {
      if (isEditMode) {
        await updateLavorazioneEsterna(Number(id), formData);
        toast.success('Lavorazione aggiornata');
      } else {
        await createLavorazioneEsterna(formData);
        toast.success('Lavorazione creata');
      }
      navigate('/articoli/tabelle');
    } catch (error) {
      toast.error('Errore nel salvataggio lavorazione');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <Card.Body>
        <Card.Title>
          {isEditMode ? 'Modifica' : 'Nuova'} Lavorazione Esterna
        </Card.Title>
        <Form onSubmit={handleSubmit}>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Codice</Form.Label>
                <Form.Control
                  value={codice}
                  onChange={(e) => setCodice(e.target.value)}
                  required
                  maxLength={9}
                  placeholder="Es. LAV001"
                />
                <Form.Text className="text-muted">Max 9 caratteri</Form.Text>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Descrizione</Form.Label>
                <Form.Control
                  value={descrizione}
                  onChange={(e) => setDescrizione(e.target.value)}
                  required
                  maxLength={200}
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={12}>
              <Form.Group className="mb-3">
                <Form.Label>Note</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                  placeholder="Note aggiuntive (opzionale)"
                />
              </Form.Group>
            </Col>
          </Row>
          <div className="text-end">
            <Button
              variant="secondary"
              onClick={() => navigate('/articoli/tabelle')}
            >
              Annulla
            </Button>{' '}
            <Button variant="primary" type="submit" disabled={loading}>
              {loading ? <Spinner animation="border" size="sm" /> : 'Salva'}
            </Button>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default CodiceLavorazioneForm;
