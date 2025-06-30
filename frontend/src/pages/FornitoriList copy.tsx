import React, { useEffect, useMemo, useState } from 'react';
import { Button, Form, Modal, Table, Spinner } from 'react-bootstrap';
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
  const [loading, setLoading] = useState(true);
  const [pageIndex, setPageIndex] = useState(0);
  const pageSize = 50;

  useEffect(() => {
    const fetchFornitori = async () => {
      try {
        const response = await getFornitori();
        setFornitori(response.data);
      } catch {
        toast.error('Errore nel caricamento fornitori');
      } finally {
        setLoading(false);
      }
    };
    fetchFornitori();
  }, []);

  const handleElimina = async (id: number) => {
    if (window.confirm('Sei sicuro di voler eliminare questo fornitore?')) {
      try {
        await deleteFornitore(id);
        toast.success('Fornitore eliminato');
        setLoading(true);
        const response = await getFornitori();
        setFornitori(response.data);
      } catch {
        toast.error('Errore durante eliminazione');
      } finally {
        setLoading(false);
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
    //data: fornitori,
    data: fornitori.slice(pageIndex * pageSize, (pageIndex + 1) * pageSize),
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

  if (loading) {
    return (
      <Layout>
        <div
          className="d-flex justify-content-center align-items-center"
          style={{ height: '60vh' }}
        >
          <Spinner animation="border" role="status" variant="primary">
            <span className="visually-hidden">Caricamento...</span>
          </Spinner>
        </div>
      </Layout>
    );
  }

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
      {/* Elemento di paginazione */}

      <div className="d-flex justify-content-between align-items-center mt-3">
        <Button
          variant="outline-secondary"
          onClick={() => setPageIndex((prev) => Math.max(prev - 1, 0))}
          disabled={pageIndex === 0}
        >
          ← Precedente
        </Button>
        <span>
          Pagina {pageIndex + 1} di {Math.ceil(fornitori.length / pageSize)}
        </span>
        <Button
          variant="outline-secondary"
          onClick={() =>
            setPageIndex((prev) =>
              prev < Math.ceil(fornitori.length / pageSize) - 1
                ? prev + 1
                : prev
            )
          }
          disabled={pageIndex >= Math.ceil(fornitori.length / pageSize) - 1}
        >
          Successiva →
        </Button>
      </div>

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
