import { useEffect, useState } from 'react';
import { Table, Button, Form, InputGroup } from 'react-bootstrap';
import axios from '@/api/axios';
import { toast } from 'react-toastify';
import type { ElencoTest } from '@articoli/types/articoli';

export default function ElencoTestCard() {
  const [test, setTest] = useState<ElencoTest[]>([]);
  const [search, setSearch] = useState('');

  const fetchData = () => {
    axios.get('/articoli/elenco-test/').then((res) => {
      console.log(res.data);
      setTest(res.data.results);
    });
  };

  useEffect(fetchData, []);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Confermi eliminazione?')) return;
    try {
      await axios.delete(`/articoli/elenco-test/${id}/`);
      toast.success('Eliminato con successo');
      fetchData();
    } catch {
      toast.error("Errore durante l'eliminazione");
    }
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
            <tr key={t.id}>
              <td>{t.descrizione}</td>
              <td>{t.norma_riferimento}</td>
              <td className="text-end">
                <Button
                  size="sm"
                  variant="outline-secondary"
                  onClick={() => toast.info('Modifica in sviluppo')}
                >
                  ✏️
                </Button>{' '}
                <Button
                  size="sm"
                  variant="outline-danger"
                  onClick={() => handleDelete(t.id)}
                >
                  🗑
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
      <div className="text-end mt-2">
        <Button
          size="sm"
          onClick={() => toast.info('Form inserimento in sviluppo')}
        >
          ➕ Aggiungi Test
        </Button>
      </div>
    </>
  );
}
