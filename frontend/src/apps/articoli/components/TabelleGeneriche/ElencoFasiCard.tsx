import { useEffect, useState } from 'react';
import { Table, Button, Form, InputGroup } from 'react-bootstrap';
import axios from '@/api/axios';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { getFasi, deleteFase } from '@articoli/api/articoli';
import FaseLavoroForm from './FaseLavoroForm';
import type { FasiLavoro } from '@articoli/types/articoli';
import ConfirmModal from '@/components/common/ConfirmModal';

export default function ElencoTestCard() {
  const navigate = useNavigate();
  const [fase, setFase] = useState<FasiLavoro[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [selectedFase, setSelectedFase] = useState<FasiLavoro | null>(null);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await getFasi();
      setFase(res.data.results);
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
    await deleteFase(id);
    fetchData();
    setDeleteId(null);
  };

  const filtered = fase.filter((f) =>
    f.descrizione.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <>
      <InputGroup className="mb-2">
        <Form.Control
          placeholder="Cerca fase..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </InputGroup>
      <div className="text-end mt-2">
        <Button
          size="sm"
          onClick={() => navigate('/articoli/tabelle/fasi-lavoro/new')}
        >
          ➕ Aggiungi Fase
        </Button>
      </div>
      <Table size="sm" striped hover responsive>
        <thead>
          <tr>
            <th>Descrizione</th>
            <th>I/E</th>
            <th>UM</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((f) => (
            <tr
              key={f.id}
              onClick={() => navigate(`/articoli/tabelle/fasi-lavoro/${f.id}/`)}
              //onClick={() => toast.info('Modifica in sviluppo')}
              style={{ cursor: 'pointer' }}
            >
              <td>{f.descrizione}</td>
              <td>{f.interno_esterno}</td>
              <td>{f.um}</td>
              <td className="text-end">
                <Button
                  size="sm"
                  variant="outline-danger"
                  //onClick={() => handleDelete(t.id)}
                  onClick={(e) => {
                    e.stopPropagation();
                    setDeleteId(f.id);
                  }}
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
      <ConfirmModal
        show={!!deleteId}
        onHide={() => setDeleteId(null)}
        onConfirm={() => deleteId && handleDelete(deleteId)}
        message="Sei sicuro di voler eliminare questa fase?"
      />
    </>
  );
}
