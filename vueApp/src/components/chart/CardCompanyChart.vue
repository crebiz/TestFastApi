<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup lang="ts">
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

// Chart.js가 기대하는 데이터 형식으로 타입 정의
interface ChartDataset {
  label: string;
  backgroundColor: string;
  borderColor: string;
  borderWidth: number;
  data: number[];
  yAxisID: string;
}

interface CardCompanyChartData {
  labels: string[];
  datasets: ChartDataset[];
}

defineProps({
  chartData: {
    type: Object as () => CardCompanyChartData,
    required: true
  }
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      type: 'linear' as const,
      display: true,
      position: 'left' as const,
      title: {
        display: true,
        text: '금액(만원)'
      }
    },
    y1: {
      type: 'linear' as const,
      display: true,
      position: 'right' as const,
      grid: {
        drawOnChartArea: false
      },
      title: {
        display: true,
        text: '건수'
      }
    }
  },
  plugins: {
    legend: {
      display: true,
      position: 'top' as const
    },
    title: {
      display: true,
      text: '카드사별 사용금액 및 건수'
    },
    tooltip: {
      callbacks: {
        label: function (context: any) {
          let label = context.dataset.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed.y !== null) {
            if (label.includes('금액')) {
              label += new Intl.NumberFormat('ko-KR').format(context.parsed.y) + '만원';
            } else {
              label += new Intl.NumberFormat('ko-KR').format(context.parsed.y) + '건';
            }
          }
          return label;
        }
      }
    }
  }
};
</script>
