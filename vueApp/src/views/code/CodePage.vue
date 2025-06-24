<template>
  <div>
    <v-row>
      <!-- 부모코드 관리 (상단) -->
      <v-col cols="12">
        <v-card elevation="3" rounded="lg" class="mb-4">
          <v-toolbar flat color="primary" dark class="rounded-t-lg">
            <v-icon class="mr-2 ml-2">mdi-code-brackets</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">그룹코드 관리</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon @click="openParentDrawer(null, 'add')">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-toolbar>

          <v-card-text>
            <v-text-field v-model="parentSearch" label="그룹코드 검색" prepend-inner-icon="mdi-magnify" clearable outlined
              dense hide-details class="mb-4"></v-text-field>

            <v-data-table :headers="parentHeaders" :items="filteredParentCodes" :loading="isParentLoading"
              :items-per-page="-1" hide-default-footer class="elevation-1">
              <template v-slot:no-data>
                <div class="text-center pa-5">
                  <v-icon size="x-large" color="grey-lighten-1" class="mb-3">mdi-database-off</v-icon>
                  <div class="text-subtitle-1 text-grey">
                    조회결과가 없습니다.
                  </div>
                </div>
              </template>
              <template v-slot:item="props">
                <tr @click="selectParentCode(props.item)" style="cursor: pointer;">
                  <td>{{ props.item.code_id }}</td>
                  <td>{{ props.item.code_name }}</td>
                  <td>{{ props.item.description }}</td>
                  <td>
                    <v-chip :color="props.item.use_yn === 'Y' ? 'success' : 'error'" size="small"
                      :text="props.item.use_yn === 'Y' ? '사용' : '미사용'"></v-chip>
                  </td>
                  <td>
                    <v-icon size="small" class="me-2" @click.stop="openParentDrawer(props.item, 'edit')">
                      mdi-pencil
                    </v-icon>
                    <v-icon size="small" @click.stop="deleteParentCode(props.item)">
                      mdi-delete
                    </v-icon>
                  </td>
                </tr>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- 자식코드 관리 (하단) -->
      <v-col cols="12">
        <v-card elevation="3" rounded="lg">
          <v-toolbar flat color="secondary" dark class="rounded-t-lg">
            <v-icon class="mr-2 ml-2">mdi-code-array</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">
              상세코드 관리
              <span v-if="selectedParentCode" class="text-subtitle-2 ms-2">
                ({{ selectedParentCode.code_name }})
              </span>
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon :disabled="!selectedParentCode" @click="openChildDrawer(null, 'add')">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-toolbar>

          <v-card-text>
            <v-data-table :headers="childHeaders" :items="childCodes" :loading="isChildLoading" :items-per-page="-1"
              hide-default-footer class="elevation-1" :disabled="!selectedParentCode">
              <template v-slot:item="props">
                <tr @click="openChildDrawer(props.item, 'edit')" style="cursor: pointer;">
                  <td>{{ props.item.code_id }}</td>
                  <td>{{ props.item.code_name }}</td>
                  <td>{{ props.item.sort_order }}</td>
                  <td>{{ props.item.description }}</td>
                  <td>
                    <v-chip :color="props.item.use_yn === 'Y' ? 'success' : 'error'" size="small"
                      :text="props.item.use_yn === 'Y' ? '사용' : '미사용'"></v-chip>
                  </td>
                  <td>
                    <v-icon size="small" @click.stop="deleteChildCode(props.item)">
                      mdi-delete
                    </v-icon>
                  </td>
                </tr>
              </template>

              <template v-slot:no-data>
                <div class="text-center pa-5">
                  <v-icon size="x-large" color="grey-lighten-1" class="mb-3">mdi-database-off</v-icon>
                  <div class="text-subtitle-1 text-grey">
                    {{ selectedParentCode ? '조회결과가 없습니다.' : '상단에서 그룹코드를 선택해주세요.' }}
                  </div>
                </div>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 그룹코드 추가/수정 슬라이드 패널 -->
    <v-navigation-drawer v-model="parentDialog" location="right" temporary width="520" class="group-code-drawer"
      elevation="24">
      <v-card flat class="h-100" style="border-radius: 0">
        <v-toolbar flat dark class="pa-3">
          <v-toolbar-title class="text-h6 font-weight-medium ml-2 text-truncate">
            {{ parentDialogTitle }}
          </v-toolbar-title>
          <v-btn icon @click="parentDialog = false" class="mr-2">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>

        <v-card-text class="pa-6">
          <v-form @submit.prevent="saveParentCode">
            <v-card flat class="mb-4 px-2">
              <v-list>
                <!-- 코드 ID -->
                <v-list-item density="compact" class="py-3">
                  <template v-slot:prepend>
                    <v-avatar color="primary" size="32" class="mr-3">
                      <v-icon color="white" size="small">mdi-identifier</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-subtitle-2 font-weight-medium">코드 ID</v-list-item-title>
                  <template v-slot:append>
                    <v-text-field v-model="editedParentCode.code_id" :disabled="parentDialogMode === 'edit'"
                      variant="outlined" density="compact" hide-details class="edit-field" style="min-width: 200px;"
                      required @input="editedParentCode.code_id = $event.target.value.toUpperCase()"
                      placeholder="예: G001"></v-text-field>
                  </template>
                </v-list-item>

                <v-divider></v-divider>

                <!-- 코드명 -->
                <v-list-item density="compact" class="py-3">
                  <template v-slot:prepend>
                    <v-avatar color="tertiary" size="32" class="mr-3">
                      <v-icon color="white" size="small">mdi-tag</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-subtitle-2 font-weight-medium">코드명</v-list-item-title>
                  <template v-slot:append>
                    <v-text-field v-model="editedParentCode.code_name" variant="outlined" density="compact" hide-details
                      class="edit-field" style="min-width: 200px;" required></v-text-field>
                  </template>
                </v-list-item>

                <v-divider></v-divider>

                <!-- 사용 여부 -->
                <v-list-item density="compact" class="py-3">
                  <template v-slot:prepend>
                    <v-avatar :color="editedParentCode.use_yn === 'Y' ? 'success' : 'error'" size="32" class="mr-3">
                      <v-icon color="white" size="small">{{ editedParentCode.use_yn === 'Y' ? 'mdi-check' : 'mdi-close'
                      }}</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-subtitle-2 font-weight-medium">사용 여부</v-list-item-title>
                  <template v-slot:append>
                    <v-switch v-model="editedParentCode.use_yn" :true-value="'Y'" :false-value="'N'" color="success"
                      hide-details :label="editedParentCode.use_yn === 'Y' ? '사용' : '미사용'"></v-switch>
                  </template>
                </v-list-item>
              </v-list>
            </v-card>

            <!-- 설명 -->
            <v-sheet rounded class="pa-4 mb-4 bg-grey-lighten-5">
              <div class="text-subtitle-2 font-weight-medium mb-2">설명</div>
              <v-textarea v-model="editedParentCode.description" variant="outlined" density="compact" hide-details
                placeholder="설명을 입력하세요" rows="3"></v-textarea>
            </v-sheet>

            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn variant="text" color="tertiary" @click="parentDialog = false">취소</v-btn>
              <v-btn color="primary" variant="elevated" @click="saveParentCode">
                <v-icon left>mdi-content-save</v-icon>
                저장
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-navigation-drawer>

    <!-- 상세코드 추가/수정 슬라이드 패널 -->
    <v-navigation-drawer v-model="childDialog" location="right" temporary width="520" class="detail-code-drawer"
      elevation="24">
      <v-card flat class="h-100" style="border-radius: 0">
        <v-toolbar flat dark class="pa-3">
          <v-toolbar-title class="text-h6 font-weight-medium ml-2 text-truncate">
            {{ childDialogTitle }}
            <span v-if="selectedParentCode" class="text-subtitle-2 ms-2">
              ({{ selectedParentCode.code_name }})
            </span>
          </v-toolbar-title>
          <v-btn icon @click="childDialog = false" class="mr-2">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>

        <v-card-text class="pa-6">
          <v-form @submit.prevent="saveChildCode">
            <v-card flat class="mb-4 px-2">
              <v-list>
                <!-- 그룹코드 -->
                <v-list-item density="compact" class="py-3">
                  <template v-slot:prepend>
                    <v-avatar color="primary" size="32" class="mr-3">
                      <v-icon color="white" size="small">mdi-code-brackets</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-subtitle-2 font-weight-medium">그룹코드</v-list-item-title>
                  <template v-slot:append>
                    <div class="text-body-1">{{ selectedParentCode ? selectedParentCode.code_name : '' }}</div>
                  </template>
                </v-list-item>

                <v-divider></v-divider>

                <!-- 코드 ID -->
                <v-list-item density="compact" class="py-3">
                  <template v-slot:prepend>
                    <v-avatar color="secondary" size="32" class="mr-3">
                      <v-icon color="white" size="small">mdi-identifier</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-subtitle-2 font-weight-medium">코드 ID</v-list-item-title>
                  <template v-slot:append>
                    <v-text-field v-model="editedChildCode.code_id" :disabled="childDialogMode === 'edit'"
                      variant="outlined" density="compact" hide-details class="edit-field" style="min-width: 200px;"
                      required @input="editedChildCode.code_id = $event.target.value.toUpperCase()"
                      placeholder="예: C001"></v-text-field>
                  </template>
                </v-list-item>

                <v-divider></v-divider>

                <!-- 코드명 -->
                <v-list-item density="compact" class="py-3">
                  <template v-slot:prepend>
                    <v-avatar color="tertiary" size="32" class="mr-3">
                      <v-icon color="white" size="small">mdi-tag</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-subtitle-2 font-weight-medium">코드명</v-list-item-title>
                  <template v-slot:append>
                    <v-text-field v-model="editedChildCode.code_name" variant="outlined" density="compact" hide-details
                      class="edit-field" style="min-width: 200px;" required></v-text-field>
                  </template>
                </v-list-item>

                <v-divider></v-divider>

                <!-- 값(Value) -->
                <v-list-item density="compact" class="py-3">
                  <template v-slot:prepend>
                    <v-avatar color="secondary" size="32" class="mr-3">
                      <v-icon color="white" size="small">mdi-key-variant</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-subtitle-2 font-weight-medium">값(Value)</v-list-item-title>
                  <template v-slot:append>
                    <v-text-field v-model="editedChildCode.value" variant="outlined" density="compact" hide-details
                      class="edit-field" style="min-width: 200px;" placeholder="예: SH"></v-text-field>
                  </template>
                </v-list-item>

                <v-divider></v-divider>

                <!-- 아이콘 -->
                <v-list-item density="compact" class="py-3">
                  <template v-slot:prepend>
                    <v-avatar color="tertiary" size="32" class="mr-3">
                      <v-icon color="white" size="small">mdi-emoticon-outline</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-subtitle-2 font-weight-medium">아이콘</v-list-item-title>
                  <template v-slot:append>
                    <v-text-field v-model="editedChildCode.icon" variant="outlined" density="compact" hide-details
                      class="edit-field" style="min-width: 200px;" placeholder="예: mdi-emoticon-outline"></v-text-field>
                  </template>
                </v-list-item>

                <v-divider></v-divider>

                <!-- 정렬 순서 -->
                <v-list-item density="compact" class="py-3">
                  <template v-slot:prepend>
                    <v-avatar color="secondary" size="32" class="mr-3">
                      <v-icon color="white" size="small">mdi-sort-numeric-ascending</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-subtitle-2 font-weight-medium">정렬 순서</v-list-item-title>
                  <template v-slot:append>
                    <v-text-field v-model="editedChildCode.sort_order" type="number" variant="outlined"
                      density="compact" hide-details class="edit-field" style="min-width: 200px;"></v-text-field>
                  </template>
                </v-list-item>

                <v-divider></v-divider>

                <!-- 사용 여부 -->
                <v-list-item density="compact" class="py-3">
                  <template v-slot:prepend>
                    <v-avatar :color="editedChildCode.use_yn === 'Y' ? 'success' : 'error'" size="32" class="mr-3">
                      <v-icon color="white" size="small">{{ editedChildCode.use_yn === 'Y' ? 'mdi-check' : 'mdi-close'
                      }}</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-subtitle-2 font-weight-medium">사용 여부</v-list-item-title>
                  <template v-slot:append>
                    <v-switch v-model="editedChildCode.use_yn" :true-value="'Y'" :false-value="'N'" color="success"
                      hide-details :label="editedChildCode.use_yn === 'Y' ? '사용' : '미사용'"></v-switch>
                  </template>
                </v-list-item>
              </v-list>
            </v-card>
            <!-- 설명 -->
            <v-sheet rounded class="pa-4 mb-4 bg-grey-lighten-5">
              <div class="text-subtitle-2 font-weight-medium mb-2">설명</div>
              <v-textarea v-model="editedChildCode.description" variant="outlined" density="compact" hide-details
                placeholder="설명을 입력하세요" rows="3"></v-textarea>
            </v-sheet>
          </v-form>
          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn variant="text" color="tertiary" @click="childDialog = false">취소</v-btn>
            <v-btn color="primary" variant="elevated" @click="saveChildCode">
              <v-icon left>mdi-content-save</v-icon>
              저장
            </v-btn>
          </v-card-actions>
        </v-card-text>
      </v-card>
    </v-navigation-drawer>

    <!-- 스낵바 -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" location="bottom right" timeout="2500">
      {{ snackbarText }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar = false">닫기</v-btn>
      </template>
    </v-snackbar>

    <!-- 확인 다이얼로그 (Material 스타일) -->
    <v-dialog v-model="confirmDialog" max-width="420" persistent>
      <v-card>
        <v-card-title class="text-h5 pa-4">
          <v-icon color="primary" class="mr-2">mdi-alert-circle</v-icon>
          {{ confirmTitle }}
        </v-card-title>
        <v-card-text class="pa-4 pt-0">
          {{ confirmMessage }}
        </v-card-text>
        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn variant="text" color="tertiary" @click="confirmDialog = false">취소</v-btn>
          <v-btn color="error" variant="elevated" @click="confirmAction()">
            <v-icon left>mdi-delete</v-icon>
            삭제
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { getApiUrl } from '@/config/api';

// API 응답 데이터 타입 정의
interface ApiCodeGroup {
  id: string;
  name: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  details?: ApiCodeDetail[];
}

interface ApiCodeDetail {
  id: string;
  group_id: string;
  name: string;
  value?: string;
  description?: string;
  sort_order?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface ParentCode {
  code_id: string;
  code_name: string;
  description: string;
  use_yn: string;
  sort_order?: number;
  created_at?: string;
  updated_at?: string;
}

interface ChildCode {
  parent_code_id: string;
  code_id: string;
  code_name: string;
  value?: string;
  description: string;
  sort_order: number;
  use_yn: string;
  icon?: string;
  created_at?: string;
  updated_at?: string;
}

export default defineComponent({
  name: 'CodePage',

  setup() {
    // 부모코드 관련 상태
    const parentCodes = ref<ParentCode[]>([]);
    const isParentLoading = ref(false);
    const parentSearch = ref('');
    const selectedParentCode = ref<ParentCode | null>(null);

    // 자식코드 관련 상태
    const childCodes = ref<ChildCode[]>([]);
    const isChildLoading = ref(false);

    // 다이얼로그 관련 상태
    const parentDialog = ref(false);
    const childDialog = ref(false);
    const parentDialogMode = ref<'add' | 'edit'>('add');
    const childDialogMode = ref<'add' | 'edit'>('add');
    const editedParentCode = ref<ParentCode>({
      code_id: '',
      code_name: '',
      description: '',
      use_yn: 'Y'
    });
    const editedChildCode = ref<ChildCode>({
      parent_code_id: '',
      code_id: '',
      code_name: '',
      description: '',
      sort_order: 0,
      use_yn: 'Y',
      icon: ''
    });

    // 스낵바 관련 상태
    const snackbar = ref(false);
    const snackbarText = ref('');
    const snackbarColor = ref('success');

    // 테이블 헤더 정의
    const parentHeaders = [
      { text: '코드 ID', value: 'code_id', width: '100px' },
      { text: '코드명', value: 'code_name', width: '150px' },
      { text: '설명', value: 'description' },
      { text: '사용여부', value: 'use_yn', width: '100px' },
      { text: '관리', value: 'actions', width: '100px', sortable: false }
    ];

    const childHeaders = [
      { text: '코드 ID', value: 'code_id', width: '100px' },
      { text: '코드명', value: 'code_name', width: '150px' },
      { text: '정렬순서', value: 'sort_order', width: '100px' },
      { text: '설명', value: 'description' },
      { text: '사용여부', value: 'use_yn', width: '100px' },
      { text: '관리', value: 'actions', width: '100px', sortable: false }
    ];

    // 필터링된 부모코드 목록
    const filteredParentCodes = computed(() => {
      if (!parentSearch.value) return parentCodes.value;

      const searchTerm = parentSearch.value.toLowerCase();
      return parentCodes.value.filter(code =>
        code.code_id.toLowerCase().includes(searchTerm) ||
        code.code_name.toLowerCase().includes(searchTerm) ||
        code.description.toLowerCase().includes(searchTerm)
      );
    });

    // 다이얼로그 제목
    const parentDialogTitle = computed(() =>
      parentDialogMode.value === 'add' ? '그룹코드 추가' : '그룹코드 수정'
    );

    const childDialogTitle = computed(() =>
      childDialogMode.value === 'add' ? '상세코드 추가' : '상세코드 수정'
    );

    // 그룹코드 목록 조회
    const fetchParentCodes = async () => {
      isParentLoading.value = true;

      try {
        // 실제 API 호출 - 환경별 기본 URL 사용
        const response = await axios.get<ApiCodeGroup[]>(getApiUrl('/api/codes/groups'));
        console.log(response.data);
        if (response.data.length === 0) {
          // 그룹코드가 없는 경우
          parentCodes.value = [];
          // 그룹코드가 없다는 알림은 표시하지 않고, 테이부 내부에 '조회결과가 없습니다' 메시지가 표시됨
        } else {
          // API 응답 데이터 형식에 맞게 변환
          parentCodes.value = response.data.map((group: ApiCodeGroup) => ({
            code_id: group.id,
            code_name: group.name,
            description: group.description || '',
            use_yn: group.is_active ? 'Y' : 'N',
            created_at: group.created_at,
            updated_at: group.updated_at
          }));
        }
      } catch (error) {
        console.error('그룹코드 목록 조회 중 오류 발생:', error);
        showSnackbar('그룹코드 목록을 불러오는데 실패했습니다.', 'error');
      } finally {
        isParentLoading.value = false;
      }
    };

    // 상세코드 목록 조회
    const fetchChildCodes = async (parentCode: ParentCode) => {
      if (!parentCode || !parentCode.code_id) {
        childCodes.value = [];
        return;
      }

      isChildLoading.value = true;
      selectedParentCode.value = parentCode;

      try {
        // 실제 API 호출 - 환경별 기본 URL 사용
        const response = await axios.get<ApiCodeDetail[]>(getApiUrl(`/api/codes/details?group_id=${parentCode.code_id}`));

        if (response.data.length === 0) {
          // 상세코드가 없는 경우
          childCodes.value = [];
          // 상세코드가 없다는 알림은 표시하지 않고, 테이부 내부에 '조회결과가 없습니다' 메시지가 표시됨
        } else {
          // API 응답 데이터 형식에 맞게 변환
          childCodes.value = response.data.map((detail: ApiCodeDetail) => ({
            parent_code_id: detail.group_id,
            code_id: detail.id,
            code_name: detail.name,
            description: detail.description || '',
            sort_order: detail.sort_order ? parseInt(detail.sort_order) : 0,
            use_yn: detail.is_active ? 'Y' : 'N',
            created_at: detail.created_at,
            updated_at: detail.updated_at
          }));
        }
      } catch (error) {
        console.error('상세코드 목록 조회 중 오류 발생:', error);
        showSnackbar('상세코드 목록을 불러오는데 실패했습니다.', 'error');
      } finally {
        isChildLoading.value = false;
      }
    };

    // 부모코드 선택
    const selectParentCode = (item: ParentCode) => {
      console.log('부모코드 선택: ', item);
      selectedParentCode.value = item;
      fetchChildCodes(item);
    };

    // 그룹코드 슬라이드 패널 열기
    const openParentDrawer = (item: ParentCode | null, mode: 'add' | 'edit') => {
      parentDialogMode.value = mode;

      if (mode === 'edit' && item) {
        editedParentCode.value = { ...item };
      } else {
        editedParentCode.value = {
          code_id: '',
          code_name: '',
          description: '',
          use_yn: 'Y'
        };
      }

      parentDialog.value = true;
    };

    // 그룹코드 슬라이드 패널 닫기
    const closeParentDialog = () => {
      parentDialog.value = false;
    };

    // 그룹코드 저장
    const saveParentCode = async () => {
      // 유효성 검사
      if (!editedParentCode.value.code_id || !editedParentCode.value.code_name) {
        showSnackbar('코드 ID와 코드명은 필수 입력 항목입니다.', 'error');
        return;
      }

      try {
        // 코드 ID를 대문자로 변환
        editedParentCode.value.code_id = editedParentCode.value.code_id.toUpperCase();

        // API 요청 데이터 형식에 맞게 변환
        const apiData = {
          id: editedParentCode.value.code_id,
          name: editedParentCode.value.code_name,
          description: editedParentCode.value.description,
          is_active: editedParentCode.value.use_yn === 'Y'
        };

        if (parentDialogMode.value === 'add') {
          // 그룹코드 추가 API 호출 - 환경별 기본 URL 사용
          await axios.post(getApiUrl('/api/codes/groups'), apiData);
          showSnackbar('그룹코드가 추가되었습니다.', 'success');
        } else {
          // 그룹코드 수정 API 호출 - 환경별 기본 URL 사용
          await axios.put(getApiUrl(`/api/codes/groups/${editedParentCode.value.code_id}`), apiData);
          showSnackbar('그룹코드가 수정되었습니다.', 'success');
        }

        // 그룹코드 목록 새로고침
        fetchParentCodes();
        closeParentDialog();
      } catch (error) {
        console.error('그룹코드 저장 중 오류 발생:', error);
        showSnackbar('그룹코드 저장에 실패했습니다.', 'error');
      }
    };

    // 그룹코드 삭제 (Vuetify 다이얼로그 사용)
    const deleteParentCode = async (item: ParentCode) => {
      showConfirmDialog(
        '그룹코드 삭제',
        `"${item.code_name}" 그룹코드를 삭제하시겠습니까? 관련된 모든 상세코드도 함께 삭제됩니다.`,
        async () => {
          try {
            // 그룹코드 삭제 API 호출 - 환경별 기본 URL 사용
            await axios.delete(getApiUrl(`/api/codes/groups/${item.code_id}`));

            // 선택된 그룹코드가 삭제된 경우 선택 해제
            if (selectedParentCode.value && selectedParentCode.value.code_id === item.code_id) {
              selectedParentCode.value = null;
              childCodes.value = [];
            }

            // 그룹코드 목록 새로고침
            fetchParentCodes();
            showSnackbar('그룹코드가 삭제되었습니다.', 'success');
          } catch (error) {
            console.error('그룹코드 삭제 중 오류 발생:', error);
            showSnackbar('그룹코드 삭제에 실패했습니다.', 'error');
          }
          confirmDialog.value = false;
        }
      );
    };

    // 상세코드 슬라이드 패널 열기
    const openChildDrawer = (item: ChildCode | null, mode: 'add' | 'edit') => {
      if (!selectedParentCode.value) return;

      childDialogMode.value = mode;

      if (mode === 'edit' && item) {
        editedChildCode.value = { ...item };
      } else {
        editedChildCode.value = {
          parent_code_id: selectedParentCode.value.code_id,
          code_id: '',
          code_name: '',
          description: '',
          sort_order: childCodes.value.length + 1,
          use_yn: 'Y',
          icon: ''
        };
      }

      childDialog.value = true;
    };

    // 상세코드 슬라이드 패널 닫기
    const closeChildDialog = () => {
      childDialog.value = false;
    };

    // 상세코드 저장
    const saveChildCode = async () => {
      // 유효성 검사
      if (!editedChildCode.value.code_id || !editedChildCode.value.code_name) {
        showSnackbar('코드 ID와 코드명은 필수 입력 항목입니다.', 'error');
        return;
      }

      try {
        // 코드 ID를 대문자로 변환
        editedChildCode.value.code_id = editedChildCode.value.code_id.toUpperCase();

        // API 요청 데이터 형식에 맞게 변환
        const apiData = {
          id: editedChildCode.value.code_id,
          group_id: editedChildCode.value.parent_code_id,
          name: editedChildCode.value.code_name,
          value: editedChildCode.value.value || '',
          description: editedChildCode.value.description,
          sort_order: editedChildCode.value.sort_order.toString(),
          is_active: editedChildCode.value.use_yn === 'Y',
          icon: editedChildCode.value.icon || ''
        };

        if (childDialogMode.value === 'add') {
          // 상세코드 추가 API 호출 - 환경별 기본 URL 사용
          await axios.post(getApiUrl('/api/codes/details'), apiData);
          showSnackbar('상세코드가 추가되었습니다.', 'success');
        } else {
          // 상세코드 수정 API 호출 - 환경별 기본 URL 사용
          await axios.put(getApiUrl(`/api/codes/details/${editedChildCode.value.code_id}`), apiData);
          showSnackbar('상세코드가 수정되었습니다.', 'success');
        }

        // 상세코드 목록 새로고침
        if (selectedParentCode.value) {
          fetchChildCodes(selectedParentCode.value);
        }
        closeChildDialog();
      } catch (error) {
        console.error('상세코드 저장 중 오류 발생:', error);
        showSnackbar('상세코드 저장에 실패했습니다.', 'error');
      }
    };

    // 상세코드 삭제 (Vuetify 다이얼로그 사용)
    const deleteChildCode = async (item: ChildCode) => {
      showConfirmDialog(
        '상세코드 삭제',
        `"${item.code_name}" 상세코드를 삭제하시겠습니까?`,
        async () => {
          try {
            // 상세코드 삭제 API 호출 - 환경별 기본 URL 사용
            await axios.delete(getApiUrl(`/api/codes/details/${item.code_id}`));

            // 상세코드 목록 새로고침
            if (selectedParentCode.value) {
              fetchChildCodes(selectedParentCode.value);
            }
            showSnackbar('상세코드가 삭제되었습니다.', 'success');
          } catch (error) {
            console.error('상세코드 삭제 중 오류 발생:', error);
            showSnackbar('상세코드 삭제에 실패했습니다.', 'error');
          }
          confirmDialog.value = false;
        }
      );
    };

    // 확인 다이얼로그 상태 및 함수
    const confirmDialog = ref(false);
    const confirmTitle = ref('');
    const confirmMessage = ref('');
    const confirmAction = ref<() => Promise<void>>(() => Promise.resolve());

    const showConfirmDialog = (title: string, message: string, action: () => Promise<void>) => {
      confirmTitle.value = title;
      confirmMessage.value = message;
      confirmAction.value = action;
      confirmDialog.value = true;
    };

    // 스낵바 표시
    const showSnackbar = (text: string, color: 'success' | 'error' | 'info' = 'success') => {
      snackbarText.value = text;
      snackbarColor.value = color;
      snackbar.value = true;
    };

    // 컴포넌트 마운트 시 부모코드 목록 조회
    onMounted(() => {
      fetchParentCodes();
    });

    return {
      parentCodes,
      isParentLoading,
      parentSearch,
      selectedParentCode,
      childCodes,
      isChildLoading,
      parentDialog,
      childDialog,
      parentDialogMode,
      childDialogMode,
      editedParentCode,
      editedChildCode,
      snackbar,
      snackbarText,
      snackbarColor,
      parentHeaders,
      childHeaders,
      filteredParentCodes,
      parentDialogTitle,
      childDialogTitle,
      fetchParentCodes,
      fetchChildCodes,
      selectParentCode,
      openParentDrawer,
      closeParentDialog,
      saveParentCode,
      deleteParentCode,
      openChildDrawer,
      closeChildDialog,
      saveChildCode,
      deleteChildCode,
      showSnackbar,
      // 확인 다이얼로그 상태 및 함수 반환
      confirmDialog,
      confirmTitle,
      confirmMessage,
      confirmAction,
      showConfirmDialog,
    };
  }
});
</script>