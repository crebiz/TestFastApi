<template>
  <v-list-group v-if="node.children">
    <template #activator="{ props }">
      <v-list-item v-bind="props" :class="getItemClass(node)">
        <template #prepend>
          <v-avatar class="budget-icon" :color="node.color || getDefaultColor(node)" rounded>
            <v-icon :color="node.iconColor || 'white'">{{ node.icon || getDefaultIcon(node) }}</v-icon>
          </v-avatar>
        </template>
        <v-list-item-title :class="{ 'font-weight-bold': isTopLevel(node) }">{{ node.name }}</v-list-item-title>
        <template #append>
          <div class="text-right font-weight-medium">{{ formatCurrency(calculateNodeTotal(node)) + '원' }}</div>
        </template>
      </v-list-item>
    </template>
    <BudgetTreeItem v-for="child in node.children" :key="child.id" :node="child" />
  </v-list-group>
  <v-list-item v-else :class="getItemClass(node)">
    <v-list-item-title>{{ node.name }}</v-list-item-title>
    <template #append>
      <div class="text-right font-weight-medium" v-if="node.fund">{{ formatCurrency(parseInt(node.fund) || 0) + '원' }}</div>
    </template>
  </v-list-item>
</template>

<script lang="ts" setup>
defineProps<{ node: any }>();

// 노드가 최상위 레벨인지 확인 (대분류)
function isTopLevel(node: any): boolean {
  // ID가 한 단어로만 구성된 경우 최상위 레벨로 간주
  return !node.id.includes('_');
}

// 중간 레벨인지 확인 (중분류)
function isMiddleLevel(node: any): boolean {
  // ID에 언더스코어가 하나만 있는 경우 중간 레벨로 간주
  return node.id.split('_').length === 2;
}

// 노드의 총 금액 계산 (하위 노드의 fund 값을 모두 합산)
function calculateNodeTotal(node: any): number {
  let total = 0;
  
  // 현재 노드에 fund 값이 있는 경우 합산
  if (node.fund) {
    total += parseInt(node.fund, 10) || 0;
  }
  
  // 하위 노드가 있는 경우 그 값들도 합산
  if (node.children) {
    node.children.forEach((child: any) => {
      if (child.fund) {
        total += parseInt(child.fund, 10) || 0;
      }
      
      // 그 하위 노드들도 재귀적으로 합산
      if (child.children) {
        child.children.forEach((grandChild: any) => {
          total += calculateNodeTotal(grandChild);
        });
      }
    });
  }
  
  return total;
}

// 노드 레벨에 따른 클래스 반환
function getItemClass(node: any): string {
  if (isTopLevel(node)) {
    return 'top-level-item';
  } else if (isMiddleLevel(node)) {
    return 'middle-level-item';
  }
  return 'sub-level-item';
}

// 노드 레벨에 따른 기본 아이콘 반환
function getDefaultIcon(node: any): string {
  if (isTopLevel(node)) {
    return 'mdi-folder-outline';
  } else if (isMiddleLevel(node)) {
    return 'mdi-folder-open-outline';
  } else {
    return 'mdi-file-document-outline';
  }
}

// 기본 색상 반환
function getDefaultColor(node: any): string {
  if (isTopLevel(node)) {
    return '#E6F9FF';
  } else if (isMiddleLevel(node)) {
    return '#F0F0F0';
  }
  return '#E0E0E0';
}

// 금액에 철 단위 콤마 추가
function formatCurrency(value: string | number): string {
  const num = typeof value === 'string' ? parseInt(value, 10) : value;
  return num.toLocaleString('ko-KR');
}
</script>

<style scoped>
.top-level-item {
  background-color: rgba(0, 0, 0, 0.03);
}

.middle-level-item {
  background-color: rgba(0, 0, 0, 0.01);
  margin-left: 8px;
}

.sub-level-item {
  margin-left: 16px;
  background-color: rgba(0, 0, 0, 0.005);
}

.budget-icon {
  margin-right: 8px;
}
</style>