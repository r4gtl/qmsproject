import { useEffect, useState } from 'react';
import { Table, Button, Form, Row, Col, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { getArticoli, deleteArticolo } from '@articoli/api/articoli';
import type { Articolo } from '@articoli/types/articoli';
import type { TipoAnimale, TipoGrezzo } from '@/types/lookup';
import ConfirmModal from '@/components/common/ConfirmModal';
import PaginationControls from '@/components/common/PaginationControls';

const ArticoliList = () => {
  const navigate = useNavigate();
  const [articoli, setArticoli] = useState<Articolo[]>([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(0);
  const [pageSize] = useState(50);

  const [filterDescrizione, setFilterDescrizione] = useState('');
  const [filterTipoAnimale, setFilterTipoAnimale] = useState('');
  const [filterTipoGrezzo, setFilterTipoGrezzo] = useState('');
  const [tipoAnimali, setTipoAnimali] = useState<TipoAnimale[]>([]);
  const [tipoGrezzi, setTipoGrezzi] = useState<TipoGrezzo[]>([]);

  const [deleteId, setDeleteId] = useState<number | null>(null);

  const fetchArticoli = async () => {
    setLoading(true);
    try {
      const params = {
        page,
        search: filterDescrizione,
        fk_tipoanimale: filterTipoAnimale || undefined,
        fk_tipogrezzo: filterTipoGrezzo || undefined,
      };
      const res = await getArticoli(params);
      setArticoli(res.data.results);
      setCount(res.data.count);
    } finally {
      setLoading(false);
    }
  };

  const loadLookups = async () => {
    const [animali, grezzi] = await Promise.all([
      getTipoAnimali(),
      getTipoGrezzi(),
    ]);
    setTipoAnimali(animali.data);
    setTipoGrezzi(grezzi.data);
  };
  useEffect(() => {
    fetchArticoli();
  }, [page, filterDescrizione, filterTipoAnimale, filterTipoGrezzo]);
  useEffect(() => {
    loadLookups();
  }, []);
  const handleDelete = async (id: number) => {
    await deleteArticolo(id);
    fetchArticoli();
    setDeleteId(null);
  };
  return (
    <>
      <h2>Articoli</h2>
      <Row className="mb-3">
        <Col md={3}>
          <Form.Control
            placeholder="Cerca descrizione..."
            value={filterDescrizione}
            onChange={(e) => setFilterDescrizione(e.target.value)}
          />
        </Col>

        <Col md={3}>
          <Form.Select
            value={filterTipoAnimale}
            onChange={(e) => setFilterTipoAnimale(e.target.value)}
          >
            <option value="">Tutti i tipi animale</option>
            {tipoAnimali.map((t) => (
              <option key={t.id} value={t.id}>
                {t.descrizione}
              </option>
            ))}
          </Form.Select>
        </Col>
        <Col md={3}>
          <Form.Select
            value={filterTipoGrezzo}
            onChange={(e) => setFilterTipoGrezzo(e.target.value)}
          >
            <option value="">Tutti i tipi di grezzo</option>
            {tipoGrezzi.map((g) => (
              <option key={g.id} value={g.id}>
                {g.descrizione}
              </option>
            ))}
          </Form.Select>
        </Col>
        <Col md={3} className="text-end">
          <Button variant="primary" onClick={() => navigate('new')}>
            + Nuovo Articolo
          </Button>
        </Col>
      </Row>
      {loading ? (
        <Spinner animation="border" />
      ) : (
        <Table striped hover responsive>
          <thead>
            <tr>
              <th>Descrizione</th>
              <th>Tipo animale</th>
              <th>Tipo grezzo</th>
              <th>Industria servita</th>
              <th>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {articoli.map((articolo) => (
              <tr
                key={articolo.id}
                onClick={() => navigate(`${articolo.id}`)}
                style={{ cursor: 'pointer' }}
              >
                <td>{articolo.descrizione}</td>
                <td>{articolo.fk_tipoanimale_descrizione || '-'}</td>
                <td>{articolo.fk_tipogrezzo_descrizione || '-'}</td>
                <td>{articolo.industries_served || '-'}</td>
                <td>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      setDeleteId(articolo.id);
                    }}
                  >
                    Elimina
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      <PaginationControls
        count={count}
        page={page}
        pagesize={pageSize}
        onPageChange={setPage}
      />

      <ConfirmModal
        show={!!deleteId}
        onHide={() => setDeleteId(null)}
        onConfirm={() => deleteId && handleDelete(deleteId)}
        message="Sei sicuro di voler eliminare quest articolo?"
      />
    </>
  );
};

export default ArticoliList;
