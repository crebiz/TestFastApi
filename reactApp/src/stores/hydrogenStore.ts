import { makeAutoObservable, runInAction } from 'mobx';
import api from '../services/api';
import { HydrogenStation } from '../types';

class HydrogenStore {
  stations: HydrogenStation[] = [];
  currentStation: HydrogenStation | null = null;
  loading = false;
  error: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  fetchStations = async () => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.get('/hydrogen-stations');
      runInAction(() => {
        this.stations = response.data;
        this.loading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = '수소 스테이션 목록을 불러오는데 실패했습니다.';
        this.loading = false;
      });
    }
  };

  fetchStationById = async (id: number) => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.get(`/hydrogen-stations/${id}`);
      runInAction(() => {
        this.currentStation = response.data;
        this.loading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = '수소 스테이션 정보를 불러오는데 실패했습니다.';
        this.loading = false;
      });
    }
  };

  createStation = async (stationData: Partial<HydrogenStation>) => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.post('/hydrogen-stations', stationData);
      runInAction(() => {
        this.stations.push(response.data);
        this.loading = false;
      });
      return response.data;
    } catch (error) {
      runInAction(() => {
        this.error = '수소 스테이션 생성에 실패했습니다.';
        this.loading = false;
      });
      return null;
    }
  };

  updateStation = async (id: number, stationData: Partial<HydrogenStation>) => {
    this.loading = true;
    this.error = null;
    try {
      const response = await api.put(`/hydrogen-stations/${id}`, stationData);
      runInAction(() => {
        const index = this.stations.findIndex(station => station.id === id);
        if (index !== -1) {
          this.stations[index] = response.data;
        }
        if (this.currentStation?.id === id) {
          this.currentStation = response.data;
        }
        this.loading = false;
      });
      return response.data;
    } catch (error) {
      runInAction(() => {
        this.error = '수소 스테이션 정보 업데이트에 실패했습니다.';
        this.loading = false;
      });
      return null;
    }
  };

  deleteStation = async (id: number) => {
    this.loading = true;
    this.error = null;
    try {
      await api.delete(`/hydrogen-stations/${id}`);
      runInAction(() => {
        this.stations = this.stations.filter(station => station.id !== id);
        if (this.currentStation?.id === id) {
          this.currentStation = null;
        }
        this.loading = false;
      });
      return true;
    } catch (error) {
      runInAction(() => {
        this.error = '수소 스테이션 삭제에 실패했습니다.';
        this.loading = false;
      });
      return false;
    }
  };
}

// 인스턴스 생성 후 내보내기
const hydrogenStore = new HydrogenStore();
export default hydrogenStore;
