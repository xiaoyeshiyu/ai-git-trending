<template>
  <div class="home-container min-h-screen bg-[#dff2f8] text-slate-900">
    <!-- 顶部导航栏 - 技术情报终端 -->
    <header class="sticky top-0 z-40 border-b border-cyan-400/20 bg-[#0e6685] backdrop-blur-sm">
      <div class="mx-auto flex max-w-[1500px] items-center justify-between px-4 py-3 lg:px-6">
        <div class="flex items-center gap-3">
          <div class="flex h-9 w-9 items-center justify-center border border-cyan-400/30 bg-cyan-400/10 text-cyan-300">
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
          </div>
          <div>
            <h1 class="text-sm font-semibold tracking-[0.28em] text-slate-100">GITTREND INTEL</h1>
            <p class="text-[10px] uppercase tracking-[0.26em] text-cyan-400/70">技术情报终端</p>
          </div>
        </div>

        <nav class="hidden items-center gap-1 md:flex">
          <router-link to="/" class="terminal-nav active">情报台</router-link>
          <router-link to="/trend" class="terminal-nav">趋势</router-link>
          <router-link to="/rankings" class="terminal-nav">排行榜</router-link>
          <router-link to="/trend-analysis" class="terminal-nav">趋势图谱</router-link>        </nav>
      </div>
    </header>

    <!-- 情报终端首屏 -->
    <section class="terminal-shell border-b border-cyan-400/15">
      <div class="mx-auto max-w-[1500px] px-4 py-5 lg:px-6">
        <div class="terminal-panel overflow-hidden">
          <div class="terminal-panel-head">
            <span>今日热榜与 AI 分析</span>
            <span>{{ todayTrendingUpdatedAt ? `更新于 ${formatDateTime(todayTrendingUpdatedAt)}` : '实时' }}</span>
          </div>
          <div class="p-5 lg:p-6">
            <div class="mb-5 flex flex-wrap items-center gap-2">
              <span class="status-chip online">后端在线</span>
              <span class="status-chip">GitHub Trending</span>
              <span class="status-chip">LLM Analysis</span>
            </div>

            <div class="mb-8 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <h2 class="max-w-4xl text-3xl font-semibold leading-tight text-slate-900 md:text-5xl">
                  今日热榜
                </h2>
                <p class="mt-4 max-w-3xl text-sm leading-7 text-slate-700 md:text-base">
                  首页直接展开今日 Trending 项目，并填充已生成的 AI 分析内容，方便快速扫描和深入查看。
                </p>
              </div>
              <div class="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:min-w-[520px]">
                <div class="terminal-metric">
                  <span>今日项目</span>
                  <strong>{{ todayTrendingList.length }}</strong>
                </div>
                <div class="terminal-metric">
                  <span>已分析</span>
                  <strong>{{ analyzedTrendingCount }}</strong>
                </div>
                <div class="terminal-metric">
                  <span>报告数</span>
                  <strong>{{ statsData.totalReports }}</strong>
                </div>
                <div class="terminal-metric">
                  <span>本周新增</span>
                  <strong>{{ statsData.weeklyNew }}</strong>
                </div>
              </div>
            </div>

            <div v-if="todayTrendingList.length > 0" class="grid grid-cols-1 gap-4 xl:grid-cols-2">
              <article
                v-for="(repo, i) in todayTrendingList"
                :key="repo.name"
                class="cursor-pointer rounded-2xl border border-cyan-100 bg-gradient-to-br from-white to-cyan-50/70 p-5 shadow-sm transition-all hover:-translate-y-1 hover:border-cyan-300 hover:shadow-lg hover:shadow-cyan-100/70"
                @click="openProjectModal(repo)"
              >
                <div class="flex items-start justify-between gap-4">
                  <div class="min-w-0 flex-1">
                    <div class="mb-2 flex items-center gap-2">
                      <span class="inline-flex h-7 min-w-7 items-center justify-center rounded-full bg-cyan-600 px-2 text-xs font-semibold text-white">
                        {{ i + 1 }}
                      </span>
                      <span class="text-[11px] uppercase tracking-[0.22em] text-cyan-700/70">
                        {{ repo.name.split('/')[0] }}
                      </span>
                    </div>
                    <h3 class="text-xl font-semibold text-slate-900">
                      {{ repo.name.split('/')[1] || repo.name }}
                    </h3>
                    <p class="mt-2 text-sm leading-6 text-slate-600">
                      {{ repo.description || '暂无项目描述' }}
                    </p>
                  </div>
                  <div class="shrink-0 text-right">
                    <div class="text-sm font-semibold text-cyan-700">★ {{ formatStars(repo.stars || 0) }}</div>
                    <div class="mt-1 text-xs text-slate-500">{{ repo.language || '未知语言' }}</div>
                  </div>
                </div>

                <div class="mt-4 flex flex-wrap items-center gap-2 text-xs text-slate-500">
                  <span class="rounded-full border border-cyan-100 bg-cyan-50 px-2.5 py-1">Forks {{ formatStars(repo.forks || 0) }}</span>
                  <span class="rounded-full border border-cyan-100 bg-cyan-50 px-2.5 py-1">Contributors {{ formatStars(repo.contributor_count || 0) }}</span>
                  <span
                    :class="repo.analysis ? 'border-emerald-200 bg-emerald-50 text-emerald-700' : 'border-amber-200 bg-amber-50 text-amber-700'"
                    class="rounded-full px-2.5 py-1"
                  >
                    {{ repo.analysis ? '已生成 AI 分析' : '待分析' }}
                  </span>
                </div>

                <div v-if="repo.analysisLoading" class="mt-4 flex items-center gap-3 rounded-xl border border-cyan-100 bg-cyan-50/50 px-4 py-3 text-sm text-slate-500">
                  <div class="spinner !h-5 !w-5"></div>
                  正在加载 AI 分析...
                </div>
                <template v-else-if="repo.renderedAnalysis">
                  <div class="mt-4 border-l-4 border-cyan-400 pl-4">
                    <p class="text-sm leading-7 text-slate-700">
                      {{ repo.analysisPreview || '该项目已生成 AI 分析，点击卡片查看完整内容。' }}
                    </p>
                  </div>
                </template>
                <div v-else class="mt-4 rounded-xl border border-dashed border-amber-200 bg-amber-50/70 px-4 py-3">
                  <p class="mb-1 text-sm font-medium text-amber-800">待分析</p>
                  <p class="text-sm leading-6 text-amber-700/80">
                    当前项目还没有可展示的 AI 分析内容，点击卡片可查看项目详情，后续会补充分析结果。
                  </p>
                </div>
              </article>
            </div>

            <div v-else class="py-10 text-center text-sm text-slate-400">
              <div class="spinner mx-auto mb-3"></div>
              加载今日热榜与 AI 分析中...
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 核心内容区域 -->
    <main class="mx-auto max-w-[1500px] px-4 py-8 lg:px-6">

      <!-- 今日报告 -->
      <section id="trending-projects" class="mb-12">
        <div class="terminal-section-title animate-fadeInUp">
          <div>
            <p class="section-kicker">每日报告</p>
            <h3>今日报告</h3>
          </div>
          <div class="flex items-center gap-3">
            <span v-if="todayBrief.date" class="text-sm text-slate-400">{{ formatDate(todayBrief.date) }} · {{ todayBrief.project_count || 0 }} 个项目</span>
            <button v-if="todayBrief.content" class="terminal-action compact" @click="openTodayReport">全屏查看</button>
          </div>
        </div>

        <!-- 报告内容 -->
        <div v-if="todayBrief.content" class="terminal-panel">
          <div
            v-html="renderedReport"
            class="markdown-content px-6 py-5 max-h-[700px] overflow-y-auto"
          ></div>
        </div>
        <div v-else class="terminal-panel flex flex-col items-center justify-center py-16 text-slate-500">
          <svg class="w-12 h-12 mb-4 text-slate-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <p class="text-sm">今日报告尚未生成</p>
          <p class="text-xs mt-2 text-slate-600">每日北京时间 8:00 自动生成</p>
          <router-link to="/rankings" class="terminal-action mt-6">查看历史报告</router-link>
        </div>
      </section>

      <!-- 数据概览 -->
      <section class="mb-12 animate-fadeInUp">
        <div class="terminal-section-title">
          <div>
            <p class="section-kicker">情报概览</p>
            <h3>情报概览</h3>
          </div>
        </div>
        <Suspense>
          <template #default>
            <StatsChart
              :stats="statsData"
              :languageData="topLanguages"
              :trendData="projectTrendData"
              :emergingAreas="emergingAreas"
              :surgingProjects="surgingProjects"
              :surgingMode="surgingMode"
            />
          </template>
          <template #fallback>
            <div class="terminal-panel flex items-center justify-center py-16">
              <div class="spinner"></div>
            </div>
          </template>
        </Suspense>
      </section>

      <!-- 分析报告日历 -->
      <section class="mb-12">
        <div class="terminal-section-title animate-fadeInUp">
          <div>
            <p class="section-kicker">报告归档</p>
            <h3>分析报告</h3>
          </div>
          <router-link to="/rankings" class="flex items-center gap-1 text-sm text-cyan-600 hover:text-cyan-700">
            查看全部 <i class="fa fa-angle-right"></i>
          </router-link>
        </div>

        <div class="terminal-panel overflow-hidden">
          <!-- 日历头部：年月导航 -->
          <div class="flex items-center justify-between gap-4 px-5 py-4" style="background: rgba(26, 150, 184, 0.06); border-bottom: 1px solid rgba(26, 150, 184, 0.15);">
            <div class="flex items-center gap-1">
              <button @click="calYear--" title="上一年" class="cal-nav-btn">«</button>
              <button @click="prevMonth" title="上个月" class="cal-nav-btn">‹</button>
            </div>
            <div class="flex items-baseline gap-2.5">
              <span class="text-lg font-semibold text-slate-900">{{ calYear }}年{{ calMonth + 1 }}月</span>
              <span class="status-chip online">{{ calMonthReportCount }} 份报告</span>
            </div>
            <div class="flex items-center gap-1">
              <button @click="nextMonth" title="下个月" class="cal-nav-btn">›</button>
              <button @click="calYear++" title="下一年" class="cal-nav-btn">»</button>
            </div>
          </div>

          <!-- 星期头 -->
          <div class="grid grid-cols-7" style="border-bottom: 1px solid rgba(26, 150, 184, 0.12);">
            <div v-for="w in ['一','二','三','四','五','六','日']" :key="w"
              class="py-2.5 text-center font-mono text-[10px] uppercase tracking-[0.2em] text-cyan-700/60">{{ w }}</div>
          </div>

          <!-- 日期格子 -->
          <div class="grid grid-cols-7">
            <div
              v-for="(cell, i) in calendarCells" :key="i"
              class="cal-cell relative min-h-[78px] p-2 transition-all duration-150"
              :class="[
                !cell.curMonth ? 'cal-cell--muted' : '',
                cell.report ? 'cal-cell--report cursor-pointer' : '',
                cell.isToday ? 'cal-cell--today' : ''
              ]"
              @click="cell.report && openReportModal(cell.report)"
            >
              <!-- 日期数字 + 今日标记 -->
              <div class="flex items-center justify-between">
                <span class="font-mono text-xs leading-none"
                  :class="[
                    cell.isToday ? 'font-bold text-cyan-600' : cell.curMonth ? 'text-slate-600' : 'text-slate-300'
                  ]">
                  {{ cell.day }}
                </span>
                <span v-if="cell.isToday" class="rounded-full bg-cyan-500 px-1.5 py-0.5 text-[9px] font-medium leading-none text-white">今天</span>
              </div>

              <!-- 有报告时显示徽章 -->
              <div v-if="cell.report" class="cal-report-badge mt-2">
                <span class="cal-report-dot"></span>
                <span>{{ cell.report.project_count }} 个项目</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 加载提示 -->
        <div v-if="isLoading" class="fixed inset-0 z-40 flex items-center justify-center bg-black/60">
          <div class="flex flex-col items-center border border-cyan-200 bg-white p-6 shadow-2xl">
            <div class="mb-4 h-12 w-12 animate-spin border-4 border-cyan-400/20 border-t-cyan-300"></div>
            <p class="text-slate-700">加载报告内容中...</p>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="border-t border-cyan-400/10 bg-[#dff2f8]">
      <div class="mx-auto flex max-w-[1500px] flex-col gap-3 px-4 py-6 text-xs text-slate-500 md:flex-row md:items-center md:justify-between lg:px-6">
        <span>GITTREND INTEL / 开源情报观察站</span>
        <span>© {{ new Date().getFullYear() }} GitTrend Insights</span>
      </div>
    </footer>

    <!-- 项目详情模态框 -->
    <ProjectModal 
      :visible="isProjectModalOpen"
      :project-name="selectedProject?.name"
      @close="closeProjectModal"
    />

    <!-- 报告详情模态框 -->
    <ReportModal 
      :report="selectedReport"
      :theme="theme"
      v-if="isReportModalOpen"
      @close="closeReportModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, defineAsyncComponent } from 'vue'
