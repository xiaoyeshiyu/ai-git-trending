<template>
  <div class="stats-chart">
    <!-- 空状态显示 -->
    <div v-if="!props.stats" class="flex flex-col items-center justify-center h-64 text-center py-12">
      <svg class="w-16 h-16 text-slate-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
      </svg>
      <h4 class="text-base font-light text-slate-600 mb-2">暂无数据</h4>
      <p class="text-sm text-slate-500">请确保后端服务已启动，或刷新页面重试</p>
    </div>

    <!-- 数据展示 -->
    <div v-else class="space-y-5">
      <!-- 统计卡片网格 -->
      <div class="grid grid-cols-2 xl:grid-cols-4 gap-3">
        <div
          v-for="(stat, index) in statsData"
          :key="stat.key"
          class="rounded-xl border border-cyan-100 bg-gradient-to-br from-white to-cyan-50/60 p-4 shadow-sm transition-all duration-300 hover:-translate-y-0.5 hover:border-cyan-300/70 hover:shadow-md animate-fadeInUp"
          :style="{ animationDelay: `${index * 0.08}s` }"
        >
          <div>
            <span class="text-[10px] font-light text-cyan-700/75 tracking-wider uppercase">{{ stat.label }}</span>
            <div class="mt-3 text-3xl font-light text-slate-900">
              {{ stat.value }}
            </div>
          </div>
          <div class="mt-4 h-1 rounded-full bg-cyan-100 overflow-hidden">
            <div
              class="h-full rounded-full bg-gradient-to-r from-cyan-400 to-sky-500 transition-all duration-1000"
              :style="{ width: `${stat.progress}%` }"
            ></div>
          </div>
        </div>
      </div>

      <!-- 数据面板 -->
      <div class="grid grid-cols-1 xl:grid-cols-12 gap-4">
        <section class="xl:col-span-5 rounded-xl border border-cyan-100 bg-white/95 p-5 shadow-sm">
          <div class="flex items-center justify-between mb-5">
            <h4 class="text-sm font-light text-slate-700 tracking-wide">编程语言分布</h4>
            <span class="text-[10px] text-cyan-700/70 tracking-wider uppercase">Top 5</span>
          </div>
          <div v-if="top5LanguageData.length > 0" class="space-y-4">
            <div
              v-for="(lang, index) in top5LanguageData"
              :key="lang.name"
              class="flex items-center gap-3"
            >
              <div class="flex h-6 w-6 shrink-0 items-center justify-center rounded-md border border-cyan-100 bg-cyan-50 text-[10px] text-cyan-700">
                {{ index + 1 }}
              </div>
              <div class="w-24 truncate text-sm text-slate-700 font-light">{{ lang.name }}</div>
              <div class="flex-1 h-2 bg-cyan-100 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full bg-gradient-to-r from-cyan-400 to-sky-500"
                  :style="{ width: lang.percentage + '%' }"
                ></div>
              </div>
              <div class="w-12 text-xs text-slate-600 text-right font-light">{{ lang.percentage }}%</div>
            </div>
          </div>
          <div v-else class="empty-panel">暂无语言数据</div>
        </section>

        <section class="xl:col-span-7 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="rounded-xl border border-cyan-100 bg-white/95 p-5 shadow-sm">
            <h4 class="text-sm font-light text-slate-700 mb-4 tracking-wide">项目趋势</h4>
            <div v-if="trendData.length > 0" class="space-y-3">
              <div v-for="trend in trendData.slice(0, 4)" :key="trend.label">
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-sm text-slate-700 font-light">{{ trend.label }}</span>
                  <span :class="trend.change > 0 ? 'text-emerald-600' : trend.change < 0 ? 'text-rose-500' : 'text-slate-500'" class="text-xs font-light">
                    {{ trend.change > 0 ? '+' : '' }}{{ trend.change }}%
                  </span>
                </div>
                <div class="h-1.5 rounded-full bg-cyan-100 overflow-hidden">
                  <div
                    class="h-full rounded-full bg-gradient-to-r from-cyan-400 to-emerald-400"
                    :style="{ width: `${projectTrendWidth(trend.value)}%` }"
                  ></div>
                </div>
              </div>
            </div>
            <div v-else class="empty-panel">暂无趋势数据</div>
          </div>

          <div class="rounded-xl border border-cyan-100 bg-white/95 p-5 shadow-sm">
            <h4 class="text-sm font-light text-slate-700 mb-4 tracking-wide">活跃度分析</h4>
            <div class="grid grid-cols-3 overflow-hidden rounded-xl border border-cyan-100 bg-gradient-to-r from-cyan-50 to-sky-50">
              <div class="text-center px-3 py-4">
                <div class="text-2xl font-light text-slate-900">{{ activityBreakdown?.recentlyActive ?? '-' }}</div>
                <div class="text-[10px] text-cyan-700/70 mt-2">活跃</div>
              </div>
              <div class="text-center px-3 py-4 border-l border-cyan-100">
                <div class="text-2xl font-light text-slate-900">{{ activityBreakdown?.stable ?? '-' }}</div>
                <div class="text-[10px] text-cyan-700/70 mt-2">稳定</div>
              </div>
              <div class="text-center px-3 py-4 border-l border-cyan-100">
                <div class="text-2xl font-light text-slate-900">{{ activityBreakdown?.needsAttention ?? '-' }}</div>
                <div class="text-[10px] text-cyan-700/70 mt-2">需关注</div>
              </div>
            </div>
          </div>

          <div class="rounded-xl border border-cyan-100 bg-white/95 p-5 shadow-sm">
            <h4 class="text-sm font-light text-slate-700 mb-4 tracking-wide">新兴技术</h4>
            <div v-if="props.emergingAreas && props.emergingAreas.length > 0" class="flex flex-wrap gap-2">
              <div v-for="area in props.emergingAreas.slice(0, 4)" :key="area.name" class="rounded-lg border border-cyan-100 bg-gradient-to-br from-cyan-50 to-white px-3 py-2">
                <div class="text-sm text-slate-700 font-light">{{ area.name }}</div>
                <div class="mt-1 text-xs text-emerald-600 font-light">+{{ area.growth }}%</div>
              </div>
            </div>
            <div v-else class="empty-panel">暂无技术领域数据</div>
          </div>

          <div class="rounded-xl border border-cyan-100 bg-white/95 p-5 shadow-sm">
            <div class="flex items-center justify-between gap-3 mb-4">
              <h4 class="text-sm font-light text-slate-700 tracking-wide">
                {{ props.surgingMode === 'hot' ? '今日高热项目' : '上升最快' }}
              </h4>
              <span v-if="props.surgingMode === 'hot'" class="text-[10px] text-cyan-700/70">历史不足</span>
            </div>
            <div v-if="props.surgingProjects && props.surgingProjects.length > 0" class="space-y-2">
              <div v-for="project in props.surgingProjects" :key="project.name" class="flex items-center gap-2 py-1">
                <span class="text-xs text-cyan-700/70 w-4">{{ project.rank }}</span>
                <span class="text-sm text-slate-700 font-light truncate flex-1">{{ project.name.split('/')[1] || project.name }}</span>
                <span class="text-xs text-cyan-700 font-light">
                  {{ props.surgingMode === 'hot' ? formatCompactNumber(project.star_increase) : `+${project.star_increase}` }}
                </span>
              </div>
            </div>
            <div v-else class="empty-panel">
              需要连续多日快照后计算
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Stats, LanguageData, TrendDataItem } from '../api/reports'

