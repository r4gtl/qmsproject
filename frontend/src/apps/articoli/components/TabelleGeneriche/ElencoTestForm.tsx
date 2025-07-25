import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Card, Spinner, Row, Col } from 'react-bootstrap';
import { toast } from 'react-toastify';
import { getTest, createTest, updateTest } from '@articoli/api/articoli';

const ElencoTestForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = id !== undefined && id !== 'new';

  const [loading, setLoading] = useState(false);
  const [descrizione, setDescrizione] = useState('');
  const [norma, setNorma] = useState('');
  const [note, setNote] = useState('');

  useEffect(() => {
    if (!isEditMode) return;
    const loadTest = async () => {
      try {
        const res = await getTest(Number(id));
        const data = res.data;
        setDescrizione(data.descrizione);
        setNorma(data.norma_riferimento);
        setNote(data.note);
      } catch (error) {
        toast.error('Errore nel caricamento test');
      }
    };
    loadTest();
  }, [id, isEditMode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append('descrizione', descrizione);
    formData.append('norma_riferimento', norma);
    formData.append('note', note);

    try {
      if (isEditMode) {
        await updateTest(Number(id), formData);
        toast.success('Test aggiornato');
      } else {
        await createTest(formData);
        toast.success('Test creato');
      }
      navigate('/articoli/tabelle');
    } catch {
      toast.error('Errore nel salvataggio test');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <Card.Body>
        <Card.Title>{isEditMode ? 'Modifica' : 'Nuovo'} Test</Card.Title>
        <Form onSubmit={handleSubmit}>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Descrizione</Form.Label>
                <Form.Control
                  value={descrizione}
                  onChange={(e) => setDescrizione(e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Norma di riferimento</Form.Label>
                <Form.Control
                  value={norma}
                  onChange={(e) => setNorma(e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Note</Form.Label>
                <Form.Control
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                  required
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

export default ElencoTestForm;
