import axios from 'axios';
import { User } from '../types/User';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const userService = {
  // 获取所有用户
  getUsers: async (): Promise<User[]> => {
    const response = await api.get('/users');
    return response.data;
  },

  // 创建新用户
  createUser: async (userData: { name: string; email: string }): Promise<User> => {
    const response = await api.post('/users', userData);
    return response.data;
  },

  // 获取特定用户
  getUser: async (id: number): Promise<User> => {
    const response = await api.get(`/users/${id}`);
    return response.data;
  },

  // 更新用户
  updateUser: async (id: number, userData: { name?: string; email?: string }): Promise<User> => {
    const response = await api.put(`/users/${id}`, userData);
    return response.data;
  },

  // 删除用户
  deleteUser: async (id: number): Promise<void> => {
    await api.delete(`/users/${id}`);
  },
};

export default api;