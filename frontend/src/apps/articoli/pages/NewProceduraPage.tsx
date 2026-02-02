/**
 * NewProceduraPage - Crea una nuova procedura e redirect all'edit
 *
 * Route: /articoli/:articoloId/procedure/new
 */
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Spinner, Card, Button } from 'react-bootstrap';
import { toast } from 'react-toastify';
import { createProcedura } from '../api/procedure';

export default function NewProceduraPage() {
  const { articoloId } = useParams<{ articoloId: string }>();
  const navigate = useNavigate();
  const [creating, setCreating] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const create = async () => {
      if (!articoloId) {
        setError('ID articolo mancante');
        setCreating(false);
        return;
      }

      try {
        const res = await createProcedura({ fk_articolo: Number(articoloId) });
        const newProcedura = res.data;
        toast.success(`Procedura Nr. ${newProcedura.nr_procedura} Rev. ${newProcedura.nr_revisione} creata`);
        // Redirect alla pagina di edit
        navigate(`/articoli/${articoloId}/procedure/${newProcedura.id}`, { replace: true });
      } catch (err: any) {
        const msg = err.response?.data?.detail || 'Errore nella creazione della procedura';
        setError(msg);
        toast.error(msg);
        setCreating(false);
      }
    };

    create();
  }, [articoloId, navigate]);

  if (creating) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" />
        <p className="mt-2">Creazione nuova procedura...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Card className="text-center py-5">
        <Card.Body>
          <p className="text-danger">{error}</p>
          <Button
            variant="link"
            onClick={() => navigate(`/articoli/${articoloId}`)}
          >
            ← Torna all'articolo
          </Button>
        </Card.Body>
      </Card>
    );
  }

  return null;
}