import { useRouter } from 'vue-router'
import ProjectModal from '@/components/ProjectModal.vue'
import ReportModal from '@/components/ReportModal.vue'
import type { Project, Report, Stats, TrendsData, TrendDataItem } from '@/api/reports'
import { getReports, getStats, getTrends, getReportByDate, getTrendData, getTrending, getProjectDetails, getProjectTrend } from '@/api/reports'
import { renderMarkdown } from '@/utils/markdown-simple'
import { extractAnalysisPreview, splitAnalysisContent } from '@/utils/analysis'

const StatsChart = defineAsyncComponent(() => import('@/components/StatsChart.vue'))

const router = useRouter()

// ── 今日 Trending ──────────────────────────────────────
interface TodayTrendingProject extends Project {
  renderedAnalysis?: string
  analysisPreview?: string
  analysisLoading?: boolean
}

const todayTrendingList = ref<TodayTrendingProject[]>([])
const todayTrendingUpdatedAt = ref('')

async function loadTodayTrending() {
  try {
    const data = await getTrending()
    todayTrendingUpdatedAt.value = data.updated_at || ''
    const repos = (data.repositories || []).slice(0, 8)

    todayTrendingList.value = repos.map((repo) => ({
      ...repo,
      renderedAnalysis: '',
      analysisPreview: '',
      analysisLoading: true
    }))

    const enrichedRepos = await Promise.all(
      repos.map(async (repo) => {
        try {
          const detail = await getProjectDetails(repo.name)
          const analysis = (detail.analysis || '').trim()
          const parsedAnalysis = splitAnalysisContent(analysis)
          const renderedAnalysis = parsedAnalysis.detailMarkdown
            ? await renderMarkdown(parsedAnalysis.detailMarkdown)
            : ''
          const analysisPreview = parsedAnalysis.summary || extractAnalysisPreview(analysis, 140)

          return {
            ...repo,
            ...detail,
            analysis,
            renderedAnalysis,
            analysisPreview,
            analysisLoading: false
          } satisfies TodayTrendingProject
        } catch {
          return {
            ...repo,
            renderedAnalysis: '',
            analysisPreview: '',
            analysisLoading: false
          } satisfies TodayTrendingProject
        }
      })
    )

    todayTrendingList.value = enrichedRepos
  } catch {
    todayTrendingList.value = []
    todayTrendingUpdatedAt.value = ''
  }
}
// ───────────────────────────────────────────────────────

