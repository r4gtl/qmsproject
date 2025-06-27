import React, { useEffect, useMemo, useState } from 'react';
import { Button, Form, Modal, Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  flexRender,
} from '@tanstack/react-table';
import type { ColumnDef } from '@tanstack/react-table';
import { getFornitori, deleteFornitore } from '@/api/anagrafiche';
import { toast } from 'react-toastify';

import Layout from '@/components/Layout/Layout';

interface Fornitore {
  id: number;
  ragionesociale: string;
  country: string;
  categoria: string;
}

const categorie = [
  'nessuna',
  'pelli',
  'macello',
  'prodotti chimici',
  'lavorazioni esterne',
  'servizi',
  'manutenzioni',
  'rifiuti',
];

export default function FornitoriList() {
  const [fornitori, setFornitori] = useState<Fornitore[]>([]);
  const [globalFilter, setGlobalFilter] = useState('');
  const [sort, setSort] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [categoriaSelezionata, setCategoriaSelezionata] = useState('');
  const navigate = useNavigate();

  const fetchFornitori = async () => {
    try {
      const response = await getFornitori();
      setFornitori(response.data);
    } catch (error) {
      toast.error('Errore nel caricamento fornitori');
    }
  };

  useEffect(() => {
    fetchFornitori();
  }, []);

  const handleElimina = async (id: number) => {
    if (window.confirm('Sei sicuro di voler eliminare questo fornitore?')) {
      try {
        await deleteFornitore(id);
        toast.success('Fornitore eliminato');
        fetchFornitori();
      } catch (error) {
        toast.error('Errore durante eliminazione');
      }
    }
  };

  const columns = useMemo<ColumnDef<Fornitore>[]>(
    () => [
      {
        header: 'Ragione Sociale',
        accessorKey: 'ragionesociale',
        cell: (info) => info.getValue(),
      },
      {
        header: 'Paese',
        accessorKey: 'country',
        cell: (info) => info.getValue(),
      },
      {
        header: 'Categoria',
        accessorKey: 'categoria',
        cell: (info) => info.getValue(),
      },
      {
        header: 'Azioni',
        id: 'actions',
        cell: ({ row }) => (
          <div className="d-flex gap-2">
            <Button
              size="sm"
              variant="outline-primary"
              onClick={() => navigate(`/fornitori/${row.original.id}/modifica`)}
            >
              Modifica
            </Button>
            <Button
              size="sm"
              variant="outline-danger"
              onClick={() => handleElimina(row.original.id)}
            >
              Elimina
            </Button>
          </div>
        ),
      },
    ],
    [navigate]
  );

  const table = useReactTable({
    data: fornitori,
    columns,
    state: {
      globalFilter,
      sorting: sort,
    },
    onSortingChange: setSort,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <Layout>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Fornitori</h2>
        <Button onClick={() => setShowModal(true)}>Aggiungi</Button>
      </div>
      <Form.Control
        type="text"
        placeholder="Filtra..."
        value={globalFilter}
        onChange={(e) => setGlobalFilter(e.target.value)}
        className="mb-3"
      />
      <Table striped bordered hover responsive>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                  style={{ cursor: 'pointer' }}
                >
                  {flexRender(
                    header.column.columnDef.header,
                    header.getContext()
                  )}
                  {header.column.getIsSorted() === 'asc' ? ' 🔼' : ''}
                  {header.column.getIsSorted() === 'desc' ? ' 🔽' : ''}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr
              key={row.id}
              onClick={() => navigate(`/fornitori/${row.original.id}/modifica`)}
              style={{ cursor: 'pointer' }}
            >
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} onClick={(e) => e.stopPropagation()}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Modal selezione categoria */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Seleziona Categoria</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Select
            value={categoriaSelezionata}
            onChange={(e) => setCategoriaSelezionata(e.target.value)}
          >
            <option value="">-- Seleziona Categoria --</option>
            {categorie.map((cat) => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
          </Form.Select>
        </Modal.Body>
        <Modal.Footer>
          <Button
            onClick={() => {
              if (categoriaSelezionata) {
                navigate(`/fornitori/nuovo/${categoriaSelezionata}`);
                setShowModal(false);
              }
            }}
            disabled={!categoriaSelezionata}
          >
            Avanti
          </Button>
        </Modal.Footer>
      </Modal>
    </Layout>
  );
}
