import React, { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";

const BlocklistForm = ({ show, handleClose, handleSubmit }) => {
  const [entry, setEntry] = useState('');
  const [file, setFile] = useState(null);
  const [notes, setNotes] = useState('');


  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setEntry(''); // Clear entry if file is selected
  };

  const handleEntryChange = (e) => {
    setEntry(e.target.value);
    setFile(null); // Clear file if entry is typed
  };

  const onSubmit = (e) => {
    e.preventDefault();
    handleSubmit({ entry, file, notes, deleteDate: deleteDate || null, autoDelete });
    setEntry('');
    setFile(null);
    setNotes('');
    handleClose();
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Add to Blocklist</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={onSubmit}>
          <Form.Group controlId="formEntry">
            <Form.Label>Entry</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter IP or Domain"
              value={entry}
              onChange={handleEntryChange}
              disabled={file !== null}
            />
          </Form.Group>
          <Form.Group controlId="formFile">
            <Form.Label>Upload File</Form.Label>
            <Form.Control
              type="file"
              onChange={handleFileChange}
              disabled={entry !== ''}
            />
          </Form.Group>
          <Form.Group controlId="formNotes">
            <Form.Label>Notes</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              required
            />
          </Form.Group>
          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </Modal.Body>
    </Modal>
  );
};

export default BlocklistForm;