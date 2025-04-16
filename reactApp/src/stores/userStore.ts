import { makeAutoObservable, runInAction } from 'mobx';
import api from '../services/api';
import { User } from '../types';

class UserStore {
  users: User[] = [];
  currentUser: User | null = null;
  loading = false;
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  fetchUsers = async () => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.get('/users');
      runInAction(() => {
        this.users = response.data;
        this.loading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = '사용자 목록을 불러오는데 실패했습니다.';
        this.loading = false;
      });
    }
  };

  fetchUserById = async (id: number) => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.get(`/users/${id}`);
      runInAction(() => {
        this.currentUser = response.data;
        this.loading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = '사용자 정보를 불러오는데 실패했습니다.';
        this.loading = false;
      });
    }
  };

  createUser = async (userData: Partial<User>) => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.post('/users', userData);
      runInAction(() => {
        this.users.push(response.data);
        this.loading = false;
      });
      return response.data;
    } catch (error) {
      runInAction(() => {
        this.error = '사용자 생성에 실패했습니다.';
        this.loading = false;
      });
      return null;
    }
  };

  updateUser = async (id: number, userData: Partial<User>) => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.put(`/users/${id}`, userData);
      runInAction(() => {
        const index = this.users.findIndex(user => user.id === id);
        if (index !== -1) {
          this.users[index] = response.data;
        }
        if (this.currentUser?.id === id) {
          this.currentUser = response.data;
        }
        this.loading = false;
      });
      return response.data;
    } catch (error) {
      runInAction(() => {
        this.error = '사용자 정보 업데이트에 실패했습니다.';
        this.loading = false;
      });
      return null;
    }
  };

  deleteUser = async (id: number) => {
    this.loading = true;
    this.error = null;
    try {
      await api.delete(`/users/${id}`);
      runInAction(() => {
        this.users = this.users.filter(user => user.id !== id);
        if (this.currentUser?.id === id) {
          this.currentUser = null;
        }
        this.loading = false;
      });
      return true;
    } catch (error) {
      runInAction(() => {
        this.error = '사용자 삭제에 실패했습니다.';
        this.loading = false;
      });
      return false;
    }
  };
}

export default new UserStore();
