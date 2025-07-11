import { Pagination } from 'react-bootstrap';

interface PaginationControlsProps {
  count: number;
  page: number;
  pageSize: number;
  onPageChange: (page: number) => void;
}

const PaginationControls = ({
  count,
  page,
  pageSize,
  onPageChange,
}: PaginationControlsProps) => {
  const totalPages = Math.ceil(count / pageSize);

  if (totalPages <= 1) return null;

  const renderPageNumbers = () => {
    const pages = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(
        <Pagination.Item
          key={i}
          active={i === page}
          onClick={() => onPageChange(i)}
        >
          {i}
        </Pagination.Item>
      );
    }
    return pages;
  };

  return <Pagination>{renderPageNumbers()}</Pagination>;
};

export default PaginationControls;