// ── 日历 ──────────────────────────────────────────────
const now = new Date()
const calYear = ref(now.getFullYear())
const calMonth = ref(now.getMonth()) // 0-indexed

function prevMonth() {
  if (calMonth.value === 0) { calYear.value--; calMonth.value = 11 }
  else calMonth.value--
}
function nextMonth() {
  if (calMonth.value === 11) { calYear.value++; calMonth.value = 0 }
  else calMonth.value++
}

const reportMap = computed(() => {
  const m: Record<string, Report> = {}
  for (const r of featuredReports.value) m[r.date] = r
  return m
})

const calMonthReportCount = computed(() =>
  calendarCells.value.filter(c => c.curMonth && c.report).length
)

interface CalCell {
  day: number
  date: string
  curMonth: boolean
  isToday: boolean
  report: Report | null
}

const calendarCells = computed((): CalCell[] => {
  const y = calYear.value
  const m = calMonth.value
  const todayStr = now.toISOString().split('T')[0]

  const firstDay = new Date(y, m, 1)
  // getDay(): 0=Sun → adjust to Mon-first: Mon=0 … Sun=6
  const startOffset = (firstDay.getDay() + 6) % 7
  const daysInMonth = new Date(y, m + 1, 0).getDate()
  const prevDays = new Date(y, m, 0).getDate()

  const cells: CalCell[] = []

  // Prev month padding
  for (let i = startOffset - 1; i >= 0; i--) {
    const d = prevDays - i
    const mm = m === 0 ? 12 : m
    const yy = m === 0 ? y - 1 : y
    const date = `${yy}-${String(mm).padStart(2,'0')}-${String(d).padStart(2,'0')}`
    cells.push({ day: d, date, curMonth: false, isToday: date === todayStr, report: reportMap.value[date] ?? null })
  }

  // Current month
  for (let d = 1; d <= daysInMonth; d++) {
    const date = `${y}-${String(m + 1).padStart(2,'0')}-${String(d).padStart(2,'0')}`
    cells.push({ day: d, date, curMonth: true, isToday: date === todayStr, report: reportMap.value[date] ?? null })
  }

  // Next month padding to fill 6 rows
  const remaining = 42 - cells.length
  for (let d = 1; d <= remaining; d++) {
    const mm = m === 11 ? 1 : m + 2
    const yy = m === 11 ? y + 1 : y
    const date = `${yy}-${String(mm).padStart(2,'0')}-${String(d).padStart(2,'0')}`
    cells.push({ day: d, date, curMonth: false, isToday: date === todayStr, report: reportMap.value[date] ?? null })
  }

  return cells
})
// ─────────────────────────────────────────────────────

