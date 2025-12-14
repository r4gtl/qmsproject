import { useEffect, useState } from 'react';
import { Table, Button, Spinner, Modal, Form, Row, Col } from 'react-bootstrap';
import axios from '@/api/axios';
import type {
  LwgFornitore,
} from '@/apps/anagrafiche/types/anagrafiche';
import { toast } from 'react-toastify';

interface LwgCertificateTableProps {
  fornitoreId: number;
}

/**
 * Componente che mostra una tabella dei certificati LWG e permette di aggiungerne di nuovi.
 */
const LwgCertificateTable: React.FC<LwgCertificateTableProps> = ({
  fornitoreId,
}) => {
  // Stato per elenco certificati LWG
  const [certificati, setCertificati] = useState<LwgFornitore[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  // Stato per modale di aggiunta certificato
  const [showModal, setShowModal] = useState<boolean>(false);
  const [saving, setSaving] = useState<boolean>(false);
  const [editingCert, setEditingCert] = useState<LwgFornitore | null>(null);

  // Stato per il form del certificato
  const [formData, setFormData] = useState<{
    lwg_urn: string;
    lwg_score: string;
    lwg_date: string;
    lwg_expiry: string;
  }>({
    lwg_urn: '',
    lwg_score: '',
    lwg_date: '',
    lwg_expiry: '',
  });

  // Funzione per caricare i certificati LWG dal server
  useEffect(() => {
    if (!fornitoreId) return;
    fetchCertificati();
  }, [fornitoreId]);

  const fetchCertificati = async () => {
    try {
      setLoading(true);
      const res = await axios.get(
        '/anagrafiche/lwgfornitori/',
        {
          params: { fk_fornitore: fornitoreId },
        }
      );

      // Debug: vediamo cosa ritorna l'API
      console.log('Risposta API lwgfornitori:', res.data);

      // Django REST Framework può restituire un oggetto con 'results' se usa la paginazione
      const data = Array.isArray(res.data) ? res.data : (res.data.results || []);
      setCertificati(data);
    } catch (error: any) {
      console.error(
        'Errore nel caricamento dei certificati LWG:',
        error.response || error
      );
      toast.error('Errore nel caricamento dei certificati LWG.');
      setCertificati([]); // Imposta array vuoto in caso di errore
    } finally {
      setLoading(false);
    }
  };

  // Funzione per gestire l'apertura della modale di aggiunta/modifica
  const handleAddClick = () => {
    setEditingCert(null);
    setFormData({
      lwg_urn: '',
      lwg_score: '',
      lwg_date: '',
      lwg_expiry: '',
    });
    setShowModal(true);
  };

  // -----------------------------------------------------
  // Apertura modal per "Modifica Certificato"
  // -----------------------------------------------------
  const handleEditClick = (cert: LwgFornitore) => {
    setEditingCert(cert);
    setFormData({
      lwg_urn: cert.lwg_urn || '',
      lwg_score: cert.lwg_score || '',
      lwg_date: cert.lwg_date || '',
      lwg_expiry: cert.lwg_expiry || '',
    });
    setShowModal(true);
  };

  // ---------------------------------------------------------------------------
  // Eliminazione certificato
  // ---------------------------------------------------------------------------
  const handleDeleteClick = async (cert: LwgFornitore) => {
    const conferma = window.confirm(
      `Sei sicuro di voler eliminare il certificato LWG con URN: ${cert.lwg_urn}?`
    );
    if (!conferma) return;
    try {
      await axios.delete(`/anagrafiche/lwgfornitori/${cert.id}/`);
      toast.success('Certificato LWG eliminato con successo.');
      // Ricarico elenco dopo eliminazione
      fetchCertificati();
    } catch (error: any) {
      console.error(
        "Errore nell'eliminazione del certificato LWG:",
        error.response || error
      );
      toast.error("Errore nell'eliminazione del certificato LWG.");
    }
  };

  // ---------------------------------------------------------------------------
  // Gestione cambi nel form del modal
  // ---------------------------------------------------------------------------
  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // ---------------------------------------------------------------------------
  // Salvataggio nuovo certificato o modifica esistente
  // ---------------------------------------------------------------------------
  const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Validazione base
    if (!formData.lwg_urn.trim()) {
      toast.error('LWG URN è obbligatorio.');
      return;
    }

    const payload = {
      lwg_urn: formData.lwg_urn.trim(),
      // score e date possono essere opzionali: se vuote le mando come null
      lwg_score: formData.lwg_score.trim() || null,
      lwg_date: formData.lwg_date || null,
      lwg_expiry: formData.lwg_expiry || null,
      fk_fornitore: fornitoreId,
    };
    try {
      setSaving(true);
      if (editingCert) {
        // Modifica esistente
        await axios.put(
          `/anagrafiche/lwgfornitori/${editingCert.id}/`,
          payload
        );
        toast.success('Certificato LWG aggiornato con successo.');
      } else {
        // Nuovo certificato
        await axios.post('/anagrafiche/lwgfornitori/', payload);
        toast.success('Certificato LWG aggiunto con successo.');
      }
      setShowModal(false);
      setEditingCert(null);
      // Ricarico elenco dopo salvataggio
      fetchCertificati();
    } catch (error: any) {
      console.error(
        'Errore nel salvataggio del certificato LWG:',
        error.response || error
      );
      toast.error(
        'Errore nel salvataggio del certificato LWG.' +
          JSON.stringify(error.response?.data ?? {})
      );
    } finally {
      setSaving(false);
    }
  };

  // ---------------------------------------------------------------------------
  // Render
  // ---------------------------------------------------------------------------
  return (
    <div className="mt-4">
      <div className="d-flex justify-content-between align-items-center mb-2">
        <h5 className="mb-0">Certificati LWG</h5>
        <Button size="sm" variant="primary" onClick={handleAddClick}>
          + Aggiungi Certificato LWG
        </Button>
      </div>
      {loading ? (
        <div className="d-flex justify-content-center my-3">
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Caricamento...</span>
          </Spinner>
        </div>
      ) : !Array.isArray(certificati) || certificati.length === 0 ? (
        <p className="text-muted">Nessun certificato LWG disponibile.</p>
      ) : (
        <Table striped bordered hover size="sm" className="align-middle">
          <thead>
            <tr>
              <th>URN</th>
              <th>Score</th>
              <th>Data Certificazione</th>
              <th>Scadenza</th>
              <th style={{ width: '120px' }}>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {certificati.map((cert) => (
              <tr key={cert.id}>
                <td>{cert.lwg_urn}</td>
                <td>{cert.lwg_score || '-'}</td>
                <td>{cert.lwg_date || '-'}</td>
                <td>{cert.lwg_expiry || '-'}</td>
                <td>
                  <div className="d-flex gap-1">
                    <Button
                      size="sm"
                      variant="outline-secondary"
                      onClick={() => handleEditClick(cert)}
                    >
                      Modifica
                    </Button>
                    <Button
                      size="sm"
                      variant="outline-danger"
                      onClick={() => handleDeleteClick(cert)}
                    >
                      Elimina
                    </Button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
      {/* Modal per Aggiungi / Modifica certificato */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Form onSubmit={handleFormSubmit}>
          <Modal.Header closeButton>
            <Modal.Title>
              {editingCert
                ? 'Modifica Certificato LWG'
                : 'Aggiungi Certificato LWG'}
            </Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Row className="mb-3">
              <Col>
                <Form.Group controlId="lwg_urn">
                  <Form.Label>LWG URN *</Form.Label>
                  <Form.Control
                    type="text"
                    name="lwg_urn"
                    value={formData.lwg_urn}
                    onChange={handleFormChange}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row className="mb-3">
              <Col md={6}>
                <Form.Group controlId="lwg_score">
                  <Form.Label>LWG Score</Form.Label>
                  <Form.Control
                    type="text"
                    name="lwg_score"
                    value={formData.lwg_score}
                    onChange={handleFormChange}
                    placeholder="es. 85.5"
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row className="mb-3">
              <Col md={6}>
                <Form.Group controlId="lwg_date">
                  <Form.Label>Data Certificazione</Form.Label>
                  <Form.Control
                    type="date"
                    name="lwg_date"
                    value={formData.lwg_date}
                    onChange={handleFormChange}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group controlId="lwg_expiry">
                  <Form.Label>Data Scadenza</Form.Label>
                  <Form.Control
                    type="date"
                    name="lwg_expiry"
                    value={formData.lwg_expiry}
                    onChange={handleFormChange}
                  />
                </Form.Group>
              </Col>
            </Row>
            {/* Se in futuro vuoi gestire anche upload documento:
                                - aggiungi un Form.Control type="file"
                                - usa FormData lato axios per inviare multipart/form-data
                            */}
          </Modal.Body>
          <Modal.Footer>
            <Button
              variant="secondary"
              onClick={() => setShowModal(false)}
              disabled={saving}
            >
              Annulla
            </Button>
            <Button type="submit" variant="primary" disabled={saving}>
              {saving ? 'Salvataggio...' : 'Salva'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </div>
  );
};
export default LwgCertificateTable;
