/**
 * MonitoraggiPage - Gestione monitoraggi ambientali e dati produzione
 *
 * Tab 1: Dati Produzione
 * Tab 2: Monitoraggio Acqua
 * Tab 3: Monitoraggio Gas
 * Tab 4: Monitoraggio Energia Elettrica
 */

const nf0 = new Intl.NumberFormat('it-IT', { maximumFractionDigits: 0 });
const nf2 = new Intl.NumberFormat('it-IT', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});
const nf3 = new Intl.NumberFormat('it-IT', {
  minimumFractionDigits: 3,
  maximumFractionDigits: 3,
});

function toNumberOrNull(v: unknown): number | null {
  if (v === null || v === undefined || v === '') return null;
  const s = String(v).replace(',', '.');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

function fmt(v: unknown, decimals: 0 | 2 | 3): string {
  const n = toNumberOrNull(v);
  if (n === null) return '';
  if (decimals === 0) return nf0.format(n);
  if (decimals === 2) return nf2.format(n);
  return nf3.format(n);
}

import { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Card,
  Tabs,
  Tab,
  Table,
  Button,
  Spinner,
  Badge,
  Modal,
  Form,
} from 'react-bootstrap';
import { FaIndustry, FaTint, FaFire, FaBolt } from 'react-icons/fa';
import { toast } from 'react-toastify';
import {
  getDatiProduzione,
  createDatoProduzione,
  updateDatoProduzione,
  deleteDatoProduzione,
  getMonitoraggiAcqua,
  createMonitoraggioAcqua,
  updateMonitoraggioAcqua,
  deleteMonitoraggioAcqua,
  getMonitoraggiGas,
  createMonitoraggioGas,
  updateMonitoraggioGas,
  deleteMonitoraggioGas,
  getMonitoraggiEnergiaElettrica,
  createMonitoraggioEnergiaElettrica,
  updateMonitoraggioEnergiaElettrica,
  deleteMonitoraggioEnergiaElettrica,
} from '../api/monitoraggiApi';
import type {
  DatoProduzione,
  MonitoraggioAcqua,
  MonitoraggioGas,
  MonitoraggioEnergiaElettrica,
  PaginatedResponse,
  DatoProduzioneFormData,
  MonitoraggioAcquaFormData,
  MonitoraggioGasFormData,
  MonitoraggioEnergiaElettricaFormData,
} from '../types';

const PAGE_SIZE = 50;

// Industries choices (from backend model)
const INDUSTRIES_CHOICES = [
  { value: 'apparel/clothing', label: 'Apparel/clothing' },
  { value: 'aviation', label: 'Aviation' },
  { value: 'automotive', label: 'Automotive' },
  { value: 'contract', label: 'Contract' },
  { value: 'footwear', label: 'Footwear' },
  { value: 'footwear (athletic)', label: 'Footwear (Athletic)' },
  { value: 'leather goods', label: 'Leather goods' },
  { value: 'upholstery', label: 'Upholstery' },
];

export default function MonitoraggiPage() {
  const [activeTab, setActiveTab] = useState<string>('dati-produzione');

  return (
    <Container className="my-4">
      <Card>
        <Card.Header>
          <h4>Monitoraggi</h4>
        </Card.Header>
        <Card.Body>
          <Tabs
            activeKey={activeTab}
            onSelect={(k) => setActiveTab(k || 'dati-produzione')}
            className="mb-3"
          >
            <Tab
              eventKey="dati-produzione"
              title={
                <>
                  <FaIndustry className="me-2" />
                  Dati Produzione
                </>
              }
            >
              <DatiProduzioneTab />
            </Tab>
            <Tab
              eventKey="acqua"
              title={
                <>
                  <FaTint className="me-2" />
                  Monitoraggio Acqua
                </>
              }
            >
              <MonitoraggioAcquaTab />
            </Tab>
            <Tab
              eventKey="gas"
              title={
                <>
                  <FaFire className="me-2" />
                  Monitoraggio Gas
                </>
              }
            >
              <MonitoraggioGasTab />
            </Tab>
            <Tab
              eventKey="energia"
              title={
                <>
                  <FaBolt className="me-2" />
                  Monitoraggio Energia Elettrica
                </>
              }
            >
              <MonitoraggioEnergiaTab />
            </Tab>
          </Tabs>
        </Card.Body>
      </Card>
    </Container>
  );
}

// =============================================================================
// TAB 1: DATI PRODUZIONE
// =============================================================================

function DatiProduzioneTab() {
  const [items, setItems] = useState<DatoProduzione[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<DatoProduzione | null>(null);
  const [formData, setFormData] = useState<Partial<DatoProduzioneFormData>>({});
  const [saving, setSaving] = useState(false);

  const fetchItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getDatiProduzione({ page, page_size: PAGE_SIZE });
      const data: PaginatedResponse<DatoProduzione> = res.data;
      setItems(data.results);
      setTotalCount(data.count);
    } catch {
      toast.error('Errore nel caricamento dati produzione');
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  const handleAdd = () => {
    setEditingItem(null);
    setFormData({
      data_inserimento: new Date().toISOString().split('T')[0],
      industries_served: 'footwear',
      fk_tipoanimale: null,
      n_pelli: 0,
      mq: '0',
      kg: '0',
      note: '',
    });
    setShowModal(true);
  };

  const handleEdit = (item: DatoProduzione) => {
    setEditingItem(item);
    setFormData({
      data_inserimento: item.data_inserimento,
      industries_served: item.industries_served,
      fk_tipoanimale: item.fk_tipoanimale,
      n_pelli: item.n_pelli,
      mq: item.mq,
      kg: item.kg || '',
      note: item.note || '',
    });
    setShowModal(true);
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      if (editingItem) {
        await updateDatoProduzione(
          editingItem.id,
          formData as Partial<DatoProduzioneFormData>
        );
        toast.success('Dato produzione aggiornato');
      } else {
        await createDatoProduzione(formData as DatoProduzioneFormData);
        toast.success('Dato produzione creato');
      }
      setShowModal(false);
      fetchItems();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Errore salvataggio');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Eliminare questo dato produzione?')) return;
    try {
      await deleteDatoProduzione(id);
      toast.success('Dato produzione eliminato');
      fetchItems();
    } catch {
      toast.error('Errore eliminazione');
    }
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('it-IT');
  };

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <span>
          <Badge bg="secondary">{totalCount}</Badge> record
        </span>
        <Button variant="primary" size="sm" onClick={handleAdd}>
          + Aggiungi dato produzione
        </Button>
      </div>

      {loading ? (
        <div className="text-center py-4">
          <Spinner animation="border" />
        </div>
      ) : (
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>Data Inserimento</th>
              <th>Destinazione d'uso</th>
              <th>N. Pelli</th>
              <th>Mq.</th>
              <th>Kg.</th>
              <th>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{formatDate(item.data_inserimento)}</td>
                <td>{item.industries_served_display}</td>
                <td className="text-end">{fmt(item.n_pelli, 3)}</td>
                <td className="text-end">{fmt(item.mq, 3)}</td>
                <td className="text-end">
                  {item.kg == null ? '-' : fmt(item.kg, 3)}
                </td>
                <td>
                  <Button
                    variant="outline-primary"
                    size="sm"
                    className="me-2"
                    onClick={() => handleEdit(item)}
                  >
                    Modifica
                  </Button>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={() => handleDelete(item.id)}
                  >
                    Elimina
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      {/* Pagination */}
      {totalCount > PAGE_SIZE && (
        <div className="d-flex justify-content-between">
          <Button disabled={page === 1} onClick={() => setPage(page - 1)}>
            Precedente
          </Button>
          <span>
            Pagina {page} di {Math.ceil(totalCount / PAGE_SIZE)}
          </span>
          <Button
            disabled={page >= Math.ceil(totalCount / PAGE_SIZE)}
            onClick={() => setPage(page + 1)}
          >
            Successiva
          </Button>
        </div>
      )}

      {/* Modal Form */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>
            {editingItem ? 'Modifica' : 'Aggiungi'} Dato Produzione
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Data Inserimento *</Form.Label>
              <Form.Control
                type="date"
                value={formData.data_inserimento || ''}
                onChange={(e) =>
                  setFormData({ ...formData, data_inserimento: e.target.value })
                }
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Destinazione d'uso *</Form.Label>
              <Form.Select
                value={formData.industries_served || ''}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    industries_served: e.target.value,
                  })
                }
                required
              >
                {INDUSTRIES_CHOICES.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>N. Pelli *</Form.Label>
              <Form.Control
                type="number"
                value={formData.n_pelli || 0}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    n_pelli: parseInt(e.target.value) || 0,
                  })
                }
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Mq. *</Form.Label>
              <Form.Control
                type="number"
                step="0.001"
                value={formData.mq || ''}
                onChange={(e) =>
                  setFormData({ ...formData, mq: e.target.value })
                }
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Kg.</Form.Label>
              <Form.Control
                type="number"
                step="0.001"
                value={formData.kg || ''}
                onChange={(e) =>
                  setFormData({ ...formData, kg: e.target.value })
                }
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={formData.note || ''}
                onChange={(e) =>
                  setFormData({ ...formData, note: e.target.value })
                }
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Annulla
          </Button>
          <Button variant="primary" onClick={handleSave} disabled={saving}>
            {saving ? 'Salvataggio...' : 'Salva'}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