// 渲染好的报告 HTML
const renderedReport = ref('')

function formatStars(stars: number): string {
  if (!stars) return '0'
  if (stars >= 1000) return (stars / 1000).toFixed(1) + 'k'
  return String(stars)
}

function preprocessReportContent(content: string): string {
  // 把"详见历史报告"替换成真实链接
  return content.replace(
    /今日上榜项目此前均已分析，详见历史报告。/g,
    '今日上榜项目此前均已分析，[查看历史报告 →](/rankings)'
  )
}


// 响应式数据
const theme = ref<'light' | 'dark'>('light')
const timeFilter = ref('today')

// 监听timeFilter变化，更新项目数据
watch(timeFilter, async () => {
  await refreshData()
})
const statsData = ref<Stats>({
  totalReports: 0,
  totalProjects: 0,
  topLanguage: 'N/A',
  weeklyNew: 0,
  totalForks: '0',
  avgContributors: 0,
  activityScore: 0
})
const trendingProjects = ref<Project[]>([])
const featuredReports = ref<Report[]>([])
const trendsData = ref<TrendsData>({  time_window_days: 30,
  most_frequent_projects: [],
  most_frequent_languages: [],
  programmingLanguages: [],
  surgingProjects: [],
  techDomains: []
})
const projectTrendData = ref<TrendDataItem[]>([]) // 项目趋势数据
const trendAreasData = ref<TrendDataItem[]>([]) // 新兴技术领域数据

