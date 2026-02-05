/**
 * LottoFormPage - Form create/edit lotto con sotto-tabelle ScelteLotto e Origini.
 *
 * Le sotto-tabelle appaiono SOLO dopo il primo salvataggio (quando il lotto ha un id).
 */
import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container, Card, Form, Button, Row, Col, Spinner, Alert,
  Table, Badge, Modal, ButtonGroup,
} from 'react-bootstrap';
import { toast } from 'react-toastify';
import ConfirmModal from '@/components/common/ConfirmModal';
import {
  getLotto, createLotto, updateLotto,
  getFornitoriLookup, getTipiAnimale, getTipiGrezzo, getScelte,
  getScelteLotto, createSceltaLotto, updateSceltaLotto, deleteSceltaLotto,
  getLottoOrigini, createLottoOrigine, deleteLottoOrigine,
  getRegioni, getSubregioni, getNazioni,
} from '../api/acquistopelliApi';
import type {
  LottoDetail, LottoCreate, Fornitore, TipoAnimale, TipoGrezzo,
  Scelta, SceltaLotto, LottoOrigine,
  LwgRegione, LwgSubregione, Nazione as NazioneType,
} from '../types';

interface LottoFormData {
  data_acquisto: string;
  identificativo: string;
  fk_fornitore: string;
  fk_tipoanimale: string;
  fk_tipogrezzo: string;
  fk_macello: string;
  origine: string;
  documento: string;
  is_lwg: boolean;
  peso_totale: string;
  pezzi: string;
  prezzo_unitario: string;
  spese_accessorie: string;
  kg_km: string;
  note: string;
}

const emptyForm: LottoFormData = {
  data_acquisto: '', identificativo: '', fk_fornitore: '',
  fk_tipoanimale: '', fk_tipogrezzo: '', fk_macello: '',
  origine: '', documento: '', is_lwg: false,
  peso_totale: '', pezzi: '', prezzo_unitario: '',
  spese_accessorie: '', kg_km: '', note: '',
};

