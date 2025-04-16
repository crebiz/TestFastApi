import userStore from './userStore';
import categoryStore from './categoryStore';
import hydrogenStore from './hydrogenStore';
import authStore from './authStore';

// 루트 스토어 - 모든 스토어를 통합
class RootStore {
  userStore = userStore;
  categoryStore = categoryStore;
  hydrogenStore = hydrogenStore;
  authStore = authStore;
}

const rootStore = new RootStore();
export default rootStore;
