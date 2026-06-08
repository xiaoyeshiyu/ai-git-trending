<template>
  <div class="terminal-page">
    <!-- 顶部导航栏 - 技术情报终端 -->
    <header class="terminal-header">
      <div class="mx-auto flex max-w-[1500px] items-center justify-between px-4 py-3 lg:px-6">
        <div class="flex items-center gap-3">
          <div class="flex h-9 w-9 items-center justify-center border border-cyan-400/30 bg-cyan-400/10 text-cyan-300">
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
          </div>
          <div>
            <h1 class="text-sm font-semibold tracking-[0.28em] text-slate-100">GITTREND INTEL</h1>
            <p class="text-[10px] uppercase tracking-[0.26em] text-cyan-400/70">LEADERBOARD INTELLIGENCE</p>
          </div>
        </div>

        <nav class="hidden items-center gap-1 md:flex">
          <router-link to="/" class="terminal-nav">情报台</router-link>
          <router-link to="/trend" class="terminal-nav">趋势</router-link>
          <router-link to="/rankings" class="terminal-nav active">排行榜</router-link>
          <router-link to="/trend-analysis" class="terminal-nav">趋势图谱</router-link>        </nav>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="terminal-main">
      <!-- 页面标题 -->
      <div class="mb-6">
        <p class="section-kicker">LEADERBOARD</p>
        <h2 class="text-3xl font-semibold text-slate-900">排行榜</h2>
        <p class="mt-2 max-w-2xl text-slate-600">
          查看最受欢迎的开源项目与历史分析报告，并快速浏览项目级 AI 摘要
        </p>
      </div>

      <!-- 子标签切换 -->
      <div class="mb-6 flex flex-wrap items-center gap-2 rounded-2xl border border-cyan-100 bg-white/90 p-3 shadow-sm">
        <button
          @click="activeTab = 'projects'"
          :class="['terminal-action', activeTab === 'projects' ? 'primary' : '']"
        >
          <svg class="w-4 h-4 mr-1.5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
          </svg>
          项目排行
        </button>
        <button
          @click="activeTab = 'reports'"
          :class="['terminal-action', activeTab === 'reports' ? 'primary' : '']"
        >
          <svg class="w-4 h-4 mr-1.5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          报告归档
        </button>
        <span v-if="activeTab === 'projects'" class="ml-auto self-center text-xs text-slate-500">
          共 {{ totalProjects }} 个项目
        </span>
        <span v-else class="ml-auto self-center text-xs text-slate-500">
          共 {{ reportList.length }} 份报告
        </span>
      </div>

      <!-- ==================== 项目排行 Tab ==================== -->
      <template v-if="activeTab === 'projects'">
      <!-- 筛选选项 -->
      <div class="mb-8 flex flex-wrap items-center gap-4 rounded-2xl border border-cyan-100 bg-white/90 p-4 shadow-sm">
        <div class="flex gap-2">
          <button
            v-for="period in timePeriods"
            :key="period.value"
            @click="selectedPeriod = period.value"
            :class="[
              'terminal-action',
              selectedPeriod === period.value ? 'primary' : ''
            ]"
          >
            {{ period.label }}
          </button>
        </div>
        <select v-model="selectedCategory" class="terminal-select min-w-[180px]">
          <option v-for="category in categories" :key="category.value" :value="category.value">
            {{ category.label }}
          </option>
        </select>
        <span v-if="loadingDomains" class="text-xs text-slate-500">正在加载领域分类...</span>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="terminal-loading">
        <div class="spinner"></div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="projects.length === 0" class="terminal-empty">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path>
        </svg>
        <h3 class="text-lg font-medium text-slate-400 mb-2">暂无排名数据</h3>
        <p class="text-slate-500">请尝试选择其他时间段或分类</p>
      </div>

      <!-- 项目列表 -->
      <div v-else class="space-y-4">
        <div
          v-for="(project, index) in projects"
          :key="project.name"
          class="rounded-2xl border border-cyan-100 bg-white/95 p-5 shadow-sm transition-all hover:border-cyan-200"
        >
          <div class="flex items-start gap-4">
            <!-- 排名 -->
            <div class="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-200 bg-cyan-50 text-lg font-bold text-cyan-700">
              {{ (currentPage - 1) * pageSize + index + 1 }}
            </div>

            <div class="min-w-0 flex-1 cursor-pointer" @click="viewProjectDetails(project)">
              <div class="mb-1 flex items-start justify-between gap-4">
                <div class="min-w-0 flex-1">
                  <div class="flex min-w-0 items-center gap-2">
                    <span class="truncate text-lg font-semibold text-slate-900">{{ project.name }}</span>
                    <span v-if="project.language" class="shrink-0 rounded-full border border-cyan-200 bg-cyan-50 px-2 py-0.5 text-[10px] text-cyan-700">
                      {{ project.language }}
                    </span>
                  </div>
                  <p class="mt-2 text-sm leading-6 text-slate-600">
                    {{ project.description || '暂无描述' }}
                  </p>
                </div>
                <div class="shrink-0 flex items-center gap-2">
                  <button class="inline-flex h-8 items-center rounded-full border border-cyan-200 bg-white px-3 text-[11px] font-medium text-cyan-700 hover:bg-cyan-50">
                    详情
                  </button>
                  <div class="inline-flex h-8 items-center rounded-full border border-cyan-200 bg-cyan-50/80 px-3 text-[11px] font-medium text-slate-800">
                    ★ {{ formatCompactNumber(project.stars || 0) }}
                  </div>
                </div>
              </div>

              <div class="mt-3 flex flex-wrap items-center gap-2 text-xs text-slate-500">
                <span class="rounded-full border border-cyan-100 bg-cyan-50 px-2.5 py-1">Forks {{ formatCompactNumber(project.forks || 0) }}</span>
                <span class="rounded-full border border-cyan-100 bg-cyan-50 px-2.5 py-1">Contributors {{ formatCompactNumber(project.contributor_count || 0) }}</span>
                <span class="rounded-full border border-cyan-100 bg-cyan-50 px-2.5 py-1">
                  {{ project.created_at && project.created_at !== 'N/A' ? `创建 ${String(project.created_at).slice(0, 4)}` : '创建时间未知' }}
                </span>
              </div>

              <div v-if="project.analysis" class="mt-3 rounded-xl border border-cyan-100 bg-cyan-50/70 px-4 py-3">
                <p class="text-sm leading-6 text-slate-700">
                  {{ getProjectAnalysisPreview(project) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- 分页控件 -->
        <div v-if="totalPages > 1" class="mt-8 flex items-center justify-center gap-2">
          <button
            class="terminal-action"
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>

          <template v-for="page in totalPages" :key="page">
            <button
              v-if="page === 1 || page === totalPages || (page >= currentPage - 1 && page <= currentPage + 1)"
              class="terminal-action"
              :class="{ 'primary': currentPage === page }"
              @click="changePage(page)"
            >
              {{ page }}
            </button>
            <span
              v-else-if="page === currentPage - 2 || page === currentPage + 2"
              class="text-slate-500"
            >
              ...
            </span>
          </template>

          <button
            class="terminal-action"
            :disabled="currentPage === totalPages"
            @click="changePage(currentPage + 1)"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
        </div>

        <!-- 总数显示 -->
        <div v-if="totalProjects > 0" class="mt-4 text-center text-sm text-slate-500">
          共 {{ totalProjects }} 个项目，第 {{ currentPage }}/{{ totalPages }} 页
        </div>
      </div>
      </template>

      <!-- ==================== 报告归档 Tab ==================== -->
      <template v-if="activeTab === 'reports'">
        <div v-if="reportLoading" class="terminal-loading">
          <div class="spinner"></div>
        </div>

        <div v-else-if="reportList.length === 0" class="terminal-empty">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <h3 class="text-lg font-medium text-slate-400 mb-2">暂无报告</h3>
          <p class="text-slate-500">报告将在每日北京时间 8:00 自动生成</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="report in reportList"
            :key="report.date"
            @click="openReport(report)"
            class="block cursor-pointer rounded-2xl border border-cyan-100 bg-white/95 p-5 shadow-sm transition-all hover:border-cyan-200"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-3 mb-2">
                  <span class="text-sm font-semibold text-slate-900">{{ formatReportDate(report.date) }}</span>
                  <span class="border border-emerald-200 bg-emerald-50 px-2 py-0.5 text-[11px] text-emerald-700">已生成</span>
                  <span class="text-xs text-slate-500">{{ report.project_count }} 个项目</span>
                </div>
                <p class="line-clamp-2 text-sm leading-relaxed text-slate-600">
                  {{ getReportBrief(report) }}
                </p>
              </div>
              <svg class="mt-1 h-5 w-5 flex-shrink-0 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M10 5.5 16 12l-6 6.5"></path>
              </svg>
            </div>
          </div>
        </div>
      </template>
    </main>

    <!-- 项目详情模态框 -->
    <ProjectModal
      :visible="showProjectModal"
      :project-name="selectedProjectName"
      @close="showProjectModal = false"
    />

    <!-- 报告详情模态框 -->
    <ReportModal
      v-if="showReportModal"
      :report="selectedReport"
      theme="dark"
      @close="showReportModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { reportApi, type Project, type Report } from '@/api/reports'
import ProjectModal from '@/components/ProjectModal.vue'
import ReportModal from '@/components/ReportModal.vue'
import { extractAnalysisPreview } from '@/utils/analysis'

const activeTab = ref<'projects' | 'reports'>('projects')
const loading = ref(false)
const projects = ref<Project[]>([])
const selectedPeriod = ref('yearly')
const selectedCategory = ref('all')
const showProjectModal = ref(false)
const selectedProjectName = ref('')

// 报告归档
const reportList = ref<Report[]>([])
const reportLoading = ref(false)

// 报告模态框
const showReportModal = ref(false)
const selectedReport = ref<Report>({ date: '', project_count: 0 })

async function openReport(report: Report) {
  try {
    const full = await reportApi.getReportContent(report.date)
    selectedReport.value = full
    showReportModal.value = true
  } catch (e) {
    console.error('加载报告失败:', e)
  }
}

// 格式化报告日期
function formatReportDate(dateStr: string): string {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'short' })
}