export default function LottoFormPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = !!id && id !== 'new';
  const lottoId = isEdit ? Number(id) : null;

  // Form state
  const [formData, setFormData] = useState<LottoFormData>(emptyForm);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Lookups
  const [fornitori, setFornitori] = useState<Fornitore[]>([]);
  const [tipiAnimale, setTipiAnimale] = useState<TipoAnimale[]>([]);
  const [tipiGrezzo, setTipiGrezzo] = useState<TipoGrezzo[]>([]);
  const [scelteList, setScelteList] = useState<Scelta[]>([]);

  // Sotto-tabelle
  const [scelteLotto, setScelteLotto] = useState<SceltaLotto[]>([]);
  const [origini, setOrigini] = useState<LottoOrigine[]>([]);

  // Modal Scelta
  const [showSceltaModal, setShowSceltaModal] = useState(false);
  const [editingScelta, setEditingScelta] = useState<SceltaLotto | null>(null);
  const [sceltaForm, setSceltaForm] = useState({ fk_scelta: '', pezzi: '' });
  const [savingScelta, setSavingScelta] = useState(false);

  // Modal Origine
  const [showOrigineModal, setShowOrigineModal] = useState(false);
  const [origineForm, setOrigineForm] = useState({
    livello_precisione: 'country' as 'country' | 'region' | 'subregion',
    nazione: '', regione: '', subregione: '',
    quota_percentuale: '', qta_stimata: '', fonte_dato: '', note: '',
  });
  const [savingOrigine, setSavingOrigine] = useState(false);

  // Lookups per origine
  const [regioniList, setRegioniList] = useState<LwgRegione[]>([]);
  const [subregioniList, setSubregioniList] = useState<LwgSubregione[]>([]);
  const [nazioniList, setNazioniList] = useState<NazioneType[]>([]);

  // Delete
  const [deleteSceltaId, setDeleteSceltaId] = useState<number | null>(null);
  const [deleteOrigineId, setDeleteOrigineId] = useState<number | null>(null);

  // Load lookups
  useEffect(() => {
    Promise.all([
      getFornitoriLookup(),
      getTipiAnimale({ page_size: 1000 }),
      getTipiGrezzo({ page_size: 1000 }),
      getScelte({ page_size: 1000 }),
      getRegioni({ page_size: 1000 }),
      getSubregioni({ page_size: 1000 }),
      getNazioni({ page_size: 1000 }),
    ]).then(([fRes, aRes, gRes, sRes, rRes, srRes, nRes]) => {
      setFornitori(fRes.data.results);
      setTipiAnimale(aRes.data.results);
      setTipiGrezzo(gRes.data.results);
      setScelteList(sRes.data.results);
      setRegioniList(rRes.data.results);
      setSubregioniList(srRes.data.results);
      setNazioniList(nRes.data.results);
    }).catch(() => toast.error('Errore caricamento dati'));
  }, []);

  // Load lotto
  const loadLotto = useCallback(async () => {
    if (!lottoId) return;
    setLoading(true);
    setError(null);
    try {
      const res = await getLotto(lottoId);
      const d: LottoDetail = res.data;
      setFormData({
        data_acquisto: d.data_acquisto || '',
        identificativo: d.identificativo || '',
        fk_fornitore: d.fk_fornitore?.toString() || '',
        fk_tipoanimale: d.fk_tipoanimale?.toString() || '',
        fk_tipogrezzo: d.fk_tipogrezzo?.toString() || '',
        fk_macello: d.fk_macello?.toString() || '',
        origine: d.origine || '',
        documento: d.documento || '',
        is_lwg: d.is_lwg,
        peso_totale: d.peso_totale || '',
        pezzi: d.pezzi?.toString() || '',
        prezzo_unitario: d.prezzo_unitario || '',
        spese_accessorie: d.spese_accessorie || '',
        kg_km: d.kg_km || '',
        note: d.note || '',
      });
      setScelteLotto(d.scelte || []);
      setOrigini(d.origini || []);
    } catch {
      setError('Errore nel caricamento del lotto');
    } finally {
      setLoading(false);
    }
  }, [lottoId]);

  useEffect(() => { if (isEdit) loadLotto(); }, [isEdit, loadLotto]);

  const handleChange = (field: keyof LottoFormData, value: string | boolean) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const strOrNull = (v: string) => v.trim() || null;
  const intOrNull = (v: string) => { const n = parseInt(v, 10); return isNaN(n) ? null : n; };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.data_acquisto || !formData.identificativo || !formData.fk_fornitore) {
      toast.warning('Data, identificativo e fornitore sono obbligatori');
      return;
    }
    setSaving(true);
    try {
      const payload: LottoCreate = {
        data_acquisto: formData.data_acquisto,
        identificativo: formData.identificativo,
        fk_fornitore: parseInt(formData.fk_fornitore, 10),
        fk_tipoanimale: intOrNull(formData.fk_tipoanimale),
        fk_tipogrezzo: intOrNull(formData.fk_tipogrezzo),
        fk_macello: intOrNull(formData.fk_macello),
        origine: strOrNull(formData.origine),
        documento: strOrNull(formData.documento),
        is_lwg: formData.is_lwg,
        peso_totale: strOrNull(formData.peso_totale),
        pezzi: intOrNull(formData.pezzi),
        prezzo_unitario: strOrNull(formData.prezzo_unitario),
        spese_accessorie: strOrNull(formData.spese_accessorie),
        kg_km: strOrNull(formData.kg_km),
        note: strOrNull(formData.note),
      };

      if (isEdit && lottoId) {
        await updateLotto(lottoId, payload);
        toast.success('Lotto aggiornato');
        loadLotto();
      } else {
        const res = await createLotto(payload);
        toast.success('Lotto creato');
        navigate(`/acquistopelli/lotti/${res.data.id}`, { replace: true });
      }
    } catch {
      toast.error('Errore nel salvataggio');
    } finally {
      setSaving(false);
    }
  };

  // --- Scelte Lotto handlers ---
  const openSceltaModal = (item?: SceltaLotto) => {
    if (item) {
      setEditingScelta(item);
      setSceltaForm({ fk_scelta: item.fk_scelta.toString(), pezzi: item.pezzi?.toString() || '' });
    } else {
      setEditingScelta(null);
      setSceltaForm({ fk_scelta: '', pezzi: '' });
    }
    setShowSceltaModal(true);
  };

  const handleSaveScelta = async () => {
    if (!sceltaForm.fk_scelta) { toast.warning('Seleziona una scelta'); return; }
    setSavingScelta(true);
    try {
      const data = {
        fk_lotto: lottoId!,
        fk_scelta: parseInt(sceltaForm.fk_scelta, 10),
        pezzi: intOrNull(sceltaForm.pezzi),
      };
      if (editingScelta) {
        await updateSceltaLotto(editingScelta.id, data);
        toast.success('Scelta aggiornata');
      } else {
        await createSceltaLotto(data);
        toast.success('Scelta aggiunta');
      }
      setShowSceltaModal(false);
      loadLotto();
    } catch {
      toast.error('Errore salvataggio scelta');
    } finally {
      setSavingScelta(false);
    }
  };

  const handleDeleteScelta = async (scId: number) => {
    try {
      await deleteSceltaLotto(scId);
      toast.success('Scelta rimossa');
      loadLotto();
    } catch {
      toast.error('Errore eliminazione scelta');
    }
    setDeleteSceltaId(null);
  };

  // --- Origine handlers ---
  const openOrigineModal = () => {
    setOrigineForm({
      livello_precisione: 'country',
      nazione: '', regione: '', subregione: '',
      quota_percentuale: '', qta_stimata: '', fonte_dato: '', note: '',
    });
    setShowOrigineModal(true);
  };

  const handleSaveOrigine = async () => {
    const { livello_precisione, nazione, regione, subregione } = origineForm;
    if (
      (livello_precisione === 'country' && !nazione) ||
      (livello_precisione === 'region' && !regione) ||
      (livello_precisione === 'subregion' && !subregione)
    ) {
      toast.warning('Seleziona almeno un livello geografico');
      return;
    }
    setSavingOrigine(true);
    try {
      await createLottoOrigine({
        lotto: lottoId!,
        livello_precisione,
        nazione: intOrNull(nazione),
        regione: intOrNull(regione),
        subregione: intOrNull(subregione),
        quota_percentuale: strOrNull(origineForm.quota_percentuale),
        qta_stimata: strOrNull(origineForm.qta_stimata),
        fonte_dato: strOrNull(origineForm.fonte_dato),
        note: strOrNull(origineForm.note),
      });
      toast.success('Origine aggiunta');
      setShowOrigineModal(false);
      loadLotto();
    } catch {
      toast.error('Errore salvataggio origine');
    } finally {
      setSavingOrigine(false);
    }
  };

  const handleDeleteOrigine = async (oId: number) => {
    try {
      await deleteLottoOrigine(oId);
      toast.success('Origine rimossa');
      loadLotto();
    } catch {
      toast.error('Errore eliminazione origine');
    }
    setDeleteOrigineId(null);
  };

  const totalePezziScelte = scelteLotto.reduce((sum, s) => sum + (s.pezzi || 0), 0);

  if (loading) return <Container className="my-4 text-center"><Spinner /></Container>;
  if (error) return <Container className="my-4"><Alert variant="danger">{error}</Alert></Container>;

  return (
    <Container className="my-4">
      {/* FORM LOTTO */}
      <Card className="shadow-sm mb-4">
        <Card.Header className="fw-bold">
          {isEdit ? `Modifica Lotto - ${formData.identificativo}` : 'Nuovo Lotto'}
        </Card.Header>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            <Row className="mb-3">
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Data Acquisto *</Form.Label>
                  <Form.Control type="date" value={formData.data_acquisto}
                    onChange={(e) => handleChange('data_acquisto', e.target.value)} required />
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Identificativo *</Form.Label>
                  <Form.Control value={formData.identificativo}
                    onChange={(e) => handleChange('identificativo', e.target.value)} required maxLength={10} />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group>
                  <Form.Label>Fornitore *</Form.Label>
                  <Form.Select value={formData.fk_fornitore}
                    onChange={(e) => handleChange('fk_fornitore', e.target.value)} required>
                    <option value="">-- Seleziona --</option>
                    {fornitori.map((f) => <option key={f.id} value={f.id}>{f.ragionesociale}</option>)}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={2} className="d-flex align-items-end">
                <Form.Check type="checkbox" label="LWG" checked={formData.is_lwg}
                  onChange={(e) => handleChange('is_lwg', e.target.checked)} />
              </Col>
            </Row>

            <Row className="mb-3">
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Tipo Animale</Form.Label>
                  <Form.Select value={formData.fk_tipoanimale}
                    onChange={(e) => handleChange('fk_tipoanimale', e.target.value)}>
                    <option value="">--</option>
                    {tipiAnimale.map((a) => <option key={a.id} value={a.id}>{a.descrizione}</option>)}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Tipo Grezzo</Form.Label>
                  <Form.Select value={formData.fk_tipogrezzo}
                    onChange={(e) => handleChange('fk_tipogrezzo', e.target.value)}>
                    <option value="">--</option>
                    {tipiGrezzo.map((g) => <option key={g.id} value={g.id}>{g.descrizione}</option>)}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Macello</Form.Label>
                  <Form.Select value={formData.fk_macello}
                    onChange={(e) => handleChange('fk_macello', e.target.value)}>
                    <option value="">--</option>
                    {fornitori.map((f) => <option key={f.id} value={f.id}>{f.ragionesociale}</option>)}
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={3}>
                <Form.Group>
                  <Form.Label>Documento</Form.Label>
                  <Form.Control value={formData.documento}
                    onChange={(e) => handleChange('documento', e.target.value)} maxLength={10} />
                </Form.Group>
              </Col>
            </Row>

            <Row className="mb-3">
              <Col md={2}>
                <Form.Group>
                  <Form.Label>Peso Totale</Form.Label>
                  <Form.Control type="number" step="0.01" value={formData.peso_totale}
                    onChange={(e) => handleChange('peso_totale', e.target.value)} />
                </Form.Group>
              </Col>
              <Col md={2}>
                <Form.Group>
                  <Form.Label>Pezzi</Form.Label>
                  <Form.Control type="number" value={formData.pezzi}
                    onChange={(e) => handleChange('pezzi', e.target.value)} />
                </Form.Group>
              </Col>
              <Col md={2}>
                <Form.Group>
                  <Form.Label>Prezzo Unitario</Form.Label>
                  <Form.Control type="number" step="0.001" value={formData.prezzo_unitario}
                    onChange={(e) => handleChange('prezzo_unitario', e.target.value)} />
                </Form.Group>
              </Col>
              <Col md={2}>
                <Form.Group>
                  <Form.Label>Spese Accessorie</Form.Label>
                  <Form.Control type="number" step="0.001" value={formData.spese_accessorie}
                    onChange={(e) => handleChange('spese_accessorie', e.target.value)} />
                </Form.Group>
              </Col>
              <Col md={2}>
                <Form.Group>
                  <Form.Label>Kg*Km (CO2)</Form.Label>
                  <Form.Control type="number" value={formData.kg_km}
                    onChange={(e) => handleChange('kg_km', e.target.value)} />
                </Form.Group>
              </Col>
            </Row>

            <Row className="mb-3">
              <Col>
                <Form.Group>
                  <Form.Label>Note</Form.Label>
                  <Form.Control as="textarea" rows={2} value={formData.note}
                    onChange={(e) => handleChange('note', e.target.value)} />
                </Form.Group>
              </Col>
            </Row>

            <div className="d-flex justify-content-end gap-2">
              <Button variant="secondary" onClick={() => navigate('/acquistopelli')}>Annulla</Button>
              <Button variant="primary" type="submit" disabled={saving}>
                {saving ? <Spinner size="sm" /> : 'Salva'}
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>

      {/* SOTTO-TABELLE (solo se lotto salvato) */}
      {isEdit && lottoId && (
        <>
          {/* SCELTE DEL LOTTO */}
          <Card className="shadow-sm mb-4">
            <Card.Header className="d-flex justify-content-between align-items-center">
              <span className="fw-bold">Scelte del Lotto</span>
              <Button size="sm" onClick={() => openSceltaModal()}>+ Aggiungi Scelta</Button>
            </Card.Header>
            <Card.Body>
              <Table size="sm" striped hover responsive>
                <thead>
                  <tr>
                    <th>Scelta</th>
                    <th>Pezzi</th>
                    <th className="text-end">Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  {scelteLotto.length === 0 ? (
                    <tr><td colSpan={3} className="text-muted text-center">Nessuna scelta</td></tr>
                  ) : scelteLotto.map((s) => (
                    <tr key={s.id}>
                      <td>{s.scelta_descrizione || '—'}</td>
                      <td>{s.pezzi ?? '—'}</td>
                      <td className="text-end">
                        <ButtonGroup size="sm">
                          <Button variant="outline-primary" onClick={() => openSceltaModal(s)}>✏️</Button>
                          <Button variant="outline-danger" onClick={() => setDeleteSceltaId(s.id)}>🗑</Button>
                        </ButtonGroup>
                      </td>
                    </tr>
                  ))}
                </tbody>
                {scelteLotto.length > 0 && (
                  <tfoot>
                    <tr className="fw-bold">
                      <td>Totale</td>
                      <td>{totalePezziScelte}</td>
                      <td />
                    </tr>
                  </tfoot>
                )}
              </Table>
            </Card.Body>
          </Card>

          {/* ORIGINI */}
          <Card className="shadow-sm mb-4">
            <Card.Header className="d-flex justify-content-between align-items-center">
              <span className="fw-bold">Origini</span>
              <Button size="sm" onClick={openOrigineModal}>+ Aggiungi Origine</Button>
            </Card.Header>
            <Card.Body>
              <Table size="sm" striped hover responsive>
                <thead>
                  <tr>
                    <th>Livello</th>
                    <th>Paese</th>
                    <th>Regione</th>
                    <th>Subregione</th>
                    <th>Quota %</th>
                    <th className="text-end">Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  {origini.length === 0 ? (
                    <tr><td colSpan={6} className="text-muted text-center">Nessuna origine</td></tr>
                  ) : origini.map((o) => (
                    <tr key={o.id}>
                      <td><Badge bg="secondary">{o.livello_precisione}</Badge></td>
                      <td>{o.nazione_display || '—'}</td>
                      <td>{o.regione_display || '—'}</td>
                      <td>{o.subregione_display || '—'}</td>
                      <td>{o.quota_percentuale || '—'}</td>
                      <td className="text-end">
                        <Button size="sm" variant="outline-danger"
                          onClick={() => setDeleteOrigineId(o.id)}>🗑</Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </>
      )}

      {/* MODAL SCELTA */}
      <Modal show={showSceltaModal} onHide={() => setShowSceltaModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>{editingScelta ? 'Modifica Scelta' : 'Aggiungi Scelta'}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group className="mb-3">
            <Form.Label>Scelta *</Form.Label>
            <Form.Select value={sceltaForm.fk_scelta}
              onChange={(e) => setSceltaForm((p) => ({ ...p, fk_scelta: e.target.value }))}>
              <option value="">-- Seleziona --</option>
              {scelteList.map((s) => <option key={s.id} value={s.id}>{s.descrizione}</option>)}
            </Form.Select>
          </Form.Group>
          <Form.Group>
            <Form.Label>Pezzi</Form.Label>
            <Form.Control type="number" value={sceltaForm.pezzi}
              onChange={(e) => setSceltaForm((p) => ({ ...p, pezzi: e.target.value }))} />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowSceltaModal(false)}>Annulla</Button>
          <Button variant="primary" onClick={handleSaveScelta} disabled={savingScelta}>
            {savingScelta ? <Spinner size="sm" /> : 'Salva'}
          </Button>
        </Modal.Footer>
      </Modal>

      {/* MODAL ORIGINE */}
      <Modal show={showOrigineModal} onHide={() => setShowOrigineModal(false)} centered size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Aggiungi Origine</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Row className="mb-3">
            <Col md={4}>
              <Form.Group>
                <Form.Label>Livello *</Form.Label>
                <Form.Select value={origineForm.livello_precisione}
                  onChange={(e) => setOrigineForm((p) => ({
                    ...p,
                    livello_precisione: e.target.value as 'country' | 'region' | 'subregion',
                    nazione: '', regione: '', subregione: '',
                  }))}>
                  <option value="country">Country</option>
                  <option value="region">Region</option>
                  <option value="subregion">Subregion</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={8}>
              {origineForm.livello_precisione === 'country' && (
                <Form.Group>
                  <Form.Label>Nazione *</Form.Label>
                  <Form.Select value={origineForm.nazione}
                    onChange={(e) => setOrigineForm((p) => ({ ...p, nazione: e.target.value }))}>
                    <option value="">-- Seleziona --</option>
                    {nazioniList.map((n) => (
                      <option key={n.id} value={n.id}>{n.descrizione || n.sigla}</option>
                    ))}
                  </Form.Select>
                </Form.Group>
              )}
              {origineForm.livello_precisione === 'region' && (
                <Form.Group>
                  <Form.Label>Regione *</Form.Label>
                  <Form.Select value={origineForm.regione}
                    onChange={(e) => setOrigineForm((p) => ({ ...p, regione: e.target.value }))}>
                    <option value="">-- Seleziona --</option>
                    {regioniList.map((r) => (
                      <option key={r.id} value={r.id}>{r.nome_regione}</option>
                    ))}
                  </Form.Select>
                </Form.Group>
              )}
              {origineForm.livello_precisione === 'subregion' && (
                <Form.Group>
                  <Form.Label>Subregione *</Form.Label>
                  <Form.Select value={origineForm.subregione}
                    onChange={(e) => setOrigineForm((p) => ({ ...p, subregione: e.target.value }))}>
                    <option value="">-- Seleziona --</option>
                    {subregioniList.map((sr) => (
                      <option key={sr.id} value={sr.id}>{sr.nome_subregione}</option>
                    ))}
                  </Form.Select>
                </Form.Group>
              )}
            </Col>
          </Row>
          <Row className="mb-3">
            <Col md={4}>
              <Form.Group>
                <Form.Label>Quota %</Form.Label>
                <Form.Control type="number" step="0.01" value={origineForm.quota_percentuale}
                  onChange={(e) => setOrigineForm((p) => ({ ...p, quota_percentuale: e.target.value }))} />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group>
                <Form.Label>Qtà Stimata</Form.Label>
                <Form.Control type="number" step="0.001" value={origineForm.qta_stimata}
                  onChange={(e) => setOrigineForm((p) => ({ ...p, qta_stimata: e.target.value }))} />
              </Form.Group>
            </Col>
            <Col md={4}>
              <Form.Group>
                <Form.Label>Fonte Dato</Form.Label>
                <Form.Control value={origineForm.fonte_dato}
                  onChange={(e) => setOrigineForm((p) => ({ ...p, fonte_dato: e.target.value }))} />
              </Form.Group>
            </Col>
          </Row>
          <Form.Group>
            <Form.Label>Note</Form.Label>
            <Form.Control as="textarea" rows={2} value={origineForm.note}
              onChange={(e) => setOrigineForm((p) => ({ ...p, note: e.target.value }))} />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowOrigineModal(false)}>Annulla</Button>
          <Button variant="primary" onClick={handleSaveOrigine} disabled={savingOrigine}>
            {savingOrigine ? <Spinner size="sm" /> : 'Salva'}
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Confirm Modals */}
      <ConfirmModal
        show={!!deleteSceltaId}
        onHide={() => setDeleteSceltaId(null)}
        onConfirm={() => deleteSceltaId && handleDeleteScelta(deleteSceltaId)}
        message="Eliminare questa scelta?"
      />
      <ConfirmModal
        show={!!deleteOrigineId}
        onHide={() => setDeleteOrigineId(null)}
        onConfirm={() => deleteOrigineId && handleDeleteOrigine(deleteOrigineId)}
        message="Eliminare questa origine?"
      />
    </Container>
  );
}
