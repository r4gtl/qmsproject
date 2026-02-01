import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Card, Spinner, Row, Col } from 'react-bootstrap';
import { toast } from 'react-toastify';
import {
  getArticolo,
  createArticolo,
  updateArticolo,
} from '@articoli/api/articoli';
import { getTipoAnimali, getTipoGrezzi } from '@/api/lookup';
import type { TipoAnimale, TipoGrezzo } from '@articoli/types/lookup';
import Select from 'react-select';
import { ProcedureCard } from '../components/Procedure';

const ArticoloForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = !!id;

  const [loading, setLoading] = useState(false);
  const [descrizione, setDescrizione] = useState('');
  const [industriesServed, setIndustriesServed] = useState('');
  const [fkTipoAnimale, setFkTipoAnimale] = useState('');
  const [fkTipoGrezzo, setFkTipoGrezzo] = useState('');
  const [tipoAnimali, setTipoAnimali] = useState<TipoAnimale[]>([]);
  const [tipoGrezzi, setTipoGrezzi] = useState<TipoGrezzo[]>([]);
  const industriesChoices = [
    { value: 'apparel/clothing', label: 'Apparel/clothing' },
    { value: 'automotive', label: 'Automotive' },
    { value: 'contract', label: 'Contract' },
    { value: 'footwear', label: 'Footwear' },
    { value: 'footwear (athletic)', label: 'Footwear (Athletic)' },
    { value: 'leather goods', label: 'Leather goods' },
    { value: 'upholstery', label: 'Upholstery' },
  ];

  useEffect(() => {
    const loadLookups = async () => {
      try {
        const [animali, grezzi] = await Promise.all([
          getTipoAnimali(),
          getTipoGrezzi(),
        ]);
        setTipoAnimali(animali.data.results);
        setTipoGrezzi(grezzi.data.results);
      } catch (error) {
        toast.error('Errore nel caricamento delle tabelle lookup');
      }
    };
    loadLookups();
  }, []);

  useEffect(() => {
    if (!isEditMode) return;
    const loadArticolo = async () => {
      try {
        const res = await getArticolo(Number(id));
        const data = res.data;
        setDescrizione(data.descrizione);
        setIndustriesServed(data.industries_served || '');
        setFkTipoAnimale(data.fk_tipoanimale?.toString() || '');
        setFkTipoGrezzo(data.fk_tipogrezzo?.toString() || '');
      } catch (error) {
        toast.error('Errore nel caricamento articolo');
      }
    };
    loadArticolo();
  }, [id, isEditMode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append('descrizione', descrizione);
    formData.append('industries_served', industriesServed);
    if (fkTipoAnimale) formData.append('fk_tipoanimale', fkTipoAnimale);
    if (fkTipoGrezzo) formData.append('fk_tipogrezzo', fkTipoGrezzo);

    try {
      if (isEditMode) {
        await updateArticolo(Number(id), formData);
        toast.success('Articolo aggiornato');
      } else {
        await createArticolo(formData);
        toast.success('Articolo creato');
      }
      navigate('/articoli');
    } catch {
      toast.error('Errore nel salvataggio articolo');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <Card.Body>
        <Card.Title>{isEditMode ? 'Modifica' : 'Nuovo'} Articolo</Card.Title>
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
                <Form.Label>Industria servita</Form.Label>
                <Select
                  options={industriesChoices}
                  value={industriesChoices.find(
                    (opt) => opt.value === industriesServed
                  )}
                  onChange={(selected) =>
                    setIndustriesServed(selected?.value || '')
                  }
                />
              </Form.Group>
            </Col>
          </Row>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Tipo animale</Form.Label>
                <Form.Select
                  value={fkTipoAnimale}
                  onChange={(e) => setFkTipoAnimale(e.target.value)}
                >
                  <option value="">---</option>
                  {tipoAnimali.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.descrizione}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Tipo grezzo</Form.Label>
                <Form.Select
                  value={fkTipoGrezzo}
                  onChange={(e) => setFkTipoGrezzo(e.target.value)}
                >
                  <option value="">---</option>
                  {tipoGrezzi.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.descrizione}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>

          <div className="text-end">
            <Button variant="secondary" onClick={() => navigate('/articoli')}>
              Annulla
            </Button>{' '}
            <Button variant="primary" type="submit" disabled={loading}>
              {loading ? <Spinner animation="border" size="sm" /> : 'Salva'}
            </Button>
          </div>
        </Form>
      </Card.Body>

      {/* Sezione Procedure - solo in modalità edit */}
      {isEditMode && id && (
        <Card.Footer className="bg-transparent border-0 p-0">
          <ProcedureCard articoloId={Number(id)} />
        </Card.Footer>
      )}
    </Card>
  );
};

export default ArticoloForm;
