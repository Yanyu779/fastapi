import React, { useState, useEffect } from 'react';
import {
  Container,
  Row,
  Col,
  Card,
  Button,
  Table,
  Modal,
  Form,
  Alert,
  Spinner,
  Badge,
  Navbar,
  Nav
} from 'react-bootstrap';
import { User } from './types/User';
import { userService } from './services/api';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [users, setUsers] = useState<User[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [formLoading, setFormLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');
  const [formData, setFormData] = useState({ name: '', email: '' });

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const usersData = await userService.getUsers();
      setUsers(usersData);
      setError('');
    } catch (err) {
      setError('获取用户列表失败，请检查网络连接');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormLoading(true);
    setError('');

    try {
      if (editingUser) {
        await userService.updateUser(editingUser.id, formData);
        setSuccess('用户更新成功！');
      } else {
        await userService.createUser(formData);
        setSuccess('用户添加成功！');
      }
      
      handleCloseModal();
      fetchUsers();
      
      setTimeout(() => setSuccess(''), 3000);
    } catch (err: any) {
      setError(err.response?.data?.error || '操作失败，请重试');
    } finally {
      setFormLoading(false);
    }
  };

  const handleDelete = async (id: number, name: string) => {
    if (window.confirm(`确定要删除用户 "${name}" 吗？此操作不可撤销。`)) {
      try {
        await userService.deleteUser(id);
        setUsers(users.filter(user => user.id !== id));
        setSuccess('用户删除成功！');
        setTimeout(() => setSuccess(''), 3000);
      } catch (err) {
        setError('删除失败，请重试');
      }
    }
  };

  const handleAddUser = () => {
    setEditingUser(null);
    setFormData({ name: '', email: '' });
    setShowModal(true);
  };

  const handleEditUser = (user: User) => {
    setEditingUser(user);
    setFormData({ name: user.name, email: user.email });
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingUser(null);
    setFormData({ name: '', email: '' });
    setError('');
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="app-container">
      {/* 导航栏 */}
      <Navbar bg="primary" variant="dark" expand="lg" className="shadow-sm">
        <Container>
          <Navbar.Brand className="fw-bold">
            <i className="bi bi-people-fill me-2"></i>
            用户管理系统
          </Navbar.Brand>
          <Nav className="ms-auto">
            <Badge bg="light" text="dark" className="user-count">
              总用户数: {users.length}
            </Badge>
          </Nav>
        </Container>
      </Navbar>

      <Container fluid className="main-content">
        <Row className="justify-content-center">
          <Col lg={10} xl={8}>
            {/* 页面标题和操作区 */}
            <div className="page-header">
              <Row className="align-items-center mb-4">
                <Col>
                  <h2 className="page-title">
                    <i className="bi bi-person-lines-fill me-2"></i>
                    用户管理
                  </h2>
                  <p className="text-muted">管理系统中的所有用户信息</p>
                </Col>
                <Col xs="auto">
                  <Button 
                    variant="primary" 
                    size="lg"
                    onClick={handleAddUser}
                    className="add-user-btn"
                  >
                    <i className="bi bi-person-plus me-2"></i>
                    添加用户
                  </Button>
                </Col>
              </Row>
            </div>

            {/* 消息提示 */}
            {error && (
              <Alert variant="danger" dismissible onClose={() => setError('')}>
                <i className="bi bi-exclamation-triangle me-2"></i>
                {error}
              </Alert>
            )}

            {success && (
              <Alert variant="success" dismissible onClose={() => setSuccess('')}>
                <i className="bi bi-check-circle me-2"></i>
                {success}
              </Alert>
            )}

            {/* 用户列表卡片 */}
            <Card className="shadow-sm users-card">
              <Card.Header className="bg-light">
                <Row className="align-items-center">
                  <Col>
                    <h5 className="mb-0">
                      <i className="bi bi-list-ul me-2"></i>
                      用户列表
                    </h5>
                  </Col>
                  <Col xs="auto">
                    <Button
                      variant="outline-primary"
                      size="sm"
                      onClick={fetchUsers}
                      disabled={loading}
                    >
                      <i className="bi bi-arrow-clockwise me-1"></i>
                      刷新
                    </Button>
                  </Col>
                </Row>
              </Card.Header>

              <Card.Body className="p-0">
                {loading ? (
                  <div className="text-center py-5">
                    <Spinner animation="border" role="status" className="mb-3">
                      <span className="visually-hidden">加载中...</span>
                    </Spinner>
                    <p className="text-muted">正在加载用户数据...</p>
                  </div>
                ) : users.length === 0 ? (
                  <div className="text-center py-5">
                    <i className="bi bi-inbox display-1 text-muted mb-3"></i>
                    <h5 className="text-muted">暂无用户数据</h5>
                    <p className="text-muted">点击上方"添加用户"按钮开始添加用户</p>
                  </div>
                ) : (
                  <div className="table-responsive">
                    <Table hover className="mb-0">
                      <thead className="table-light">
                        <tr>
                          <th style={{ width: '80px' }}>
                            <i className="bi bi-hash"></i> ID
                          </th>
                          <th>
                            <i className="bi bi-person me-1"></i>姓名
                          </th>
                          <th>
                            <i className="bi bi-envelope me-1"></i>邮箱
                          </th>
                          <th>
                            <i className="bi bi-calendar me-1"></i>创建时间
                          </th>
                          <th style={{ width: '180px' }}>
                            <i className="bi bi-gear me-1"></i>操作
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {users.map((user, index) => (
                          <tr key={user.id} className="user-row">
                            <td>
                              <Badge bg="secondary" className="user-id-badge">
                                {user.id}
                              </Badge>
                            </td>
                            <td className="fw-medium">{user.name}</td>
                            <td>
                              <a href={`mailto:${user.email}`} className="email-link">
                                {user.email}
                              </a>
                            </td>
                            <td className="text-muted">
                              {formatDate(user.created_at)}
                            </td>
                            <td>
                              <div className="btn-group">
                                <Button
                                  variant="outline-primary"
                                  size="sm"
                                  onClick={() => handleEditUser(user)}
                                  className="action-btn"
                                >
                                  <i className="bi bi-pencil"></i>
                                </Button>
                                <Button
                                  variant="outline-danger"
                                  size="sm"
                                  onClick={() => handleDelete(user.id, user.name)}
                                  className="action-btn"
                                >
                                  <i className="bi bi-trash"></i>
                                </Button>
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </Table>
                  </div>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>

      {/* 添加/编辑用户模态框 */}
      <Modal show={showModal} onHide={handleCloseModal} centered>
        <Modal.Header closeButton className="bg-primary text-white">
          <Modal.Title>
            <i className={`bi ${editingUser ? 'bi-pencil' : 'bi-person-plus'} me-2`}></i>
            {editingUser ? '编辑用户' : '添加用户'}
          </Modal.Title>
        </Modal.Header>

        <Form onSubmit={handleSubmit}>
          <Modal.Body className="p-4">
            {error && (
              <Alert variant="danger" className="mb-3">
                <i className="bi bi-exclamation-triangle me-2"></i>
                {error}
              </Alert>
            )}

            <Form.Group className="mb-3">
              <Form.Label className="fw-medium">
                <i className="bi bi-person me-1"></i>姓名
              </Form.Label>
              <Form.Control
                type="text"
                placeholder="请输入用户姓名"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
                disabled={formLoading}
                className="form-input"
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label className="fw-medium">
                <i className="bi bi-envelope me-1"></i>邮箱
              </Form.Label>
              <Form.Control
                type="email"
                placeholder="请输入邮箱地址"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
                disabled={formLoading}
                className="form-input"
              />
            </Form.Group>
          </Modal.Body>

          <Modal.Footer className="bg-light">
            <Button 
              variant="secondary" 
              onClick={handleCloseModal}
              disabled={formLoading}
            >
              取消
            </Button>
            <Button 
              variant="primary" 
              type="submit"
              disabled={formLoading}
              className="submit-btn"
            >
              {formLoading ? (
                <>
                  <Spinner
                    as="span"
                    animation="border"
                    size="sm"
                    role="status"
                    className="me-2"
                  />
                  {editingUser ? '更新中...' : '添加中...'}
                </>
              ) : (
                <>
                  <i className={`bi ${editingUser ? 'bi-check' : 'bi-plus'} me-2`}></i>
                  {editingUser ? '更新用户' : '添加用户'}
                </>
              )}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </div>
  );
}

export default App;
