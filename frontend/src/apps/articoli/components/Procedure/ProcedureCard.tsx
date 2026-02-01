/**
 * ProcedureCard - Card per visualizzare le procedure di un articolo
 *
 * Da usare in ArticoloForm per mostrare la lista delle revisioni.
 */
import { useEffect, useState } from 'react';
import { Card, Table, Button, Spinner, Badge } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { getProcedureByArticolo, createProcedura } from '../../api/procedure';
import type { Procedura } from '../../types/procedure';

interface ProcedureCardProps {
  articoloId: number;
}

export default function ProcedureCard({ articoloId }: ProcedureCardProps) {
  const navigate = useNavigate();
  const [procedure, setProcedure] = useState<Procedura[]>([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);

  // Carica le procedure dell'articolo
  const fetchProcedure = async () => {
    try {
      setLoading(true);
      const res = await getProcedureByArticolo(articoloId);
      setProcedure(res.data.results);
    } catch {
      toast.error('Errore nel caricamento procedure');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (articoloId) {
      fetchProcedure();
    }
  }, [articoloId]);

  // Crea nuova revisione
  const handleNuovaRevisione = async () => {
    try {
      setCreating(true);
      const res = await createProcedura({ fk_articolo: articoloId });
      toast.success(
        `Creata Procedura ${res.data.nr_procedura} Rev. ${res.data.nr_revisione}`
      );
      // Naviga alla pagina della nuova procedura
      navigate(`/articoli/${articoloId}/procedure/${res.data.id}`);
    } catch {
      toast.error('Errore nella creazione della procedura');
    } finally {
      setCreating(false);
    }
  };

  // Naviga alla procedura
  const handleRowClick = (proceduraId: number) => {
    navigate(`/articoli/${articoloId}/procedure/${proceduraId}`);
  };

  // Formatta la data
  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('it-IT');
  };

  return (
    <Card className="mt-4">
      <Card.Header className="d-flex justify-content-between align-items-center">
        <span>
          <strong>Procedure</strong>
          {procedure.length > 0 && (
            <Badge bg="secondary" className="ms-2">
              {procedure.length}
            </Badge>
          )}
        </span>
        <Button
          variant="primary"
          size="sm"
          onClick={handleNuovaRevisione}
          disabled={creating}
        >
          {creating ? (
            <Spinner animation="border" size="sm" />
          ) : (
            '+ Nuova Revisione'
          )}
        </Button>
      </Card.Header>
      <Card.Body>
        {loading ? (
          <div className="text-center py-4">
            <Spinner animation="border" />
          </div>
        ) : procedure.length === 0 ? (
          <p className="text-muted mb-0">
            Nessuna procedura per questo articolo.
          </p>
        ) : (
          <Table hover responsive size="sm" className="mb-0">
            <thead>
              <tr>
                <th>Nr. Proc.</th>
                <th>Data Proc.</th>
                <th>Rev.</th>
                <th>Data Rev.</th>
                <th>Righe</th>
                <th>Note</th>
              </tr>
            </thead>
            <tbody>
              {procedure.map((p) => (
                <tr
                  key={p.id}
                  onClick={() => handleRowClick(p.id)}
                  style={{ cursor: 'pointer' }}
                  className="align-middle"
                >
                  <td>
                    <strong>{p.nr_procedura}</strong>
                  </td>
                  <td>{formatDate(p.data_procedura)}</td>
                  <td>
                    <Badge bg="info">{p.nr_revisione}</Badge>
                  </td>
                  <td>{formatDate(p.data_revisione)}</td>
                  <td>
                    <Badge bg="secondary">{p.dettagli_count || 0}</Badge>
                  </td>
                  <td className="text-truncate" style={{ maxWidth: '200px' }}>
                    {p.note || '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        )}
      </Card.Body>
    </Card>
  );
}
