/**
 * TabelleGenericheHRPage - Gestione tabelle di lookup HR
 *
 * Layout a card (stile TabelleGenerichePage di articoli):
 * - Centri di Lavoro
 * - Reparti (Ward)
 * - Mansioni (Role)
 * - Incarichi Sicurezza (Safety_Role)
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
import { FaCogs, FaBuilding, FaUserTie, FaShieldAlt } from 'react-icons/fa';
import {
  getCentriDiLavoro,
  createCentroDiLavoro,
  updateCentroDiLavoro,
  deleteCentroDiLavoro,
  getReparti,
  createReparto,
  updateReparto,
  deleteReparto,
  getMansioni,
  createMansione,
  updateMansione,
  deleteMansione,
  getSafetyRoles,
  createSafetyRole,
  updateSafetyRole,
  deleteSafetyRole,
} from '../api';
import type { CentrodiLavoro, Ward, Role, SafetyRole } from '../types';

export default function TabelleGenericheHRPage() {
  return (
    <Container className="my-4">
      <h3 className="mb-4">Tabelle Generiche - Human Resources</h3>
      <Row className="g-4">
        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaCogs className="me-2" />
              Centri di Lavoro
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <CentriDiLavoroCard />
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaBuilding className="me-2" />
              Reparti
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <RepartiCard />
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaUserTie className="me-2" />
              Mansioni
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <MansioniCard />
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card style={{ height: '500px' }} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaShieldAlt className="me-2" />
              Incarichi Sicurezza
            </Card.Header>
            <Card.Body style={{ overflowY: 'auto', maxHeight: '420px' }}>
              <IncarichiSicurezzaCard />
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

// =============================================================================
// CENTRI DI LAVORO CARD
// =============================================================================

function CentriDiLavoroCard() {
  const [items, setItems] = useState<CentrodiLavoro[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<CentrodiLavoro | null>(null);
  const [formDescription, setFormDescription] = useState('');
  const [saving, setSaving] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getCentriDiLavoro({ page_size: 1000 });
      setItems(res.data.results);
    } catch {
      toast.error('Errore caricamento centri di lavoro');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormDescription('');
    setShowModal(true);
  };

  const handleEdit = (item: CentrodiLavoro) => {
    setEditing(item);
    setFormDescription(item.description);
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formDescription.trim()) {
      toast.warning('La descrizione è obbligatoria');
      return;
    }

    try {
      setSaving(true);
      if (editing) {
        await updateCentroDiLavoro(editing.id, { description: formDescription.trim() });
        toast.success('Centro di lavoro aggiornato');
      } else {
        await createCentroDiLavoro({ description: formDescription.trim() });
        toast.success('Centro di lavoro creato');
      }
      setShowModal(false);
      await loadItems();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore salvataggio';
      toast.error(msg);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteCentroDiLavoro(id);
      toast.success('Centro di lavoro eliminato');
      await loadItems();
      setDeleteId(null);
    } catch (err: any) {
      const msg =
        err.response?.data?.detail ||
        'Impossibile eliminare. Potrebbe essere in uso.';
      toast.error(msg);
      setDeleteId(null);
    }
  };

  const filtered = items.filter((item) =>
    item.description.toLowerCase().includes(search.toLowerCase())
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
          placeholder="Cerca centro..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </InputGroup>
      <div className="text-end mb-2">
        <Button size="sm" onClick={handleAdd}>
          + Aggiungi Centro
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
              <td>{item.description}</td>
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
                  onClick={() => {
                    if (confirm(`Eliminare "${item.description}"?`)) {
                      setDeleteId(item.id);
                      handleDelete(item.id);
                    }
                  }}
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
          {filtered.length === 0 && (
            <tr>
              <td colSpan={2} className="text-center text-muted">
                Nessun centro di lavoro presente.
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>
            {editing ? 'Modifica Centro di Lavoro' : 'Nuovo Centro di Lavoro'}
          </Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group>
              <Form.Label>
                Descrizione <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                value={formDescription}
                onChange={(e) => setFormDescription(e.target.value)}
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
// REPARTI CARD
// =============================================================================

function RepartiCard() {
  const [items, setItems] = useState<Ward[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<Ward | null>(null);
  const [formDescription, setFormDescription] = useState('');
  const [saving, setSaving] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getReparti({ page_size: 1000 });
      setItems(res.data.results);
    } catch {
      toast.error('Errore caricamento reparti');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormDescription('');
    setShowModal(true);
  };

  const handleEdit = (item: Ward) => {
    setEditing(item);
    setFormDescription(item.description);
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formDescription.trim()) {
      toast.warning('La descrizione è obbligatoria');
      return;
    }

    try {
      setSaving(true);
      if (editing) {
        await updateReparto(editing.id, { description: formDescription.trim() });
        toast.success('Reparto aggiornato');
      } else {
        await createReparto({ description: formDescription.trim() });
        toast.success('Reparto creato');
      }
      setShowModal(false);
      await loadItems();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore salvataggio';
      toast.error(msg);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteReparto(id);
      toast.success('Reparto eliminato');
      await loadItems();
      setDeleteId(null);
    } catch (err: any) {
      const msg =
        err.response?.data?.detail ||
        'Impossibile eliminare. Potrebbe essere in uso.';
      toast.error(msg);
      setDeleteId(null);
    }
  };

  const filtered = items.filter((item) =>
    item.description.toLowerCase().includes(search.toLowerCase())
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
          placeholder="Cerca reparto..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </InputGroup>
      <div className="text-end mb-2">
        <Button size="sm" onClick={handleAdd}>
          + Aggiungi Reparto
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
              <td>{item.description}</td>
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
                  onClick={() => {
                    if (confirm(`Eliminare "${item.description}"?`)) {
                      setDeleteId(item.id);
                      handleDelete(item.id);
                    }
                  }}
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
          {filtered.length === 0 && (
            <tr>
              <td colSpan={2} className="text-center text-muted">
                Nessun reparto presente.
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>{editing ? 'Modifica Reparto' : 'Nuovo Reparto'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group>
              <Form.Label>
                Descrizione <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                value={formDescription}
                onChange={(e) => setFormDescription(e.target.value)}
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
// MANSIONI CARD
// =============================================================================

function MansioniCard() {
  const [items, setItems] = useState<Role[]>([]);
  const [reparti, setReparti] = useState<Ward[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<Role | null>(null);
  const [formDescription, setFormDescription] = useState('');
  const [formReparto, setFormReparto] = useState<number | ''>('');
  const [saving, setSaving] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const [mansioniRes, repartiRes] = await Promise.all([
        getMansioni({ page_size: 1000 }),
        getReparti({ page_size: 1000 }),
      ]);
      setItems(mansioniRes.data.results);
      setReparti(repartiRes.data.results);
    } catch {
      toast.error('Errore caricamento mansioni');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const handleAdd = () => {
    setEditing(null);
    setFormDescription('');
    setFormReparto('');
    setShowModal(true);
  };

  const handleEdit = (item: Role) => {
    setEditing(item);
    setFormDescription(item.description);
    setFormReparto(item.fk_reparto || '');
    setShowModal(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formDescription.trim()) {
      toast.warning('La descrizione è obbligatoria');
      return;
    }

    try {
      setSaving(true);
      const data = {
        description: formDescription.trim(),
        fk_reparto: formReparto ? (formReparto as number) : null,
      };
      if (editing) {
        await updateMansione(editing.id, data);
        toast.success('Mansione aggiornata');
      } else {
        await createMansione(data);
        toast.success('Mansione creata');
      }
      setShowModal(false);
      await loadItems();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore salvataggio';
      toast.error(msg);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteMansione(id);
      toast.success('Mansione eliminata');
      await loadItems();
      setDeleteId(null);
    } catch (err: any) {
      const msg =
        err.response?.data?.detail ||
        'Impossibile eliminare. Potrebbe essere in uso.';
      toast.error(msg);
      setDeleteId(null);
    }
  };

  const filtered = items.filter((item) =>
    item.description.toLowerCase().includes(search.toLowerCase())
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
          placeholder="Cerca mansione..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </InputGroup>
      <div className="text-end mb-2">
        <Button size="sm" onClick={handleAdd}>
          + Aggiungi Mansione
        </Button>
      </div>
      <Table size="sm" striped hover responsive>
        <thead>
          <tr>
            <th>Descrizione</th>
            <th>Reparto</th>
            <th style={{ width: '100px' }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((item) => (
            <tr key={item.id}>
              <td>{item.description}</td>
              <td>{item.fk_reparto_display || '-'}</td>
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
                  onClick={() => {
                    if (confirm(`Eliminare "${item.description}"?`)) {
                      setDeleteId(item.id);
                      handleDelete(item.id);
                    }
                  }}
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
          {filtered.length === 0 && (
            <tr>
              <td colSpan={3} className="text-center text-muted">
                Nessuna mansione presente.
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>{editing ? 'Modifica Mansione' : 'Nuova Mansione'}</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleSave}>
          <Modal.Body>
            <Form.Group className="mb-3">
              <Form.Label>
                Descrizione <span className="text-danger">*</span>
              </Form.Label>
              <Form.Control
                value={formDescription}
                onChange={(e) => setFormDescription(e.target.value)}
                required
                autoFocus
              />
            </Form.Group>
            <Form.Group>
              <Form.Label>Reparto (opzionale)</Form.Label>
              <Form.Select
                value={formReparto}
                onChange={(e) => setFormReparto(e.target.value ? Number(e.target.value) : '')}
              >
                <option value="">-- Nessun reparto --</option>
                {reparti.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.description}
                  </option>
                ))}
              </Form.Select>
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
// INCARICHI SICUREZZA CARD
// =============================================================================

function IncarichiSicurezzaCard() {
  const [items, setItems] = useState<SafetyRole[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<SafetyRole | null>(null);
  const [formDescrizione, setFormDescrizione] = useState('');
  const [formNote, setFormNote] = useState('');
  const [saving, setSaving] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const loadItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getSafetyRoles({ page_size: 1000 });
      setItems(res.data.results);
    } catch {
      toast.error('Errore caricamento incarichi sicurezza');
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
    setFormNote('');
    setShowModal(true);
  };

  const handleEdit = (item: SafetyRole) => {
    setEditing(item);
    setFormDescrizione(item.descrizione);
    setFormNote(item.note || '');
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
      const data = {
        descrizione: formDescrizione.trim(),
        note: formNote.trim() || null,
      };
      if (editing) {
        await updateSafetyRole(editing.id, data);
        toast.success('Incarico sicurezza aggiornato');
      } else {
        await createSafetyRole(data);
        toast.success('Incarico sicurezza creato');
      }
      setShowModal(false);
      await loadItems();
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Errore salvataggio';
      toast.error(msg);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteSafetyRole(id);
      toast.success('Incarico sicurezza eliminato');
      await loadItems();
      setDeleteId(null);
    } catch (err: any) {
      const msg =
        err.response?.data?.detail ||
        'Impossibile eliminare. Potrebbe essere in uso.';
      toast.error(msg);
      setDeleteId(null);
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
          placeholder="Cerca incarico..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </InputGroup>
      <div className="text-end mb-2">
        <Button size="sm" onClick={handleAdd}>
          + Aggiungi Incarico
        </Button>
      </div>
      <Table size="sm" striped hover responsive>
        <thead>
          <tr>
            <th>Descrizione</th>
            <th>Note</th>
            <th style={{ width: '100px' }}>Azioni</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((item) => (
            <tr key={item.id}>
              <td>{item.descrizione}</td>
              <td>{item.note || '-'}</td>
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
                  onClick={() => {
                    if (confirm(`Eliminare "${item.descrizione}"?`)) {
                      setDeleteId(item.id);
                      handleDelete(item.id);
                    }
                  }}
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
          {filtered.length === 0 && (
            <tr>
              <td colSpan={3} className="text-center text-muted">
                Nessun incarico sicurezza presente.
              </td>
            </tr>
          )}
        </tbody>
      </Table>

      <Modal show={showModal} onHide={() => setShowModal(false)} backdrop="static">
        <Modal.Header closeButton>
          <Modal.Title>
            {editing ? 'Modifica Incarico Sicurezza' : 'Nuovo Incarico Sicurezza'}
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
            <Form.Group>
              <Form.Label>Note (opzionale)</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
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
