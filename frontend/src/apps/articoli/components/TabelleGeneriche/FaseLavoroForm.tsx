import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Card, Spinner, Row, Col } from 'react-bootstrap';
import { toast } from 'react-toastify';
import { getFase, createFase, updateFase } from '@articoli/api/articoli';

const FaseLavoroForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = id !== undefined && id !== 'new';

  const [loading, setLoading] = useState(false);
  const [descrizione, setDescrizione] = useState('');
  const [int_est, setInt_est] = useState('');
  const [um, setUM] = useState('');

  useEffect(() => {
    if (!isEditMode) return;
    const loadFase = async () => {
      try {
        const res = await getFase(Number(id));
        const data = res.data;
        setDescrizione(data.descrizione ?? '');
        setInt_est(data.interno_esterno ?? '');
        setUM(data.um ?? '');
      } catch (error) {
        toast.error('Errore nel caricamento Fase');
      }
    };
    loadFase();
  }, [id, isEditMode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append('descrizione', descrizione);
    formData.append('interno_esterno', int_est);
    formData.append('um', um);

    try {
      if (isEditMode) {
        await updateFase(Number(id), formData);
        toast.success('Fase aggiornata');
      } else {
        await createFase(formData);
        toast.success('Fase creata');
      }
      navigate('/articoli/tabelle');
    } catch {
      toast.error('Errore nel salvataggio fase');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <Card.Body>
        <Card.Title>{isEditMode ? 'Modifica' : 'Nuova'} Fase</Card.Title>
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
                <Form.Label>Interno/Esterno</Form.Label>
                <Form.Select
                  value={int_est}
                  onChange={(e) => setInt_est(e.target.value)}
                  required
                >
                  <option value="">Seleziona...</option>
                  <option value="interno">Interno</option>
                  <option value="esterno">Esterno</option>
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>UM</Form.Label>
                <Form.Select
                  value={um}
                  onChange={(e) => setUM(e.target.value)}
                  required
                >
                  <option value="">Seleziona...</option>
                  <option value="mq">Mq.</option>
                  <option value="Nr.">Nr.</option>
                  <option value="Kg.">Kg.</option>
                </Form.Select>
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

export default FaseLavoroForm;
