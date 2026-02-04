/**
 * TabelleFormazionePage - Gestione tabelle Formazione
 *
 * Layout a 2 card per riga:
 * - Aree Formazione
 * - Corsi Formazione
 */
import { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Row,
  Col,
  Card,
  Table,
  Button,
  Spinner,
  Modal,
  Form,
  InputGroup,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import { FaLayerGroup, FaGraduationCap } from 'react-icons/fa';
import {
  getAreeFormazione,
  createAreaFormazione,
  updateAreaFormazione,
  deleteAreaFormazione,
  getCorsiFormazione,
  createCorsoFormazione,
  updateCorsoFormazione,
  deleteCorsoFormazione,
} from '../api/formazioneTabelleApi';
import type { AreaFormazione, CorsoFormazione } from '../types';
import { extractErrorMessage } from '../utils/drfErrors';

export default function TabelleFormazionePage() {
  return (
    <Container className="my-4">
      <h3 className="mb-4">Tabelle Formazione</h3>
      <Row className="g-4">
        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaLayerGroup className="me-2" />
              Aree Formazione
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <AreeFormazioneCard />
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaGraduationCap className="me-2" />
              Corsi Formazione
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <CorsiFormazioneCard />
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

// =============================================================================
// AREE FORMAZIONE CARD
// =============================================================================

function AreeFormazioneCard() {
  const [items, setItems] = useState<AreaFormazione[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<AreaFormazione | null>(null);
  const [formDescrizione, setFormDescrizione] = useState('');
  const [saving, setSaving] = useState(false);

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getAreeFormazione({ page_size: 1000 });
      setItems(res.data.results);
    } catch {
      toast.error('Errore caricamento aree formazione');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormDescrizione('');
    setShowModal(true);
  };

  const handleEdit = (item: AreaFormazione) => {
    setEditing(item);
    setFormDescrizione(item.descrizione);
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formDescrizione.trim()) {
      toast.warning('La descrizione è obbligatoria');
      return;
    }

    try {
      setSaving(true);
      if (editing) {
        await updateAreaFormazione(editing.id, { descrizione: formDescrizione.trim() });
        toast.success('Area formazione aggiornata');
      } else {
        await createAreaFormazione({ descrizione: formDescrizione.trim() });
        toast.success('Area formazione creata');
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
    try {
      await deleteAreaFormazione(id);
      toast.success('Area formazione eliminata');
      await loadItems();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Impossibile eliminare. Potrebbe essere in uso.'));
    }
  };

  const filtered = items.filter((item) =>
    item.descrizione.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <div className="text-center py-4">
        <Spinner animation="border" />
      </div>
    );
  }

  return (
    <>
      <InputGroup className="mb-2">
        <Form.Control
          placeholder="Cerca area..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </InputGroup>
      <div className="text-end mb-2">
        <Button size="sm" onClick={handleAdd}>
          + Aggiungi Area
        </Button>
      </div>
      <Table size="sm" striped hover responsive>
        <thead>
          <tr>
            <th>Descrizione</th>
            <th style={{ width: '100px' }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((item) => (
            <tr key={item.id}>
              <td>{item.descrizione}</td>
              <td>
                <Button
                  size="sm"
                  variant="outline-primary"
                  className="me-1"
                  onClick={() => handleEdit(item)}
                  title="Modifica"
                >
                  ✏️
                </Button>
                <Button
                  size="sm"
                  variant="outline-danger"
                  onClick={() => {
                    if (confirm(`Eliminare "${item.descrizione}"?`)) {
                      handleDelete(item.id);
                    }
                  }}
                  title="Elimina"
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
          {filtered.length === 0 && (
            <tr>
              <td colSpan={2} className="text-center text-muted">
                Nessuna area formazione presente.
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>
            {editing ? 'Modifica Area Formazione' : 'Nuova Area Formazione'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group>
              <Form.Label>
                Descrizione <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                value={formDescrizione}
                onChange={(e) => setFormDescrizione(e.target.value)}
                required
                autoFocus
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
// CORSI FORMAZIONE CARD
// =============================================================================

function CorsiFormazioneCard() {
  const [items, setItems] = useState<CorsoFormazione[]>([]);
  const [aree, setAree] = useState<AreaFormazione[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<CorsoFormazione | null>(null);
  const [formDescrizione, setFormDescrizione] = useState('');
  const [formArea, setFormArea] = useState<number | ''>('');
  const [formValiditaMesi, setFormValiditaMesi] = useState<number | ''>('');
  const [saving, setSaving] = useState(false);

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const [corsiRes, areeRes] = await Promise.all([
        getCorsiFormazione({ page_size: 1000 }),
        getAreeFormazione({ page_size: 1000 }),
      ]);
      setItems(corsiRes.data.results);
      setAree(areeRes.data.results);
    } catch {
      toast.error('Errore caricamento corsi formazione');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormDescrizione('');
    setFormArea('');
    setFormValiditaMesi('');
    setShowModal(true);
  };

  const handleEdit = (item: CorsoFormazione) => {
    setEditing(item);
    setFormDescrizione(item.descrizione);
    setFormArea(item.fk_areaformazione);
    setFormValiditaMesi(item.validita_mesi);
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formDescrizione.trim()) {
      toast.warning('La descrizione è obbligatoria');
      return;
    }
    if (!formArea) {
      toast.warning("L'area formazione è obbligatoria");
      return;
    }
    if (!formValiditaMesi || formValiditaMesi <= 0) {
      toast.warning('La validità in mesi deve essere maggiore di 0');
      return;
    }

    try {
      setSaving(true);
      const data = {
        descrizione: formDescrizione.trim(),
        fk_areaformazione: formArea as number,
        validita_mesi: formValiditaMesi as number,
      };
      if (editing) {
        await updateCorsoFormazione(editing.id, data);
        toast.success('Corso formazione aggiornato');
      } else {
        await createCorsoFormazione(data);
        toast.success('Corso formazione creato');
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
    try {
      await deleteCorsoFormazione(id);
      toast.success('Corso formazione eliminato');
      await loadItems();
    } catch (err: any) {
      toast.error(extractErrorMessage(err, 'Impossibile eliminare. Potrebbe essere in uso.'));
    }
  };

  const filtered = items.filter((item) =>
    item.descrizione.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <div className="text-center py-4">
        <Spinner animation="border" />
      </div>
    );
  }

  return (
    <>
      <InputGroup className="mb-2">
        <Form.Control
          placeholder="Cerca corso..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </InputGroup>
      <div className="text-end mb-2">
        <Button size="sm" onClick={handleAdd}>
          + Aggiungi Corso
        </Button>
      </div>
      <Table size="sm" striped hover responsive>
        <thead>
          <tr>
            <th>Descrizione</th>
            <th>Area</th>
            <th>Validità (mesi)</th>
            <th style={{ width: '100px' }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((item) => (
            <tr key={item.id}>
              <td>{item.descrizione}</td>
              <td>{item.fk_areaformazione_display || '-'}</td>
              <td>{item.validita_mesi}</td>
              <td>
                <Button
                  size="sm"
                  variant="outline-primary"
                  className="me-1"
                  onClick={() => handleEdit(item)}
                  title="Modifica"
                >
                  ✏️
                </Button>
                <Button
                  size="sm"
                  variant="outline-danger"
                  onClick={() => {
                    if (confirm(`Eliminare "${item.descrizione}"?`)) {
                      handleDelete(item.id);
                    }
                  }}
                  title="Elimina"
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
          {filtered.length === 0 && (
            <tr>
              <td colSpan={4} className="text-center text-muted">
                Nessun corso formazione presente.
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>
            {editing ? 'Modifica Corso Formazione' : 'Nuovo Corso Formazione'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>
                Descrizione <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                value={formDescrizione}
                onChange={(e) => setFormDescrizione(e.target.value)}
                required
                autoFocus
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>
                Area Formazione <span className="text-danger">*</span>
              </Form.Label>
              <Form.Select
                value={formArea}
                onChange={(e) => setFormArea(e.target.value ? Number(e.target.value) : '')}
                required
              >
                <option value="">-- Seleziona area --</option>
                {aree.map((a) => (
                  <option key={a.id} value={a.id}>
                    {a.descrizione}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
            <Form.Group>
              <Form.Label>
                Validità (mesi) <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                type="number"
                min={1}
                value={formValiditaMesi}
                onChange={(e) => setFormValiditaMesi(e.target.value ? Number(e.target.value) : '')}
                required
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