// Props
const props = defineProps<{
  stats?: Stats | null
  languageData?: LanguageData[]
  trendData?: TrendDataItem[]
  emergingAreas?: { name: string; growth: number; bgClass: string; icon: any }[]
  surgingProjects?: { name: string; description: string; star_increase: number; language?: string; rank: number }[]
  surgingMode?: 'surging' | 'hot'
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

// 计算属性：只显示前5个编程语言
const top5LanguageData = computed(() => {
  return (props.languageData ?? []).slice(0, 5)
})

const trendData = computed(() => props.trendData ?? [])
const maxTrendValue = computed(() => {
  const values = trendData.value.map((item) => item.value || 0)
  return values.length ? Math.max(...values, 0) : 0
})

const activityBreakdown = computed(() => {
  return props.stats?.activityBreakdown ?? {
    recentlyActive: props.stats?.weeklyNew ?? 0,
    stable: Math.max((props.stats?.totalProjects ?? 0) - (props.stats?.weeklyNew ?? 0), 0),
    needsAttention: 0
  }
})

const formatCompactNumber = (value: number) => {
  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M★`
  if (value >= 1000) return `${(value / 1000).toFixed(1)}K★`
  return `${value}★`
}

const projectTrendWidth = (value: number) => {
  const max = maxTrendValue.value
  if (max <= 0) return 0
  return Math.max(12, Math.round((value / max) * 100))
}
</script>

<style scoped>
.empty-panel {
  display: flex;
  min-height: 6rem;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  border: 1px dashed rgba(125, 211, 252, 0.9);
  background: linear-gradient(135deg, rgba(236, 254, 255, 0.8), rgba(255, 255, 255, 0.9));
  padding: 1rem;
  text-align: center;
  font-size: 0.75rem;
  font-weight: 300;
  color: rgb(71, 85, 105);
}
</style>
