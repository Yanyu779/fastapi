import React, { useState, useEffect } from 'react';
import { Form, Button, Alert, Modal } from 'react-bootstrap';
import { User } from '../types/User';
import { userService } from '../services/api';

interface UserFormProps {
  show: boolean;
  onHide: () => void;
  onUserSaved: () => void;
  editingUser?: User | null;
}

const UserForm: React.FC<UserFormProps> = ({ show, onHide, onUserSaved, editingUser }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (editingUser) {
      setFormData({
        name: editingUser.name,
        email: editingUser.email,
      });
    } else {
      setFormData({
        name: '',
        email: '',
      });
    }
    setError('');
  }, [editingUser, show]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (editingUser) {
        await userService.updateUser(editingUser.id, formData);
      } else {
        await userService.createUser(formData);
      }
      onUserSaved();
      onHide();
    } catch (err: any) {
      setError(err.response?.data?.error || '操作失败');
      console.error('Error saving user:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>{editingUser ? '编辑用户' : '添加用户'}</Modal.Title>
      </Modal.Header>
      <Form onSubmit={handleSubmit}>
        <Modal.Body>
          {error && <Alert variant="danger">{error}</Alert>}
          <Form.Group className="mb-3">
            <Form.Label>姓名</Form.Label>
            <Form.Control
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>邮箱</Form.Label>
            <Form.Control
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={onHide} disabled={loading}>
            取消
          </Button>
          <Button variant="primary" type="submit" disabled={loading}>
            {loading ? '保存中...' : '保存'}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default UserForm;