<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card elevation="3" rounded="lg" class="mb-4">
          <v-toolbar flat color="primary" dark class="rounded-t-lg">
            <v-icon class="me-2">mdi-card-bulleted</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">카드사용내역 조회</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>

          <v-card-text class="pa-4">
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="selectedCardCompany"
                  :items="cardCompanies"
                  label="카드사 선택"
                  variant="outlined"
                  density="comfortable"
                  class="mb-4"
                  hide-details
                ></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-file-input
                  v-model="excelFile"
                  label="엑셀 파일 업로드"
                  accept=".xlsx, .xls"
                  variant="outlined"
                  density="comfortable"
                  prepend-icon="mdi-file-excel"
                  :disabled="!selectedCardCompany"
                  hide-details
                  class="mb-4"
                  @change="handleFileUpload"
                ></v-file-input>
              </v-col>
            </v-row>

            <v-divider class="my-4"></v-divider>

            <v-alert v-if="uploadSuccess" type="success" variant="tonal" closable class="mb-4">
              {{ uploadSuccessMessage }}
            </v-alert>

            <v-alert v-if="uploadError" type="error" variant="tonal" closable class="mb-4">
              {{ uploadErrorMessage }}
            </v-alert>

            <v-btn
              color="primary"
              variant="elevated"
              class="mb-4"
              :disabled="!excelFile"
              @click="processExcelFile"
              :loading="isLoading"
            >
              <v-icon start>mdi-upload</v-icon>
              파일 처리
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card elevation="3" rounded="lg">
          <v-toolbar flat :color="getCardColor(selectedCardCompany)" dark class="rounded-t-lg">
            <v-icon class="me-2">{{ getCardIcon(selectedCardCompany) }}</v-icon>
            <v-toolbar-title class="text-h6 font-weight-medium">
              {{ selectedCardCompany || '카드사' }} 사용내역
              <span v-if="cardTransactions.length > 0" class="text-subtitle-2 ms-2">
                (총 {{ cardTransactions.length }}건)
              </span>
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="검색"
              single-line
              hide-details
              density="compact"
              bg-color="rgba(255, 255, 255, 0.15)"
              class="max-width-200"
              style="max-width: 200px"
            ></v-text-field>
          </v-toolbar>

          <v-card-text class="pa-4">
            <div class="d-flex align-center mb-3">
              <v-icon color="primary" size="small" class="mr-2">mdi-information-outline</v-icon>
              <span class="text-subtitle-2 font-weight-medium">총 {{ cardTransactions.length }}건의 카드사용내역</span>
              <v-spacer></v-spacer>
            </div>

            <v-divider class="mb-3"></v-divider>
            
            <v-data-table
              name="cardTable"
              :headers="headers"
              :items="cardTransactions"
              :search="search"
              :loading="isLoading"
              :items-per-page="-1"
              hide-default-footer
              class="rounded-lg"
              item-key="id"
              hover
            >
              <template #headers>
                <tr>
                  <th v-for="header in headers" :key="header.key" class="text-primary font-weight-bold">
                    {{ header.title }}
                  </th>
                </tr>
              </template>
              <template #item="{ item }">
                <tr>
                  <td>{{ formatDate(item.date) }}</td>
                  <td>{{ item.cardName }}</td>
                  <td>{{ item.merchant }}</td>
                  <td class="text-end">{{ formatCurrency(item.amount) }}</td>
                </tr>
              </template>
              <template v-slot:no-data>
                <div class="text-center pa-5">
                  <v-icon size="x-large" color="grey-lighten-1" class="mb-3">mdi-credit-card-off</v-icon>
                  <div class="text-subtitle-1 text-grey">
                    {{ selectedCardCompany ? '조회된 카드 사용내역이 없습니다.' : '카드사를 선택하고 엑셀 파일을 업로드해주세요.' }}
                  </div>
                </div>
              </template>
              <template #bottom>
                <div class="pa-2 d-flex align-center">
                  <span class="text-caption text-grey-darken-1">
                    * 카드사용내역은 엑셀 파일 업로드 후 조회할 수 있습니다.
                  </span>
                </div>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'CardPage',
  setup() {
    // 카드사 목록
    const cardCompanies = [
      '신한카드',
      '롯데카드',
      '삼성카드',
    ];

    const selectedCardCompany = ref('');
    const excelFile = ref(null);
    const isLoading = ref(false);
    const search = ref('');
    const uploadSuccess = ref(false);
    const uploadError = ref(false);
    const uploadSuccessMessage = ref('');
    const uploadErrorMessage = ref('');

    // 테이블 헤더 정의
    const headers = [
      { title: '이용일자', key: 'date', align: 'start' as const, sortable: true },
      { title: '이용카드', key: 'cardName', align: 'start' as const, sortable: true },
      { title: '가맹점', key: 'merchant', align: 'start' as const, sortable: true },
      { title: '사용금액', key: 'amount', align: 'end' as const, sortable: true },
    ];

    // 카드 거래 내역 샘플 데이터
    const cardTransactions = ref([
      {
        date: '2025-04-25',
        cardName: '신한 플래티넘',
        merchant: '스타벅스 강남점',
        amount: 5800
      },
      {
        date: '2025-04-23',
        cardName: '신한 플래티넘',
        merchant: '이마트 용산점',
        amount: 67500
      },
      {
        date: '2025-04-20',
        cardName: '롯데 시그니처',
        merchant: 'CGV 왕십리점',
        amount: 28000
      },
      {
        date: '2025-04-18',
        cardName: '삼성 페이',
        merchant: '교보문고',
        amount: 32400
      },
      {
        date: '2025-04-15',
        cardName: '삼성 페이',
        merchant: '쿠팡',
        amount: 45600
      },
    ]);

    // 파일 업로드 처리
    const handleFileUpload = (file: File | null) => {
      if (file) {
        uploadSuccess.value = false;
        uploadError.value = false;
      }
    };

    // 엑셀 파일 처리 (실제로는 백엔드 API를 호출하여 처리)
    const processExcelFile = () => {
      isLoading.value = true;
      
      // 실제 구현에서는 API 호출 코드가 들어갑니다
      setTimeout(() => {
        isLoading.value = false;
        uploadSuccess.value = true;
        uploadSuccessMessage.value = `${selectedCardCompany.value} 엑셀 파일이 성공적으로 처리되었습니다.`;
        
        // 실제 구현에서는 API 응답으로 받은 데이터를 표시합니다
        // 여기서는 샘플 데이터를 필터링하여 표시
        if (selectedCardCompany.value === '신한카드') {
          cardTransactions.value = cardTransactions.value.filter(tx => tx.cardName.includes('신한'));
        } else if (selectedCardCompany.value === '롯데카드') {
          cardTransactions.value = cardTransactions.value.filter(tx => tx.cardName.includes('롯데'));
        } else if (selectedCardCompany.value === '삼성카드') {
          cardTransactions.value = cardTransactions.value.filter(tx => tx.cardName.includes('삼성'));
        }
      }, 1500);
    };

    // 날짜 포맷 함수
    const formatDate = (dateString: string) => {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    };

    // 금액 포맷 함수
    const formatCurrency = (amount: number) => {
      return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(amount);
    };

    // 카드사별 색상 반환
    const getCardColor = (company: string) => {
      switch (company) {
        case '신한카드': return 'blue-darken-3';
        case '롯데카드': return 'red-darken-2';
        case '삼성카드': return 'blue-darken-4';
        default: return 'primary';
      }
    };

    // 카드사별 아이콘 반환
    const getCardIcon = (company: string) => {
      switch (company) {
        case '신한카드': return 'mdi-credit-card-outline';
        case '롯데카드': return 'mdi-credit-card-multiple';
        case '삼성카드': return 'mdi-credit-card-chip';
        default: return 'mdi-credit-card';
      }
    };

    return {
      cardCompanies,
      selectedCardCompany,
      excelFile,
      isLoading,
      search,
      headers,
      cardTransactions,
      uploadSuccess,
      uploadError,
      uploadSuccessMessage,
      uploadErrorMessage,
      handleFileUpload,
      processExcelFile,
      formatDate,
      formatCurrency,
      getCardColor,
      getCardIcon
    };
  }
});
</script>

<style scoped>
.max-width-200 {
  max-width: 200px;
}
</style>