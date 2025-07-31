import React, { useState, useEffect } from 'react';
import { Table, Button, Alert, Spinner } from 'react-bootstrap';
import { User } from '../types/User';
import { userService } from '../services/api';

interface UserListProps {
  onEditUser: (user: User) => void;
  refreshTrigger: number;
}

const UserList: React.FC<UserListProps> = ({ onEditUser, refreshTrigger }) => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    fetchUsers();
  }, [refreshTrigger]);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      setError('');
      const usersData = await userService.getUsers();
      setUsers(usersData);
    } catch (err) {
      setError('获取用户列表失败');
      console.error('Error fetching users:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('确定要删除这个用户吗？')) {
      try {
        await userService.deleteUser(id);
        setUsers(users.filter(user => user.id !== id));
      } catch (err) {
        setError('删除用户失败');
        console.error('Error deleting user:', err);
      }
    }
  };

  if (loading) {
    return (
      <div className="text-center p-4">
        <Spinner animation="border" />
        <p>加载中...</p>
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger">{error}</Alert>;
  }

  return (
    <div>
      <h3>用户列表</h3>
      {users.length === 0 ? (
        <Alert variant="info">暂无用户</Alert>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>ID</th>
              <th>姓名</th>
              <th>邮箱</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{new Date(user.created_at).toLocaleString()}</td>
                <td>
                  <Button
                    variant="outline-primary"
                    size="sm"
                    className="me-2"
                    onClick={() => onEditUser(user)}
                  >
                    编辑
                  </Button>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={() => handleDelete(user.id)}
                  >
                    删除
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  );
};

export default UserList;