import React, { useState } from 'react';
import { Container, Row, Col, Button, Navbar } from 'react-bootstrap';
import UserList from './components/UserList';
import UserForm from './components/UserForm';
import { User } from './types/User';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [showForm, setShowForm] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleAddUser = () => {
    setEditingUser(null);
    setShowForm(true);
  };

  const handleEditUser = (user: User) => {
    setEditingUser(user);
    setShowForm(true);
  };

  const handleUserSaved = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setEditingUser(null);
  };

  return (
    <div className="App">
      <Navbar bg="primary" variant="dark" className="mb-4">
        <Container>
          <Navbar.Brand>用户管理系统</Navbar.Brand>
        </Container>
      </Navbar>

      <Container>
        <Row>
          <Col>
            <div className="d-flex justify-content-between align-items-center mb-4">
              <h2>用户管理</h2>
              <Button variant="primary" onClick={handleAddUser}>
                添加用户
              </Button>
            </div>
            
            <UserList 
              onEditUser={handleEditUser} 
              refreshTrigger={refreshTrigger}
            />
            
            <UserForm
              show={showForm}
              onHide={handleCloseForm}
              onUserSaved={handleUserSaved}
              editingUser={editingUser}
            />
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
