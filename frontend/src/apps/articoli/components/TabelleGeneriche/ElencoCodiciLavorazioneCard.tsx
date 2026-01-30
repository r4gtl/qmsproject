import { useEffect, useState } from 'react';
import { Table, Button, Form, InputGroup } from 'react-bootstrap';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import {
  getLavorazioniEsterne,
  deleteLavorazioneEsterna,
} from '@articoli/api/articoli';
import type { LavorazioneEsterna } from '@articoli/types/articoli';
import ConfirmModal from '@/components/common/ConfirmModal';

export default function ElencoCodiciLavorazioneCard() {
  const navigate = useNavigate();
  const [lavorazioni, setLavorazioni] = useState<LavorazioneEsterna[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await getLavorazioniEsterne();
      setLavorazioni(res.data.results);
    } catch (error) {
      toast.error('Errore durante il caricamento');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const load = async () => {
      await fetchData();
    };
    load();
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await deleteLavorazioneEsterna(id);
      toast.success('Lavorazione eliminata');
      fetchData();
      setDeleteId(null);
    } catch (error) {
      toast.error('Errore durante l\'eliminazione');
      console.error(error);
    }
  };

  const filtered = lavorazioni.filter(
    (lav) =>
      lav.descrizione.toLowerCase().includes(search.toLowerCase()) ||
      lav.codice.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <>
      <InputGroup className="mb-2">
        <Form.Control
          placeholder="Cerca lavorazione..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </InputGroup>
      <div className="text-end mt-2">
        <Button
          size="sm"
          onClick={() => navigate('/articoli/tabelle/codici-lavorazione/new')}
        >
          ➕ Aggiungi Lavorazione
        </Button>
      </div>
      {filtered.length === 0 && !loading ? (
        <div className="text-center text-muted mt-4">
          <p>Nessuna lavorazione trovata</p>
        </div>
      ) : (
        <Table size="sm" striped hover responsive>
          <thead>
            <tr>
              <th>Codice</th>
              <th>Descrizione</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((lav) => (
              <tr
                key={lav.id}
                onClick={() =>
                  navigate(`/articoli/tabelle/codici-lavorazione/${lav.id}/`)
                }
                style={{ cursor: 'pointer' }}
              >
                <td>{lav.codice}</td>
                <td>{lav.descrizione}</td>
                <td className="text-end">
                  <Button
                    size="sm"
                    variant="outline-danger"
                    onClick={(e) => {
                      e.stopPropagation();
                      setDeleteId(lav.id);
                    }}
                  >
                    🗑
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
      <ConfirmModal
        show={!!deleteId}
        onHide={() => setDeleteId(null)}
        onConfirm={() => deleteId && handleDelete(deleteId)}
        message="Sei sicuro di voler eliminare questa lavorazione?"
      />
    </>
  );
}
