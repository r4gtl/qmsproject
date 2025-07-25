import { useEffect, useState } from 'react';
import { Table, Button, Form, InputGroup } from 'react-bootstrap';
import axios from '@/api/axios';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';
import { getTests, deleteTest } from '@articoli/api/articoli';
import ElencoTestForm from './ElencoTestForm';
import type { ElencoTest } from '@articoli/types/articoli';
import ConfirmModal from '@/components/common/ConfirmModal';

export default function ElencoTestCard() {
  const navigate = useNavigate();
  const [test, setTest] = useState<ElencoTest[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [selectedTest, setSelectedTest] = useState<ElencoTest | null>(null);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const res = await getTests();
      setTest(res.data.results);
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
    await deleteTest(id);
    fetchData();
    setDeleteId(null);
  };

  const filtered = test.filter((t) =>
    t.descrizione.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <>
      <InputGroup className="mb-2">
        <Form.Control
          placeholder="Cerca test..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </InputGroup>
      <div className="text-end mt-2">
        <Button
          size="sm"
          onClick={() => navigate('/articoli/tabelle/elenco-test/new')}
        >
          ➕ Aggiungi Test
        </Button>
      </div>
      <Table size="sm" striped hover responsive>
        <thead>
          <tr>
            <th>Descrizione</th>
            <th>Norma</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((t) => (
            <tr
              key={t.id}
              //onClick={() => navigate(`${t.id}`)}
              onClick={() => toast.info('Modifica in sviluppo')}
              style={{ cursor: 'pointer' }}
            >
              <td>{t.descrizione}</td>
              <td>{t.norma_riferimento}</td>
              <td className="text-end">
                <Button
                  size="sm"
                  variant="outline-danger"
                  //onClick={() => handleDelete(t.id)}
                  onClick={(e) => {
                    e.stopPropagation();
                    setDeleteId(t.id);
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
        message="Sei sicuro di voler eliminare questo test?"
      />
    </>
  );
}
