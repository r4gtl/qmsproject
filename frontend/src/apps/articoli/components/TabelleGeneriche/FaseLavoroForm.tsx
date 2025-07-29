import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Card, Spinner, Row, Col } from 'react-bootstrap';
import { toast } from 'react-toastify';
import { getFase, createFase, updateFase } from '@articoli/api/articoli';
import DettagliFaseTable from '../FaseLavoro/DettagliFaseTable';
import {
  getDettagliFase,
  createDettaglioFase,
  updateDettaglioFase,
  deleteDettaglioFase,
} from '@articoli/api/articoli';

const FaseLavoroForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = id !== undefined && id !== 'new';

  const [loading, setLoading] = useState(false);
  const [descrizione, setDescrizione] = useState('');
  const [int_est, setInt_est] = useState('');
  const [um, setUM] = useState('');

  const [dettagli, setDettagli] = useState<DettaglioFaseLavoro[]>([]);
  const [deletedDettagli, setDeletedDettagli] = useState<number[]>([]);

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
    const loadDettagli = async () => {
      try {
        const res = await getDettagliFase(Number(id));
        setDettagli(res.data);
      } catch {
        toast.error('Errore nel caricamento attributi fase');
      }
    };

    loadFase();
    loadDettagli();
  }, [id, isEditMode]);

  const handleDettagliChange = (updated: DettaglioFaseLavoro[]) => {
    // Detect what was rimosso
    const removedIds = dettagli
      .filter((d) => d.id && !updated.find((u) => u.id === d.id))
      .map((d) => d.id!) as number[];

    setDettagli(updated);
    setDeletedDettagli((prev) => [...prev, ...removedIds]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append('descrizione', descrizione);
    formData.append('interno_esterno', int_est);
    formData.append('um', um);

    try {
      let faseID = Number(id);

      if (isEditMode) {
        await updateFase(faseID, formData);
        toast.success('Fase aggiornata');
      } else {
        const res = await createFase(formData);
        faseID = res.data.id;
        toast.success('Fase creata');
      }
      for (const dett of dettagli) {
        if (dett.id) {
          await updateDettaglioFase(dett.id, {
            attributo: dett.attributo,
            note: dett.note,
          });
        } else {
          await createDettaglioFase({
            fk_fase_lavoro: faseID,
            attributo: dett.attributo,
            note: dett.note,
          });
        }
      }

      // 3. Cancella attributi rimossi
      for (const id of deletedDettagli) {
        await deleteDettaglioFase(id);
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

        <DettagliFaseTable
          faseId={isEditMode ? Number(id) : null}
          dettagli={dettagli}
          onChange={handleDettagliChange}
        />
      </Card.Body>
    </Card>
  );
};

export default FaseLavoroForm;
