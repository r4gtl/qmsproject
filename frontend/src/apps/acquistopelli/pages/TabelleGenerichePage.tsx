import { Container, Row, Col, Card } from 'react-bootstrap';
import { FaPaw, FaScroll, FaStar, FaGlobe, FaMapMarkerAlt, FaFlag } from 'react-icons/fa';
import GenericTableCard from '../components/TabelleGeneriche/GenericTableCard';
import type { TipoAnimale, TipoGrezzo, Scelta, LwgRegione, LwgSubregione, Nazione } from '../types';
import {
  getTipiAnimale, createTipoAnimale, updateTipoAnimale, deleteTipoAnimale,
  getTipiGrezzo, createTipoGrezzo, updateTipoGrezzo, deleteTipoGrezzo,
  getScelte, createScelta, updateScelta, deleteScelta,
  getRegioni, createRegione, updateRegione, deleteRegione,
  getSubregioni, createSubregione, updateSubregione, deleteSubregione,
  getNazioni, createNazione, updateNazione, deleteNazione,
} from '../api/acquistopelliApi';

const CARD_STYLE = { height: '500px' };
const BODY_STYLE = { overflowY: 'auto' as const, maxHeight: '420px' };

export default function TabelleGenerichePelliPage() {
  return (
    <Container className="my-4">
      <h3 className="mb-4">Tabelle Generiche - Acquisti Pelli</h3>
      <Row className="g-4">
        {/* Tipi Animale */}
        <Col md={6}>
          <Card style={CARD_STYLE} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaPaw className="me-2" /> Tipi Animale
            </Card.Header>
            <Card.Body style={BODY_STYLE}>
              <GenericTableCard<TipoAnimale>
                columns={[{ header: 'Descrizione', accessor: 'descrizione' }]}
                fetchFn={getTipiAnimale}
                createFn={createTipoAnimale}
                updateFn={updateTipoAnimale}
                deleteFn={deleteTipoAnimale}
                formFields={[{ name: 'descrizione', label: 'Descrizione', required: true }]}
                searchPlaceholder="Cerca tipo animale..."
                searchKey="descrizione"
                entityName="tipo animale"
              />
            </Card.Body>
          </Card>
        </Col>

        {/* Tipi Grezzo */}
        <Col md={6}>
          <Card style={CARD_STYLE} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaScroll className="me-2" /> Tipi Grezzo
            </Card.Header>
            <Card.Body style={BODY_STYLE}>
              <GenericTableCard<TipoGrezzo>
                columns={[{ header: 'Descrizione', accessor: 'descrizione' }]}
                fetchFn={getTipiGrezzo}
                createFn={createTipoGrezzo}
                updateFn={updateTipoGrezzo}
                deleteFn={deleteTipoGrezzo}
                formFields={[{ name: 'descrizione', label: 'Descrizione', required: true }]}
                searchPlaceholder="Cerca tipo grezzo..."
                searchKey="descrizione"
                entityName="tipo grezzo"
              />
            </Card.Body>
          </Card>
        </Col>

        {/* Scelte */}
        <Col md={6}>
          <Card style={CARD_STYLE} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaStar className="me-2" /> Scelte
            </Card.Header>
            <Card.Body style={BODY_STYLE}>
              <GenericTableCard<Scelta>
                columns={[{ header: 'Descrizione', accessor: 'descrizione' }]}
                fetchFn={getScelte}
                createFn={createScelta}
                updateFn={updateScelta}
                deleteFn={deleteScelta}
                formFields={[{ name: 'descrizione', label: 'Descrizione', required: true }]}
                searchPlaceholder="Cerca scelta..."
                searchKey="descrizione"
                entityName="scelta"
              />
            </Card.Body>
          </Card>
        </Col>

        {/* Regioni LWG */}
        <Col md={6}>
          <Card style={CARD_STYLE} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaGlobe className="me-2" /> Regioni LWG
            </Card.Header>
            <Card.Body style={BODY_STYLE}>
              <GenericTableCard<LwgRegione>
                columns={[
                  { header: 'Nome Regione', accessor: 'nome_regione' },
                  { header: 'Codice M49', accessor: 'codice_m49' },
                ]}
                fetchFn={getRegioni}
                createFn={createRegione}
                updateFn={updateRegione}
                deleteFn={deleteRegione}
                formFields={[
                  { name: 'nome_regione', label: 'Nome Regione', required: true },
                  { name: 'codice_m49', label: 'Codice M49' },
                ]}
                searchPlaceholder="Cerca regione..."
                searchKey="nome_regione"
                entityName="regione"
              />
            </Card.Body>
          </Card>
        </Col>

        {/* Subregioni LWG */}
        <Col md={6}>
          <Card style={CARD_STYLE} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaMapMarkerAlt className="me-2" /> Subregioni LWG
            </Card.Header>
            <Card.Body style={BODY_STYLE}>
              <GenericTableCard<LwgSubregione>
                columns={[
                  { header: 'Nome Subregione', accessor: 'nome_subregione' },
                  { header: 'Regione', accessor: 'regione_nome' },
                ]}
                fetchFn={getSubregioni}
                createFn={createSubregione}
                updateFn={updateSubregione}
                deleteFn={deleteSubregione}
                formFields={[
                  { name: 'nome_subregione', label: 'Nome Subregione', required: true },
                  { name: 'regione', label: 'ID Regione', required: true },
                ]}
                searchPlaceholder="Cerca subregione..."
                searchKey="nome_subregione"
                entityName="subregione"
              />
            </Card.Body>
          </Card>
        </Col>

        {/* Nazioni */}
        <Col md={6}>
          <Card style={CARD_STYLE} className="shadow-sm">
            <Card.Header className="d-flex align-items-center">
              <FaFlag className="me-2" /> Nazioni
            </Card.Header>
            <Card.Body style={BODY_STYLE}>
              <GenericTableCard<Nazione>
                columns={[
                  { header: 'Descrizione', accessor: 'descrizione' },
                  { header: 'ISO2', accessor: 'sigla' },
                  { header: 'ISO3', accessor: 'sigla_estesa' },
                ]}
                fetchFn={getNazioni}
                createFn={createNazione}
                updateFn={updateNazione}
                deleteFn={deleteNazione}
                formFields={[
                  { name: 'descrizione', label: 'Nome Nazione', required: true },
                  { name: 'sigla', label: 'Sigla ISO2' },
                  { name: 'sigla_estesa', label: 'Sigla ISO3' },
                ]}
                searchPlaceholder="Cerca nazione..."
                searchKey="descrizione"
                entityName="nazione"
              />
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}
