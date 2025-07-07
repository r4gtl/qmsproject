import React, { useEffect, useState } from 'react';
import { Button, Form, Modal, Table, Spinner } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  getPaginationRowModel,
  flexRender,
} from '@tanstack/react-table';
import type { ColumnDef, ColumnFiltersState } from '@tanstack/react-table';
import { getFornitori, deleteFornitore } from '@/api/anagrafiche';
import { toast } from 'react-toastify';
import Layout from '@/components/Layout/Layout';
import { FaSort, FaSortUp, FaSortDown } from 'react-icons/fa';

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
  const navigate = useNavigate();
  const [fornitori, setFornitori] = useState<Fornitore[]>([]);
  const [loading, setLoading] = useState(true);
  const [globalFilter, setGlobalFilter] = useState('');
  //const [columnFilters, setColumnFilters] = useState<any[]>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);

  const [sort, setSort] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [categoriaSelezionata, setCategoriaSelezionata] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getFornitori();
        setFornitori(res.data);
      } catch {
        toast.error('Errore nel caricamento fornitori');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const columns: ColumnDef<Fornitore>[] = [
    {
      accessorKey: 'ragionesociale',
      header: 'Ragione Sociale',
      cell: (info) => info.getValue(),
      enableColumnFilter: true,
    },
    {
      accessorKey: 'country',
      header: 'Paese',
      cell: (info) => info.getValue(),
      enableColumnFilter: true,
    },
    {
      accessorKey: 'categoria',
      header: 'Categoria',
      cell: (info) => info.getValue(),
      enableColumnFilter: true,
    },
    {
      id: 'azioni',
      header: 'Azioni',
      enableColumnFilter: false,
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
  ];

  const table = useReactTable({
    data: fornitori,
    columns,
    state: {
      globalFilter,
      columnFilters,
      sorting: sort,
    },
    onSortingChange: setSort,
    onGlobalFilterChange: setGlobalFilter,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: {
      pagination: {
        pageSize: 50,
        pageIndex: 0,
      },
    },
  });

  const handleElimina = async (id: number) => {
    if (!window.confirm('Sicuro di voler eliminare?')) return;
    try {
      await deleteFornitore(id);
      toast.success('Eliminato');
      setLoading(true);
      const res = await getFornitori();
      setFornitori(res.data);
    } catch {
      toast.error('Errore durante eliminazione');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Fornitori</h2>
        <Button onClick={() => setShowModal(true)}>Aggiungi</Button>
      </div>
      <div className="d-flex justify-content-between align-items-center mb-2">
        <Form.Label className="fw-bold mb-0">Ricerca globale</Form.Label>
        <Button
          variant="outline-secondary"
          size="sm"
          onClick={() => {
            setGlobalFilter('');
            setColumnFilters([]);
            setPageIndex(0);
          }}
        >
          Reset filtri
        </Button>
      </div>
      <Form.Control
        type="text"
        placeholder="Filtra..."
        value={globalFilter}
        onChange={(e) => setGlobalFilter(e.target.value)}
        className="mb-3"
      />

      {loading ? (
        <div className="text-center my-5">
          <Spinner animation="border" />
        </div>
      ) : (
        <>
          <Table striped bordered hover responsive>
            <thead>
              {table.getHeaderGroups().map((headerGroup) => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <th key={header.id}>
                      <div
                        onClick={
                          header.column.getCanSort()
                            ? header.column.getToggleSortingHandler()
                            : undefined
                        }
                        style={{
                          cursor: header.column.getCanSort()
                            ? 'pointer'
                            : 'default',
                        }}
                      >
                        {flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}{' '}
                        {header.column.getCanSort() && (
                          <>
                            {!header.column.getIsSorted() && (
                              <FaSort className="ms-1" />
                            )}
                            {header.column.getIsSorted() === 'asc' && (
                              <FaSortUp className="ms-1" />
                            )}
                            {header.column.getIsSorted() === 'desc' && (
                              <FaSortDown className="ms-1" />
                            )}
                          </>
                        )}
                      </div>
                      {header.column.getCanFilter() && (
                        <div className="mt-1">
                          <input
                            type="text"
                            placeholder="Filtro"
                            value={
                              (header.column.getFilterValue() as string) ?? ''
                            }
                            onChange={(e) =>
                              header.column.setFilterValue(e.target.value)
                            }
                            className="form-control form-control-sm"
                          />
                        </div>
                      )}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody>
              {table.getRowModel().rows.map((row) => (
                <tr key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </Table>

          <div className="d-flex justify-content-between align-items-center mt-3">
            <Button
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
            >
              &lt; Precedente
            </Button>
            <span>
              Pagina {table.getState().pagination.pageIndex + 1} di{' '}
              {table.getPageCount()}
            </span>
            <Button
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
            >
              Successiva &gt;
            </Button>
          </div>
        </>
      )}

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
            disabled={!categoriaSelezionata}
            onClick={() => {
              navigate(`/fornitori/nuovo/${categoriaSelezionata}`);
              setShowModal(false);
            }}
          >
            Avanti
          </Button>
        </Modal.Footer>
      </Modal>
    </Layout>
  );
}