// 今日简报
const todayBrief = ref<{ date: string; headline: string; summary: string; project_count: number; content: string }>({
  date: '',
  headline: '',
  summary: '',
  project_count: 0,
  content: ''
})

// 加载状态
const isLoading = ref(false)

// 模态框状态
const isProjectModalOpen = ref(false)
const isReportModalOpen = ref(false)
const selectedProject = ref<Project | null>(null)

// 趋势雷达内嵌面板状态
const trendRadarTab = ref<'areas' | 'languages' | 'activity'>('areas')
const trendRadarTabs = [
  { value: 'areas' as const, label: '领域趋势' },
  { value: 'languages' as const, label: '语言分布' },
  { value: 'activity' as const, label: '活跃度指标' }
]
const selectedReport = ref<Report>({
  date: '',
  project_count: 0
})

const analyzedTrendingCount = computed(() => todayTrendingList.value.filter((repo) => !!repo.analysis).length)

const intelligenceFeed = computed(() => [
  {
    label: '最新报告',
    value: featuredReports.value[0]?.date || '待生成'
  },
  {
    label: '高频语言',
    value: topLanguages.value[0]?.name || statsData.value.topLanguage || 'N/A'
  },
  {
    label: '项目样本',
    value: `${trendingProjects.value.length || statsData.value.totalProjects || 0} repos`
  },
  {
    label: surgingMode.value === 'hot' ? '热度样本' : '增长样本',
    value: `${surgingProjects.value.length} signals`
  }
])

