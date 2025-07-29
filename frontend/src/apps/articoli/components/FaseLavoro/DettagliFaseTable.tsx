import { useState } from 'react';
import { Table, Button, Form } from 'react-bootstrap';
import { FaTrash, FaPlus, FaSave } from 'react-icons/fa';
import { toast } from 'react-toastify';
import type { DettaglioFaseLavoro } from '@articoli/types/articoli';
import type { DettagliFaseTableProps } from '@articoli/types/articoli';

const DettagliFaseTable = ({
  faseId,
  dettagli,
  onChange,
}: DettagliFaseTableProps) => {
  const [localDettagli, setLocalDettagli] = useState([...dettagli]);

  const handleChange = (
    index: number,
    field: keyof DettaglioFaseLavoro,
    value: string
  ) => {
    const updated = [...localDettagli];
    updated[index] = { ...updated[index], [field]: value };
    setLocalDettagli(updated);
  };

  const handleAdd = () => {
    setLocalDettagli([...localDettagli, { attributo: '', note: '' }]);
  };

  const handleDelete = (index: number) => {
    const updated = [...localDettagli];
    updated.splice(index, 1);
    setLocalDettagli(updated);
    onChange(updated);
  };

  return (
    <>
      <h5 className="mt-4">Attributi assegnati</h5>
      <Table bordered hover responsive size="sm">
        <thead className="table-light">
          <tr>
            <th>Attributo</th>
            <th>Note</th>
            <th style={{ width: 40 }}></th>
          </tr>
        </thead>
        <tbody>
          {localDettagli.map((det, idx) => (
            <tr key={idx}>
              <td>
                <Form.Control
                  value={det.attributo}
                  onChange={(e) =>
                    handleChange(idx, 'attributo', e.target.value)
                  }
                  required
                />
              </td>
              <td>
                <Form.Control
                  value={det.note || ''}
                  onChange={(e) => handleChange(idx, 'note', e.target.value)}
                />
              </td>
              <td className="text-center">
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => handleDelete(idx)}
                >
                  <FaTrash />
                </Button>
              </td>
            </tr>
          ))}
          {localDettagli.length === 0 && (
            <tr>
              <td colSpan={3} className="text-center text-muted">
                Nessun attributo presente
              </td>
            </tr>
          )}
        </tbody>
      </Table>
      <div className="text-end">
        <Button size="sm" onClick={handleAdd}>
          <FaPlus className="me-1" /> Aggiungi attributo
        </Button>
      </div>
    </>
  );
};

export default DettagliFaseTable;