// =============================================================================
// TAB 2: MONITORAGGIO ACQUA
// =============================================================================

function MonitoraggioAcquaTab() {
  const [items, setItems] = useState<MonitoraggioAcqua[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<MonitoraggioAcqua | null>(
    null
  );
  const [formData, setFormData] = useState<Partial<MonitoraggioAcquaFormData>>(
    {}
  );
  const [saving, setSaving] = useState(false);

  const fetchItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getMonitoraggiAcqua({ page, page_size: PAGE_SIZE });
      const data: PaginatedResponse<MonitoraggioAcqua> = res.data;
      setItems(data.results);
      setTotalCount(data.count);
    } catch {
      toast.error('Errore nel caricamento monitoraggi acqua');
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  const handleAdd = () => {
    setEditingItem(null);
    setFormData({
      data_lettura: new Date().toISOString().split('T')[0],
      mc_in: 0,
      mc_out: 0,
      note: '',
    });
    setShowModal(true);
  };

  const handleEdit = (item: MonitoraggioAcqua) => {
    setEditingItem(item);
    setFormData({
      data_lettura: item.data_lettura,
      mc_in: item.mc_in,
      mc_out: item.mc_out,
      note: item.note || '',
    });
    setShowModal(true);
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      if (editingItem) {
        await updateMonitoraggioAcqua(
          editingItem.id,
          formData as Partial<MonitoraggioAcquaFormData>
        );
        toast.success('Monitoraggio acqua aggiornato');
      } else {
        await createMonitoraggioAcqua(formData as MonitoraggioAcquaFormData);
        toast.success('Monitoraggio acqua creato');
      }
      setShowModal(false);
      fetchItems();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Errore salvataggio');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Eliminare questo monitoraggio acqua?')) return;
    try {
      await deleteMonitoraggioAcqua(id);
      toast.success('Monitoraggio acqua eliminato');
      fetchItems();
    } catch {
      toast.error('Errore eliminazione');
    }
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('it-IT');
  };

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <span>
          <Badge bg="secondary">{totalCount}</Badge> record
        </span>
        <Button variant="primary" size="sm" onClick={handleAdd}>
          + Aggiungi monitoraggio acqua
        </Button>
      </div>

      {loading ? (
        <div className="text-center py-4">
          <Spinner animation="border" />
        </div>
      ) : (
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>Data Lettura</th>
              <th>MC in ingresso</th>
              <th>MC in uscita</th>
              <th>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{formatDate(item.data_lettura)}</td>
                <td className="text-end">{fmt(item.mc_in, 3)}</td>
                <td className="text-end">{fmt(item.mc_out, 3)}</td>
                <td>
                  <Button
                    variant="outline-primary"
                    size="sm"
                    className="me-2"
                    onClick={() => handleEdit(item)}
                  >
                    Modifica
                  </Button>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={() => handleDelete(item.id)}
                  >
                    Elimina
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      {/* Pagination */}
      {totalCount > PAGE_SIZE && (
        <div className="d-flex justify-content-between">
          <Button disabled={page === 1} onClick={() => setPage(page - 1)}>
            Precedente
          </Button>
          <span>
            Pagina {page} di {Math.ceil(totalCount / PAGE_SIZE)}
          </span>
          <Button
            disabled={page >= Math.ceil(totalCount / PAGE_SIZE)}
            onClick={() => setPage(page + 1)}
          >
            Successiva
          </Button>
        </div>
      )}

      {/* Modal Form */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>
            {editingItem ? 'Modifica' : 'Aggiungi'} Monitoraggio Acqua
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Data Lettura *</Form.Label>
              <Form.Control
                type="date"
                value={formData.data_lettura || ''}
                onChange={(e) =>
                  setFormData({ ...formData, data_lettura: e.target.value })
                }
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>MC in ingresso *</Form.Label>
              <Form.Control
                type="number"
                value={formData.mc_in || 0}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    mc_in: parseInt(e.target.value) || 0,
                  })
                }
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>MC in uscita *</Form.Label>
              <Form.Control
                type="number"
                value={formData.mc_out || 0}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    mc_out: parseInt(e.target.value) || 0,
                  })
                }
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={formData.note || ''}
                onChange={(e) =>
                  setFormData({ ...formData, note: e.target.value })
                }
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Annulla
          </Button>
          <Button variant="primary" onClick={handleSave} disabled={saving}>
            {saving ? 'Salvataggio...' : 'Salva'}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

