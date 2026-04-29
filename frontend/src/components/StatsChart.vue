<template>
  <div class="stats-chart bg-slate-900/30 border border-slate-800/50 rounded-lg p-6">
    <!-- 空状态显示 -->
    <div v-if="!props.stats" class="flex flex-col items-center justify-center h-64 text-center py-12">
      <svg class="w-16 h-16 text-slate-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
      </svg>
      <h4 class="text-base font-light text-slate-400 mb-2">暂无数据</h4>
      <p class="text-sm text-slate-500">请确保后端服务已启动，或刷新页面重试</p>
    </div>

    <!-- 数据展示 -->
    <div v-else>
      <!-- 统计卡片网格 - 杂志风格简洁展示 -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div
          v-for="(stat, index) in statsData"
          :key="stat.key"
          class="bg-slate-900/50 border border-slate-800/30 rounded-lg p-4 hover:border-slate-700/50 transition-colors duration-300 animate-fadeInUp"
          :style="{ animationDelay: `${index * 0.08}s` }"
        >
          <div class="flex items-center justify-between mb-3">
            <span class="text-[10px] font-light text-slate-500 tracking-wider uppercase">{{ stat.label }}</span>
          </div>
          <div class="text-2xl font-light text-slate-100">
            {{ stat.value }}
          </div>
          <!-- 简洁的进度条 -->
          <div class="mt-3 h-px bg-slate-800/50">
            <div
              class="h-px bg-amber-500/60 transition-all duration-1000"
              :style="{ width: `${stat.progress}%` }"
            ></div>
          </div>
        </div>
      </div>

      <!-- 语言分布 + 四宫格布局 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 语言分布 - 左侧 -->
        <div class="lg:col-span-1">
          <h4 class="text-sm font-light text-slate-400 mb-4 tracking-wide">编程语言分布</h4>
          <div v-if="top5LanguageData.length > 0" class="space-y-3">
            <div
              v-for="(lang, index) in top5LanguageData"
              :key="lang.name"
              class="flex items-center gap-3"
            >
              <div class="w-16 text-xs text-slate-500 font-light">{{ lang.name }}</div>
              <div class="flex-1 h-1.5 bg-slate-800/50 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full bg-slate-400/60"
                  :style="{ width: lang.percentage + '%' }"
                ></div>
              </div>
              <div class="w-10 text-xs text-slate-400 text-right font-light">{{ lang.percentage }}%</div>
            </div>
          </div>
          <div v-else class="py-8 text-center text-xs text-slate-500">暂无数据</div>
        </div>

        <!-- 四宫格布局 - 右侧 -->
        <div class="lg:col-span-2 grid grid-cols-2 gap-4">
          <!-- 项目趋势 -->
          <div class="bg-slate-900/30 border border-slate-800/30 rounded-lg p-4">
            <h4 class="text-xs font-light text-slate-400 mb-3 tracking-wide">项目趋势</h4>
            <div v-if="trendData.length > 0" class="space-y-2">
              <div v-for="trend in trendData" :key="trend.label" class="flex items-center justify-between py-1.5">
                <span class="text-sm text-slate-300 font-light">{{ trend.label }}</span>
                <span :class="trend.change > 0 ? 'text-amber-400' : 'text-slate-500'" class="text-xs font-light">
                  {{ trend.change > 0 ? '+' : '' }}{{ trend.change }}%
                </span>
              </div>
            </div>
            <div v-else class="py-4 text-center text-xs text-slate-500">暂无数据</div>
          </div>

          <!-- 活跃度分析 -->
          <div class="bg-slate-900/30 border border-slate-800/30 rounded-lg p-4">
            <h4 class="text-xs font-light text-slate-400 mb-3 tracking-wide">活跃度分析</h4>
            <div class="grid grid-cols-3 gap-2">
              <div class="text-center py-2">
                <div class="text-lg font-light text-slate-200">{{ activityBreakdown?.recentlyActive ?? '-' }}</div>
                <div class="text-[10px] text-slate-500 mt-1">活跃</div>
              </div>
              <div class="text-center py-2 border-l border-slate-800/30">
                <div class="text-lg font-light text-slate-200">{{ activityBreakdown?.stable ?? '-' }}</div>
                <div class="text-[10px] text-slate-500 mt-1">稳定</div>
              </div>
              <div class="text-center py-2 border-l border-slate-800/30">
                <div class="text-lg font-light text-slate-200">{{ activityBreakdown?.needsAttention ?? '-' }}</div>
                <div class="text-[10px] text-slate-500 mt-1">需关注</div>
              </div>
            </div>
          </div>

          <!-- 新兴技术领域 -->
          <div class="bg-slate-900/30 border border-slate-800/30 rounded-lg p-4">
            <h4 class="text-xs font-light text-slate-400 mb-3 tracking-wide">新兴技术</h4>
            <div v-if="props.emergingAreas && props.emergingAreas.length > 0" class="space-y-2">
              <div v-for="area in props.emergingAreas" :key="area.name" class="flex items-center justify-between py-1">
                <span class="text-sm text-slate-300 font-light">{{ area.name }}</span>
                <span class="text-xs text-amber-400 font-light">+{{ area.growth }}%</span>
              </div>
            </div>
            <div v-else class="py-4 text-center text-xs text-slate-500">暂无数据</div>
          </div>

          <!-- 上升最快项目 -->
          <div class="bg-slate-900/30 border border-slate-800/30 rounded-lg p-4">
            <h4 class="text-xs font-light text-slate-400 mb-3 tracking-wide">上升最快</h4>
            <div v-if="props.surgingProjects && props.surgingProjects.length > 0" class="space-y-2">
              <div v-for="project in props.surgingProjects" :key="project.name" class="flex items-center gap-2 py-1">
                <span class="text-xs text-slate-500 w-4">{{ project.rank }}</span>
                <span class="text-sm text-slate-300 font-light truncate flex-1">{{ project.name.split('/')[1] || project.name }}</span>
                <span class="text-xs text-amber-400 font-light">+{{ project.star_increase }}</span>
              </div>
            </div>
            <div v-else class="py-4 text-center text-xs text-slate-500">暂无数据</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import type { Stats, LanguageData, TrendDataItem } from '../api/reports'
