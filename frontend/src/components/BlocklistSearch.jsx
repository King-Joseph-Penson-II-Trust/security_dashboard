import React, { useState, useEffect } from "react";
import api from "../api";
import { Card, Button, Collapse } from "react-bootstrap";
import BlocklistForm from "./BlocklistForm";
import "../styles/BlocklistSearch.css";

const BlocklistSearch = () => {
  const [blocklistItems, setBlocklistItems] = useState([]);
  const [openIndex, setOpenIndex] = useState(null);
  const [inputValue, setInputValue] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [existingEntries, setExistingEntries] = useState([]);
  const [newEntries, setNewEntries] = useState([]);

  useEffect(() => {
    fetchBlocklistItems();
  }, []);

  const fetchBlocklistItems = async () => {
    try {
      const response = await api.get('/api/blocklist/');
      setBlocklistItems(response.data);
    } catch (error) {
      console.error('There was an error fetching the blocklist items!', error);
    }
  };

  const handleModalClose = () => setShowModal(false);
  const handleModalShow = () => setShowModal(true);

  const handleModalSubmit = async ({ entry, file, notes, deleteDate, autoDelete }) => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('notes', notes);
      formData.append('delete_date', deleteDate);
      formData.append('auto_delete', autoDelete);

      try {
        const response = await api.post('/api/blocklist/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        setExistingEntries(response.data.existing_entries);
        setNewEntries(response.data.new_entries);
        fetchBlocklistItems(); // Refresh the blocklist items
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    } else {
      try {
        const response = await api.post('/api/blocklist/', { entry, notes, delete_date: deleteDate, auto_delete: autoDelete });
        setBlocklistItems([...blocklistItems, response.data]);
        fetchBlocklistItems(); // Refresh the blocklist items
      } catch (error) {
        console.error('Error adding to blocklist:', error);
      }
    }
  };

  const toggleCollapse = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  const deleteBlocklistItem = async (id) => {
    try {
      await api.delete(`/api/blocklist/${id}/`);
      fetchBlocklistItems(); // Refresh the blocklist items
    } catch (error) {
      console.error('Error deleting blocklist item:', error);
    }
  };

  const filteredBlocklist = blocklistItems
    .filter(item => !item.auto_delete && item.entry.toLowerCase().includes(inputValue.toLowerCase()))
    .sort((a, b) => new Date(b.added_on) - new Date(a.added_on));

  return (
    <div className="blocklist-container">
      <input
        type="text"
        placeholder="Search or add new item..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
      <button onClick={handleModalShow}>Add to Blocklist</button>
      <BlocklistForm
        show={showModal}
        handleClose={handleModalClose}
        handleSubmit={handleModalSubmit}
      />
      {existingEntries.length > 0 && (
        <div>
          <h4>Existing Entries</h4>
          <ul>
            {existingEntries.map((entry, index) => (
              <li key={index}>{entry}</li>
            ))}
          </ul>
        </div>
      )}
      {newEntries.length > 0 && (
        <div>
          <h4>New Entries</h4>
          <ul>
            {newEntries.map((entry, index) => (
              <li key={index}>{entry}</li>
            ))}
          </ul>
        </div>
      )}
      {filteredBlocklist.map((item, index) => (
        <Card key={item.id} className="blocklist-card">
          <Card.Header className="blocklist-card-header">
            <Button
              onClick={() => toggleCollapse(index)}
              aria-controls={`collapse-text-${index}`}
              aria-expanded={openIndex === index}
              variant="link"
              className="blocklist-toggle-button"
            >
              {item.entry}
            </Button>
            <Button
              onClick={() => deleteBlocklistItem(item.id)}
              variant="danger"
              className="blocklist-delete-button"
            >
              Delete
            </Button>
          </Card.Header>
          <Collapse in={openIndex === index}>
            <div id={`collapse-text-${index}`}>
              <Card.Body className="blocklist-card-body">
                <p><strong>Entry Type: {item.entry_type}</strong></p>
                <p><strong>Added By:</strong> {item.added_by}</p>
                <p><strong>Added On:</strong> {new Date(item.added_on).toLocaleString()}</p>
                <p><strong>Auto Delete:</strong> {item.auto_delete ? 'Yes' : 'No'}</p>
                {item.delete_date && <p><strong>Delete Date:</strong> {new Date(item.delete_date).toLocaleDateString()}</p>}
                {item.notes && <p><strong>Notes:</strong> {item.notes}</p>}
              </Card.Body>
            </div>
          </Collapse>
        </Card>
      ))}
    </div>
  );
};

export default BlocklistSearch;