// 计算属性 - 热门编程语言
const topLanguages = computed(() => {
  // 只使用从API获取的真实语言数据
  if (trendsData.value && trendsData.value.most_frequent_languages && trendsData.value.most_frequent_languages.length > 0) {
    const total = trendsData.value.most_frequent_languages.reduce((sum, [, count]) => sum + count, 0)
    
    // 为语言分配颜色类
    const colorClasses = [
      'bg-gradient-to-r from-blue-500 to-blue-600',
      'bg-gradient-to-r from-yellow-500 to-yellow-600',
      'bg-gradient-to-r from-green-500 to-green-600',
      'bg-gradient-to-r from-cyan-500 to-cyan-600',
      'bg-gradient-to-r from-orange-500 to-orange-600',
      'bg-gradient-to-r from-purple-500 to-purple-600',
      'bg-gradient-to-r from-pink-500 to-pink-600',
      'bg-gradient-to-r from-red-500 to-red-600'
    ]
    
    return trendsData.value.most_frequent_languages
      .slice(0, 5) // 只显示前5种语言
      .map(([name, count], index) => ({
        name,
        count,
        percentage: Math.round((count / total) * 100),
        colorClass: colorClasses[index % colorClasses.length]
      }))
  }
  
  // 如果没有真实数据，返回空数组
  return []
})

// 更新热门趋势项目数据
function updateTrendingProjects() {
  if (trendsData.value && trendsData.value.most_frequent_projects && trendsData.value.most_frequent_projects.length > 0) {
    // 直接使用后端返回的完整项目数据
    const safeDate = (val: string | undefined) => {
      if (!val || val === 'N/A') return new Date().toISOString().split('T')[0]
      const d = new Date(val)
      return isNaN(d.getTime()) ? new Date().toISOString().split('T')[0] : d.toISOString().split('T')[0]
    }
    trendingProjects.value = trendsData.value.most_frequent_projects.slice(0, 12).map(project => ({
      name: project.name,
      url: project.url || `https://github.com/${project.name}`,
      description: project.description,
      language: project.language,
      stars: project.stars || project.avg_stars || 0,
      forks: project.forks || 0,
      contributor_count: project.contributor_count || 0,
      created_at: project.created_at && project.created_at !== 'N/A' ? project.created_at : new Date().toISOString(),
      updated_at: project.updated_at && project.updated_at !== 'N/A' ? project.updated_at : new Date().toISOString(),
      open_issues: project.open_issues || 0,
      watchers: project.watchers || 0,
      summary_date: safeDate(project.created_at)
    }))
  } else {
    // 如果没有真实数据，返回空数组
    trendingProjects.value = []
  }
}

// 计算属性 - 新兴技术领域
const emergingAreas = computed(() => {
  // 只使用从API获取的真实新兴技术领域数据
  if (trendAreasData.value && trendAreasData.value.length > 0) {
    // 为不同的技术领域分配图标和背景色
    const techIcons = ['IconEcosystem', 'IconTooling', 'IconCommunity', 'IconDocumentation']
    const bgClasses = ['bg-purple-500/20', 'bg-blue-500/20', 'bg-green-500/20', 'bg-pink-500/20']
    
    // 进一步映射到相应的days参数
    const areaNameMap: Record<string, string> = {
      '新项目': '生成式AI',
      '活跃项目': 'WebAssembly',
      '热门项目': '边缘计算',
      '趋势项目': '低代码平台'
    }
    
    return trendAreasData.value.slice(0, 4).map((item, index) => ({
      name: areaNameMap[item.label] || item.label,
      growth: item.change,
      bgClass: bgClasses[index % bgClasses.length],
      icon: techIcons[index % techIcons.length]
    }))
  }
  
  // 如果没有真实数据，返回空数组
  return []
})

// 计算属性 - 上升最快项目
const surgingProjects = computed(() => {
  if (trendsData.value && trendsData.value.surgingProjects && trendsData.value.surgingProjects.length > 0) {
    return trendsData.value.surgingProjects.slice(0, 4).map((project, index) => ({
      ...project,
      rank: index + 1
    }))
  }

  return trendingProjects.value.slice(0, 4).map((project, index) => ({
    name: project.name,
    description: project.description,
    language: project.language,
    star_increase: project.stars,
    rank: index + 1
  }))
})

function mapProjectTrendData(points: { date: string; count: number }[]): TrendDataItem[] {
  return points.map((point, index) => {
    const previous = index > 0 ? points[index - 1].count : point.count
    const change = previous > 0
      ? Math.round(((point.count - previous) / previous) * 100)
      : 0

    return {
      label: point.date.slice(5),
      value: point.count,
      change,
      colorClass: ['text-cyan-500', 'text-sky-500', 'text-emerald-500', 'text-blue-500'][index % 4]
    }
  })
}

const surgingMode = computed<'surging' | 'hot'>(() => {
  return trendsData.value?.surgingProjects?.length ? 'surging' : 'hot'
})

