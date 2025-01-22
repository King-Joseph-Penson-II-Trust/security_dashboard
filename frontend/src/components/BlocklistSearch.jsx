import React, { useState, useEffect } from "react";
import api from "../api";
import { Card, Button, Collapse } from "react-bootstrap";
import "../styles/BlocklistSearch.css";

const BlocklistSearch = () => {
  const [blocklistItems, setBlocklistItems] = useState([]);
  const [openIndex, setOpenIndex] = useState(null);
  const [inputValue, setInputValue] = useState('');

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

  const addToBlocklist = async () => {
    try {
      const response = await api.post('/api/blocklist/', { entry: inputValue });
      setBlocklistItems([...blocklistItems, response.data]);
      setInputValue(''); // Clear input after adding
    } catch (error) {
      console.error('Error adding to blocklist:', error);
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
      <button onClick={addToBlocklist}>Add to Blocklist</button>
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