// 提取报告摘要
function getReportBrief(report: Report): string {
  const content = report.content || ''
  if (!content) return `${formatReportDate(report.date)} GitHub 趋势分析报告`

  // 提取第一个 ## 标题
  const lines = content.split('\n')
  const headingLine = lines.find(l => l.trim().startsWith('## '))
  const heading = headingLine?.replace(/^##\s*/, '').trim() || ''

  // 提取正文前两段
  const bodyStart = headingLine ? lines.indexOf(headingLine) + 1 : 0
  const paragraphs: string[] = []
  for (let i = bodyStart; i < lines.length && paragraphs.length < 2; i++) {
    const line = lines[i].trim()
    if (!line) continue
    if (line.startsWith('#') || line.startsWith('```') || line.startsWith('>')) continue
    paragraphs.push(line)
  }

  return heading || paragraphs.join(' ') || `${formatReportDate(report.date)} GitHub 趋势分析报告`
}

// 加载报告列表
async function loadReports() {
  reportLoading.value = true
  try {
    const reports = await reportApi.getReports()
    // 按日期降序排列
    reportList.value = reports.sort((a, b) => b.date.localeCompare(a.date))
  } catch (error) {
    console.error('加载报告列表失败:', error)
  } finally {
    reportLoading.value = false
  }
}



// 分页相关
const currentPage = ref(1)
const pageSize = ref(20)
const totalProjects = ref(0)
const totalPages = computed(() => Math.ceil(totalProjects.value / pageSize.value))
const DOMAIN_LABELS: Record<string, string> = {
  all: '全部领域',
  'AI/ML': 'AI/机器学习',
  'LLM Apps': 'LLM 应用',
  Web: 'Web开发',
  Frontend: '前端',
  Mobile: '移动开发',
  DevOps: 'DevOps',
  'Data Science': '数据科学',
  Database: '数据库',
  Tools: '工具',
  Security: '安全',
  Blockchain: '区块链',
  Gaming: '游戏开发',
  OS: '系统编程',
  IoT: '物联网',
  Other: '其他'
}

const timePeriods = [
  { label: '今日', value: 'daily' },
  { label: '本周', value: 'weekly' },
  { label: '本月', value: 'monthly' },
  { label: '全年', value: 'yearly' }
]

const categories = ref<Array<{ value: string; label: string }>>([
  { value: 'all', label: DOMAIN_LABELS.all }
])
const loadingDomains = ref(false)

// 加载技术领域分类
const loadTechDomains = async () => {
  loadingDomains.value = true
  try {
    const domains = await reportApi.getTechDomains()
    if (domains && domains.length > 0) {
      categories.value = [
        { value: 'all', label: DOMAIN_LABELS.all },
        ...domains
          .filter((domain) => domain.name && domain.name !== 'Other')
          .map((domain) => ({
            value: domain.name,
            label: DOMAIN_LABELS[domain.name] || domain.name
          })),
        ...(
          domains.some((domain) => domain.name === 'Other')
            ? [{ value: 'Other', label: DOMAIN_LABELS.Other }]
            : []
        )
      ]
    }
  } catch (error) {
    console.error('加载技术领域失败:', error)
  } finally {
    loadingDomains.value = false
  }
}

// 根据选择的时间段计算日期范围
const getDateRange = (period: string): { dateFrom: string; dateTo: string } => {
  const now = new Date()
  const today = now.toISOString().split('T')[0]
  let dateFrom: string
  let dateTo = today

  switch (period) {
    case 'daily':
      dateFrom = today
      break
    case 'weekly':
      const weekAgo = new Date(now)
      weekAgo.setDate(now.getDate() - 7)
      dateFrom = weekAgo.toISOString().split('T')[0]
      break
    case 'monthly':
      const monthAgo = new Date(now)
      monthAgo.setMonth(now.getMonth() - 1)
      dateFrom = monthAgo.toISOString().split('T')[0]
      break
    case 'yearly':
      const yearAgo = new Date(now)
      yearAgo.setFullYear(now.getFullYear() - 1)
      dateFrom = yearAgo.toISOString().split('T')[0]
      break
    default:
      dateFrom = today
  }

  return { dateFrom, dateTo }
}

// 加载项目列表（支持日期范围、技术领域筛选和分页）
const loadProjects = async () => {
  loading.value = true
  try {
    const { dateFrom, dateTo } = getDateRange(selectedPeriod.value)
    const params: any = {
      date_from: dateFrom,
      date_to: dateTo,
      sort_by: 'stars',
      order: 'desc',
      page: currentPage.value,
      page_size: pageSize.value
    }
    // 使用技术领域筛选
    if (selectedCategory.value !== 'all') {
      params.tech_domain = selectedCategory.value
    }
    const response = await reportApi.getProjects(params)
    projects.value = response.items || []
    totalProjects.value = response.total || 0
  } catch (error) {
    console.error('Failed to load projects:', error)
  } finally {
    loading.value = false
  }
}

// 切换页码
const changePage = (page: number) => {
  currentPage.value = page
  loadProjects()
}

// 监听筛选变化，重置到第一页
watch(selectedPeriod, () => {
  currentPage.value = 1
  loadProjects()
})

watch(selectedCategory, () => {
  currentPage.value = 1
  loadProjects()
})

const viewProjectDetails = (project: Project) => {
  selectedProjectName.value = project.name
  showProjectModal.value = true
}

const getProjectAnalysisPreview = (project: Project) => {
  return extractAnalysisPreview(project.analysis || '', 180)
}

const formatCompactNumber = (value: number) => {
  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`
  if (value >= 1000) return `${(value / 1000).toFixed(1)}K`
  return `${value}`
}

onMounted(() => {
  loadTechDomains()
  loadProjects()
  loadReports()
})
</script>

<style scoped>
.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.stat-label {
  font-size: 12px;
  color: slate-400;
}
</style>
