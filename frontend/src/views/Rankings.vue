<template>
  <div class="terminal-page">
    <!-- 顶部导航栏 - 技术情报终端 -->
    <header class="terminal-header">
      <div class="mx-auto flex max-w-[1500px] items-center justify-between px-4 py-3 lg:px-6">
        <div class="flex items-center gap-3">
          <div class="flex h-9 w-9 items-center justify-center border border-cyan-400/30 bg-cyan-400/10 text-cyan-300">
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
            </svg>
          </div>
          <div>
            <h1 class="text-sm font-semibold tracking-[0.28em] text-slate-100">GITTREND INTEL</h1>
            <p class="text-[10px] uppercase tracking-[0.26em] text-cyan-400/70">TECH INTELLIGENCE TERMINAL</p>
          </div>
        </div>

        <nav class="hidden items-center gap-1 md:flex">
          <router-link to="/" class="terminal-nav">情报台</router-link>
          <router-link to="/trend" class="terminal-nav">趋势</router-link>
          <router-link to="/rankings" class="terminal-nav active">排行榜</router-link>
          <router-link to="/trend-analysis" class="terminal-nav">趋势图谱</router-link>
          <router-link to="/favorites" class="terminal-nav">收藏</router-link>
        </nav>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="terminal-main">
      <!-- 页面标题 -->
      <div class="mb-6">
        <p class="section-kicker">LEADERBOARD</p>
        <h2 class="text-3xl font-semibold text-slate-100">排行榜</h2>
        <p class="mt-2 text-slate-400 max-w-2xl">
          查看最受欢迎的开源项目与历史分析报告
        </p>
      </div>

      <!-- 子标签切换 -->
      <div class="mb-6 flex gap-2">
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
        <span v-if="activeTab === 'projects'" class="ml-auto text-xs text-slate-500 self-center">
          共 {{ totalProjects }} 个项目
        </span>
        <span v-else class="ml-auto text-xs text-slate-500 self-center">
          共 {{ reportList.length }} 份报告
        </span>
      </div>

      <!-- ==================== 项目排行 Tab ==================== -->
      <template v-if="activeTab === 'projects'">
      <!-- 筛选选项 -->
      <div class="mb-8 flex flex-wrap gap-4">
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
        <select v-model="selectedCategory" class="terminal-select">
          <option v-for="category in categories" :key="category" :value="category">
            {{ category === 'all' ? '全部领域' : category }}
          </option>
        </select>
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
          class="terminal-panel p-4 flex items-center gap-4"
        >
          <!-- 排名 -->
          <div class="w-10 h-10 rounded-lg bg-cyan-400/10 border border-cyan-400/30 flex items-center justify-center text-cyan-300 font-bold text-lg">
            {{ (currentPage - 1) * pageSize + index + 1 }}
          </div>

          <!-- 项目卡片 -->
          <div class="flex-1 cursor-pointer" @click="viewProjectDetails(project)">
            <ProjectCard :project="project" />
          </div>
        </div>

        <!-- 分页控件 -->
        <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-8">
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
        <div v-if="totalProjects > 0" class="text-center text-sm text-slate-500 mt-4">
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
          <a
            v-for="report in reportList"
            :key="report.date"
            :href="`github_trending_${report.date}.html`"
            target="_blank"
            rel="noopener"
            class="terminal-panel p-4 block hover:border-cyan-400/30 transition-colors"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-3 mb-2">
                  <span class="text-sm font-semibold text-slate-200">{{ formatReportDate(report.date) }}</span>
                  <span class="text-[11px] px-2 py-0.5 border border-green-400/20 bg-green-400/8 text-green-400">已生成</span>
                  <span class="text-xs text-slate-500">{{ report.project_count }} 个项目</span>
                </div>
                <p class="text-sm text-slate-400 leading-relaxed line-clamp-2">
                  {{ getReportBrief(report) }}
                </p>
              </div>
              <svg class="w-5 h-5 text-slate-500 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M10 5.5 16 12l-6 6.5"></path>
              </svg>
            </div>
          </a>
        </div>
      </template>
    </main>

    <!-- 项目详情模态框 -->
    <ProjectModal
      :visible="showProjectModal"
      :project-name="selectedProjectName"
      @close="showProjectModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { reportApi, type Project, type Report } from '@/api/reports'
import ProjectCard from '@/components/ProjectCard.vue'
import ProjectModal from '@/components/ProjectModal.vue'

const activeTab = ref<'projects' | 'reports'>('projects')
const loading = ref(false)
const projects = ref<Project[]>([])
const selectedPeriod = ref('daily')
const selectedCategory = ref('all')
const showProjectModal = ref(false)
const selectedProjectName = ref('')

// 报告归档
const reportList = ref<Report[]>([])
const reportLoading = ref(false)

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

const timePeriods = [
  { label: '今日', value: 'daily' },
  { label: '本周', value: 'weekly' },
  { label: '本月', value: 'monthly' },
  { label: '全年', value: 'yearly' }
]

const categories = ref<string[]>(['all'])
const loadingDomains = ref(false)

// 加载技术领域分类
const loadTechDomains = async () => {
  loadingDomains.value = true
  try {
    const domains = await reportApi.getTechDomains()
    if (domains && domains.length > 0) {
      categories.value = ['all', ...domains.map(d => d.name)]
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