// =============================================================================
// TAB 3: MONITORAGGIO GAS
// =============================================================================

function MonitoraggioGasTab() {
  const [items, setItems] = useState<MonitoraggioGas[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<MonitoraggioGas | null>(null);
  const [formData, setFormData] = useState<Partial<MonitoraggioGasFormData>>(
    {}
  );
  const [saving, setSaving] = useState(false);

  const fetchItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getMonitoraggiGas({ page, page_size: PAGE_SIZE });
      const data: PaginatedResponse<MonitoraggioGas> = res.data;
      setItems(data.results);
      setTotalCount(data.count);
    } catch {
      toast.error('Errore nel caricamento monitoraggi gas');
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  const handleAdd = () => {
    setEditingItem(null);
    setFormData({
      data_lettura: new Date().toISOString().split('T')[0],
      mc_in: '0',
      note: '',
    });
    setShowModal(true);
  };

  const handleEdit = (item: MonitoraggioGas) => {
    setEditingItem(item);
    setFormData({
      data_lettura: item.data_lettura,
      mc_in: item.mc_in,
      note: item.note || '',
    });
    setShowModal(true);
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      if (editingItem) {
        await updateMonitoraggioGas(
          editingItem.id,
          formData as Partial<MonitoraggioGasFormData>
        );
        toast.success('Monitoraggio gas aggiornato');
      } else {
        await createMonitoraggioGas(formData as MonitoraggioGasFormData);
        toast.success('Monitoraggio gas creato');
      }
      setShowModal(false);
      fetchItems();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Errore salvataggio');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Eliminare questo monitoraggio gas?')) return;
    try {
      await deleteMonitoraggioGas(id);
      toast.success('Monitoraggio gas eliminato');
      fetchItems();
    } catch {
      toast.error('Errore eliminazione');
    }
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('it-IT');
  };

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <span>
          <Badge bg="secondary">{totalCount}</Badge> record
        </span>
        <Button variant="primary" size="sm" onClick={handleAdd}>
          + Aggiungi monitoraggio gas
        </Button>
      </div>

      {loading ? (
        <div className="text-center py-4">
          <Spinner animation="border" />
        </div>
      ) : (
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>Data Lettura</th>
              <th>MC in ingresso</th>
              <th>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{formatDate(item.data_lettura)}</td>
                <td className="text-end">{fmt(item.mc_in, 3)}</td>
                <td>
                  <Button
                    variant="outline-primary"
                    size="sm"
                    className="me-2"
                    onClick={() => handleEdit(item)}
                  >
                    Modifica
                  </Button>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={() => handleDelete(item.id)}
                  >
                    Elimina
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      {/* Pagination */}
      {totalCount > PAGE_SIZE && (
        <div className="d-flex justify-content-between">
          <Button disabled={page === 1} onClick={() => setPage(page - 1)}>
            Precedente
          </Button>
          <span>
            Pagina {page} di {Math.ceil(totalCount / PAGE_SIZE)}
          </span>
          <Button
            disabled={page >= Math.ceil(totalCount / PAGE_SIZE)}
            onClick={() => setPage(page + 1)}
          >
            Successiva
          </Button>
        </div>
      )}

      {/* Modal Form */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>
            {editingItem ? 'Modifica' : 'Aggiungi'} Monitoraggio Gas
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Data Lettura *</Form.Label>
              <Form.Control
                type="date"
                value={formData.data_lettura || ''}
                onChange={(e) =>
                  setFormData({ ...formData, data_lettura: e.target.value })
                }
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>MC in ingresso *</Form.Label>
              <Form.Control
                type="number"
                step="0.001"
                value={formData.mc_in || ''}
                onChange={(e) =>
                  setFormData({ ...formData, mc_in: e.target.value })
                }
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={formData.note || ''}
                onChange={(e) =>
                  setFormData({ ...formData, note: e.target.value })
                }
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Annulla
          </Button>
          <Button variant="primary" onClick={handleSave} disabled={saving}>
            {saving ? 'Salvataggio...' : 'Salva'}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

// =============================================================================
// TAB 4: MONITORAGGIO ENERGIA ELETTRICA
// =============================================================================

function MonitoraggioEnergiaTab() {
  const [items, setItems] = useState<MonitoraggioEnergiaElettrica[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] =
    useState<MonitoraggioEnergiaElettrica | null>(null);
  const [formData, setFormData] = useState<
    Partial<MonitoraggioEnergiaElettricaFormData>
  >({});
  const [saving, setSaving] = useState(false);

  const fetchItems = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getMonitoraggiEnergiaElettrica({
        page,
        page_size: PAGE_SIZE,
      });
      const data: PaginatedResponse<MonitoraggioEnergiaElettrica> = res.data;
      setItems(data.results);
      setTotalCount(data.count);
    } catch {
      toast.error('Errore nel caricamento monitoraggi energia');
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  const handleAdd = () => {
    setEditingItem(null);
    setFormData({
      data_lettura: new Date().toISOString().split('T')[0],
      kwh_in: '0',
      note: '',
    });
    setShowModal(true);
  };

  const handleEdit = (item: MonitoraggioEnergiaElettrica) => {
    setEditingItem(item);
    setFormData({
      data_lettura: item.data_lettura,
      kwh_in: item.kwh_in,
      note: item.note || '',
    });
    setShowModal(true);
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      if (editingItem) {
        await updateMonitoraggioEnergiaElettrica(
          editingItem.id,
          formData as Partial<MonitoraggioEnergiaElettricaFormData>
        );
        toast.success('Monitoraggio energia aggiornato');
      } else {
        await createMonitoraggioEnergiaElettrica(
          formData as MonitoraggioEnergiaElettricaFormData
        );
        toast.success('Monitoraggio energia creato');
      }
      setShowModal(false);
      fetchItems();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Errore salvataggio');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Eliminare questo monitoraggio energia?')) return;
    try {
      await deleteMonitoraggioEnergiaElettrica(id);
      toast.success('Monitoraggio energia eliminato');
      fetchItems();
    } catch {
      toast.error('Errore eliminazione');
    }
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('it-IT');
  };

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <span>
          <Badge bg="secondary">{totalCount}</Badge> record
        </span>
        <Button variant="primary" size="sm" onClick={handleAdd}>
          + Aggiungi monitoraggio energia
        </Button>
      </div>

      {loading ? (
        <div className="text-center py-4">
          <Spinner animation="border" />
        </div>
      ) : (
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>Data Lettura</th>
              <th>Kwh</th>
              <th>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{formatDate(item.data_lettura)}</td>
                <td className="text-end">{fmt(item.kwh_in, 3)}</td>
                <td>
                  <Button
                    variant="outline-primary"
                    size="sm"
                    className="me-2"
                    onClick={() => handleEdit(item)}
                  >
                    Modifica
                  </Button>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={() => handleDelete(item.id)}
                  >
                    Elimina
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      {/* Pagination */}
      {totalCount > PAGE_SIZE && (
        <div className="d-flex justify-content-between">
          <Button disabled={page === 1} onClick={() => setPage(page - 1)}>
            Precedente
          </Button>
          <span>
            Pagina {page} di {Math.ceil(totalCount / PAGE_SIZE)}
          </span>
          <Button
            disabled={page >= Math.ceil(totalCount / PAGE_SIZE)}
            onClick={() => setPage(page + 1)}
          >
            Successiva
          </Button>
        </div>
      )}

      {/* Modal Form */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>
            {editingItem ? 'Modifica' : 'Aggiungi'} Monitoraggio Energia
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Data Lettura *</Form.Label>
              <Form.Control
                type="date"
                value={formData.data_lettura || ''}
                onChange={(e) =>
                  setFormData({ ...formData, data_lettura: e.target.value })
                }
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Kwh *</Form.Label>
              <Form.Control
                type="number"
                step="0.001"
                value={formData.kwh_in || ''}
                onChange={(e) =>
                  setFormData({ ...formData, kwh_in: e.target.value })
                }
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Note</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={formData.note || ''}
                onChange={(e) =>
                  setFormData({ ...formData, note: e.target.value })
                }
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Annulla
          </Button>
          <Button variant="primary" onClick={handleSave} disabled={saving}>
            {saving ? 'Salvataggio...' : 'Salva'}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