// 初始化数据
onMounted(async () => {
  await loadInitialData()

  applyTheme('light')
})

// 加载初始数据
async function loadInitialData() {
  await Promise.all([
    loadStatsData(),
    loadReportCards(),
    loadTrendOverview(),
    loadTodayBrief(),
    loadTodayTrending(),
  ])
}

async function loadStatsData() {
  try {
    statsData.value = await getStats()
  } catch (error) {
    console.error('加载统计数据失败:', error)
    statsData.value = { totalReports: 0, totalProjects: 0, topLanguage: 'N/A', weeklyNew: 0, totalForks: '0', avgContributors: 0, activityScore: 0 }
  }
}

async function loadReportCards() {
  try {
    const reports = await getReports()
    featuredReports.value = reports.sort((a, b) => b.date.localeCompare(a.date))
  } catch (error) {
    console.error('加载报告列表失败:', error)
    featuredReports.value = []
  }
}

function extractBrief(content: string): { headline: string; summary: string } {
  if (!content) return { headline: '', summary: '' }
  const lines = content.split('\n')
  // 找第一个 ## 标题作为 headline
  const headlineLine = lines.find(l => l.trim().startsWith('## '))
  const headline = headlineLine?.replace(/^##\s*/, '').trim() || ''
  // 跳过标题，取后续纯文本段落作为摘要（排除列表、代码块等）
  const bodyStart = headlineLine ? lines.indexOf(headlineLine) + 1 : 0
  const paragraphs: string[] = []
  for (let i = bodyStart; i < lines.length && paragraphs.length < 3; i++) {
    const line = lines[i].trim()
    if (!line) continue
    if (line.startsWith('#') || line.startsWith('```') || line.startsWith('>') || line.startsWith('-') || line.startsWith('*')) continue
    if (line.startsWith('**') && line.endsWith('**')) continue
    paragraphs.push(line)
  }
  return { headline, summary: paragraphs.join('\n\n') }
}

async function loadTodayBrief() {
  try {
    const reports = await getReports()
    if (reports.length === 0) return
    const latest = reports.sort((a, b) => b.date.localeCompare(a.date))[0]
    const fullReport = await getReportByDate(latest.date)
    const { headline, summary } = extractBrief(fullReport.content || '')
    const content = fullReport.content || ''
    todayBrief.value = {
      date: latest.date,
      headline: headline || `GitHub 趋势分析报告 (${latest.date})`,
      summary: summary || '报告正在生成中，请稍后查看。',
      project_count: latest.project_count || fullReport.project_count || 0,
      content
    }
    if (content) {
      renderedReport.value = await renderMarkdown(preprocessReportContent(content))
    }
  } catch (error) {
    console.error('加载今日简报失败:', error)
  }
}

function openTodayReport() {
  const report: Report = {
    date: todayBrief.value.date,
    project_count: todayBrief.value.project_count,
    content: todayBrief.value.content
  }
  selectedReport.value = report
  isReportModalOpen.value = true
}

async function loadTrendOverview() {
  try {
    const [trendsResponse, trendAreasResponse, projectTrendResponse] = await Promise.all([
      getTrends(),
      getTrendData(),
      getProjectTrend(7)
    ])
    trendsData.value = trendsResponse
    trendAreasData.value = trendAreasResponse
    projectTrendData.value = mapProjectTrendData(projectTrendResponse)
    updateTrendingProjects()
  } catch (error) {
    console.error('加载趋势数据失败:', error)
    trendingProjects.value = []
    trendsData.value = { time_window_days: 7, most_frequent_projects: [], most_frequent_languages: [], programmingLanguages: [], surgingProjects: [], techDomains: [] }
    projectTrendData.value = []
    trendAreasData.value = []
  }
}

// 刷新数据
async function refreshData() {
  isLoading.value = true
  try {
      // 根据timeFilter映射到相应的days参数
      let days = 1; // 默认1天（今日）
      switch (timeFilter.value) {
        case 'today':
          days = 1; // 今日数据使用1天
          break;
        case 'week':
          days = 7; // 本周数据使用7天
          break;
        case 'month':
          days = 30; // 本月数据使用30天
          break;
      }
      
      // 并行获取趋势数据和新兴技术领域数据
      const [newTrendsResponse, newTrendAreasResponse, newProjectTrendResponse] = await Promise.all([
        getTrends({ days }),
        getTrendData(),
        getProjectTrend(days)
      ]);
    
      // 更新趋势数据和新兴技术领域数据
      trendsData.value = newTrendsResponse
      trendAreasData.value = newTrendAreasResponse
      projectTrendData.value = mapProjectTrendData(newProjectTrendResponse)
    
    // 更新项目数据
    updateTrendingProjects()
  } catch (error) {
    console.error('刷新数据失败:', error)
    // 如果失败，清空项目数据而不是使用模拟数据
    trendingProjects.value = []
    projectTrendData.value = []
  } finally {
    isLoading.value = false
  }
}

// 查看今日热门
function viewTodayTrending() {
  // 设置时间过滤器为今日
  timeFilter.value = 'today'
  // 重新加载数据以确保显示今日热门项目
  loadInitialData().then(() => {
    // 滚动到热门趋势项目区域
    const element = document.querySelector('#trending-projects')
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  })
}

function setTheme(newTheme: 'light' | 'dark') {
  theme.value = newTheme
  applyTheme(newTheme)
}

function applyTheme(newTheme: 'light' | 'dark') {
  if (newTheme === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// 打开项目详情模态框
function openProjectModal(project: Project) {
  selectedProject.value = project
  isProjectModalOpen.value = true
}

// 关闭项目详情模态框
function closeProjectModal() {
  isProjectModalOpen.value = false
  setTimeout(() => {
    selectedProject.value = null
  }, 300)
}

// 打开报告详情模态框
async function openReportModal(report: Report) {
  // 先以已知信息打开模态框，避免与全屏加载遮罩同时出现造成闪屏
  selectedReport.value = report
  isReportModalOpen.value = true
  try {
    const fullReport = await getReportByDate(report.date)
    selectedReport.value = fullReport
  } catch (error) {
    console.error('加载报告内容失败:', error)
  }
}

// 关闭报告详情模态框
function closeReportModal() {
  isReportModalOpen.value = false
}

// 日期格式化
function formatDate(dateStr: string): string {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function formatDateTime(dateStr: string): string {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  if (Number.isNaN(date.getTime())) return dateStr
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatReportDay(dateStr: string): string {
  if (!dateStr) return '--'
  const date = new Date(dateStr)
  return String(date.getDate()).padStart(2, '0')
}

function formatReportMonth(dateStr: string): string {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}`
}

function getReportTitle(report: Report): string {
  const content = report.content || ''
  if (!content) return `${formatDate(report.date)} GitHub 趋势分析报告`

  const heading = content
    .split('\n')
    .map(line => line.trim())
    .find(line => line.startsWith('#'))

  return heading?.replace(/^#+\s*/, '') || 'GitHub 热门项目报告'
}
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeInUp {
  animation: fadeInUp 0.5s ease forwards;
}

/* ── 分析报告日历 ── */
.cal-nav-btn {
  display: inline-flex;
  height: 1.85rem;
  width: 1.85rem;
  align-items: center;
  justify-content: center;
  border-radius: 0.4rem;
  border: 1px solid rgba(26, 150, 184, 0.25);
  background: #ffffff;
  font-size: 0.78rem;
  color: #127a98;
  transition: all 0.15s ease;
}

.cal-nav-btn:hover {
  border-color: rgba(26, 150, 184, 0.5);
  background: rgba(26, 150, 184, 0.1);
  color: #0a2d3d;
}

.cal-cell {
  border-bottom: 1px solid rgba(26, 150, 184, 0.12);
  border-right: 1px solid rgba(26, 150, 184, 0.12);
}

.cal-cell--muted {
  background: rgba(26, 150, 184, 0.025);
}

.cal-cell--report:hover {
  background: rgba(26, 150, 184, 0.06);
  box-shadow: inset 0 0 0 1px rgba(26, 150, 184, 0.18);
}

.cal-cell--today {
  background: rgba(26, 150, 184, 0.07);
  box-shadow: inset 0 0 0 1px rgba(26, 150, 184, 0.3);
}

.cal-report-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  border-radius: 0.35rem;
  border: 1px solid rgba(26, 150, 184, 0.22);
  background: rgba(26, 150, 184, 0.08);
  padding: 0.2rem 0.4rem;
  font-size: 10px;
  line-height: 1.1;
  color: #127a98;
  font-weight: 500;
}

.cal-report-dot {
  display: inline-block;
  width: 5px;
  height: 5px;
  border-radius: 9999px;
  background: #1a96b8;
}
</style>
