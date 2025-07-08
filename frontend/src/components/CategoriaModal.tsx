import { Modal, Button, ListGroup } from 'react-bootstrap';

interface Props {
  show: boolean;
  onHide: () => void;
  onSelect: (categoria: string) => void;
}

const categorieDisponibili = [
  'pelli',
  'macello',
  'prodotti chimici',
  'lavorazioni esterne',
  'servizi',
  'manutenzioni',
  'rifiuti',
  'nessuna',
];

export default function CategoriaModal({ show, onHide, onSelect }: Props) {
  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>Seleziona categoria</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <ListGroup>
          {categorieDisponibili.map((cat) => (
            <ListGroup.Item key={cat} action onClick={() => onSelect(cat)}>
              {cat}
            </ListGroup.Item>
          ))}
        </ListGroup>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Annulla
        </Button>
      </Modal.Footer>
    </Modal>
  );
}
