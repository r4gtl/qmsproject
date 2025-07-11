import { Modal, Button } from 'react-bootstrap';

interface ConfirmModalProps {
  show: boolean;
  onHide: () => void;
  onConfirm: () => void;
  message: string;
}

const ConfirmModal = ({
  show,
  onHide,
  onConfirm,
  message,
}: ConfirmModalProps) => {
  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>Conferma</Modal.Title>
      </Modal.Header>
      <Modal.Body>{message}</Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Annulla
        </Button>
        <Button variant="danger" onClick={onConfirm}>
          Elimina
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ConfirmModal;
