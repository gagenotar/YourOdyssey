import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import TripItineraryView from './TripItineraryView';

interface Props {
  show: boolean;
  item: any | null;
  onClose: () => void;
}

export default function TripDetailModal({ show, item, onClose }: Props) {
  if (!item) return null;
  const itinerary = item.itinerary || {};

  return (
    <Modal show={show} onHide={onClose} size="xl" fullscreen={'lg-down' as any} centered>
      <Modal.Header closeButton>
        <div>
          <Modal.Title>{itinerary.destination || itinerary.destination_info?.name || 'Trip details'}</Modal.Title>
          <div style={{ fontSize: '0.85rem', color: '#6b7280' }}>
            Saved: {new Date(item.created_at).toLocaleString()} • {itinerary.duration ?? '?'} days
          </div>
        </div>
      </Modal.Header>

    <Modal.Body style={{ maxHeight: '85vh', overflowY: 'auto' }}>
        <TripItineraryView itinerary={itinerary} />
      </Modal.Body>

      <Modal.Footer>
        <button
          type="button"
          className="btn btn-primary"
          onClick={onClose}
          aria-label="Close trip details"
        >
          Close
        </button>
      </Modal.Footer>
    </Modal>
  );
}