import { reportApi } from '../api/reports'

// Props
const props = defineProps<{
  stats?: Stats | null
  emergingAreas?: { name: string; growth: number; bgClass: string; icon: any }[]
  surgingProjects?: { name: string; description: string; star_increase: number; language?: string; rank: number }[]
}>()

// Icons
const BarChartIcon = {
  template: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
  </svg>`
}

const CubeIcon = {
  template: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
  </svg>`
}

const CodeIcon = {
  template: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
  </svg>`
}

// 计算属性：格式化统计数据
const statsData = computed(() => {
  if (!props.stats) {
    return []
  }
  
  return [
    {
      key: 'totalReports',
      label: '总报告数',
      value: Math.round(props.stats.totalReports || 0).toLocaleString(),
      icon: BarChartIcon,
      bgClass: 'bg-gradient-to-br from-blue-500 to-blue-600',
      badgeClass: 'bg-blue-500/20 text-blue-400',
      progressClass: 'bg-gradient-to-r from-blue-500 to-blue-600',
      change: '',
      progress: Math.min(100, ((props.stats.totalReports || 0) / 1000) * 100)
    },
    {
      key: 'totalProjects',
      label: '总项目数',
      value: Math.round(props.stats.totalProjects || 0).toLocaleString(),
      icon: CubeIcon,
      bgClass: 'bg-gradient-to-br from-purple-500 to-purple-600',
      badgeClass: 'bg-purple-500/20 text-purple-400',
      progressClass: 'bg-gradient-to-r from-purple-500 to-purple-600',
      change: '',
      progress: Math.min(100, ((props.stats.totalProjects || 0) / 500) * 100)
    },
    {
      key: 'weeklyNew',
      label: '本周新增',
      value: Math.round(props.stats.weeklyNew || 0).toLocaleString(),
      icon: BarChartIcon,
      bgClass: 'bg-gradient-to-br from-green-500 to-green-600',
      badgeClass: 'bg-green-500/20 text-green-400',
      progressClass: 'bg-gradient-to-r from-green-500 to-green-600',
      change: '',
      progress: Math.min(100, ((props.stats.weeklyNew || 0) / 50) * 100)
    },
    {
      key: 'avgContributors',
      label: '平均贡献者',
      value: Math.round(props.stats.avgContributors || 0).toLocaleString(),
      icon: CodeIcon,
      bgClass: 'bg-gradient-to-br from-orange-500 to-orange-600',
      badgeClass: 'bg-orange-500/20 text-orange-400',
      progressClass: 'bg-gradient-to-r from-orange-500 to-orange-600',
      change: '',
      progress: Math.min(100, ((props.stats.avgContributors || 0) / 200) * 100)
    }
  ]
})

// 响应式数据
const languageData = ref<LanguageData[]>([])

// 计算属性：只显示前5个编程语言
const top5LanguageData = computed(() => {
  return languageData.value.slice(0, 5)
})
const trendData = ref<TrendDataItem[]>([])
const activityScore = ref<number | null>(null)

// 从后端获取数据的方法
const fetchLanguageDistribution = async () => {
  try {
    const data = await reportApi.getLanguageDistribution()
    languageData.value = data
  } catch (error) {
    console.error('获取语言分布数据失败:', error)
  }
}

const fetchTrendData = async () => {
  try {
    const data = await reportApi.getTrendData()
    trendData.value = data
  } catch (error) {
    console.error('获取趋势数据失败:', error)
  }
}

// 生命周期
onMounted(() => {
  // 只有在有数据时才进行处理
  if (props.stats) {
    // 使用从后端获取的真实活跃度数据
    if (props.stats.activityScore !== undefined) {
      activityScore.value = props.stats.activityScore
    }
    
    // 获取语言分布和趋势数据
    fetchLanguageDistribution()
    fetchTrendData()
  }
})

// 监听stats变化，更新活跃度数据
watch(() => props.stats, (newValue, oldValue) => {
  if (newValue && newValue.activityScore !== undefined) {
    activityScore.value = newValue.activityScore
  }
  
  // 当stats变为有数据时，重新获取语言分布和趋势数据
  if (newValue && !oldValue) {
    fetchLanguageDistribution()
    fetchTrendData()
  }
  
  // 当stats变为null时，清空相关数据
  if (!newValue) {
    languageData.value = []
    trendData.value = []
    activityScore.value = null
  }
})
</script>