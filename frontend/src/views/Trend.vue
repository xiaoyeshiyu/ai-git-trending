<template>
  <div class="terminal-page">
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
            <p class="text-[10px] uppercase tracking-[0.26em] text-cyan-400/70">TECH INTELLIGENCE TERMINAL</p>
          </div>
        </div>
        <nav class="hidden items-center gap-1 md:flex">
          <router-link to="/" class="terminal-nav">情报台</router-link>
          <router-link to="/trend" class="terminal-nav active">趋势</router-link>
          <router-link to="/rankings" class="terminal-nav">排行榜</router-link>
          <router-link to="/trend-analysis" class="terminal-nav">趋势图谱</router-link>
          <router-link to="/favorites" class="terminal-nav">收藏</router-link>
        </nav>
      </div>
    </header>

    <main class="terminal-main">
      <!-- 页头 -->
      <div class="mb-6">
        <p class="section-kicker">TRENDING ANALYSIS</p>
        <h2 class="text-3xl font-semibold text-slate-100">趋势分析</h2>
        <p class="mt-2 text-slate-400 max-w-2xl">基于历史分析数据的项目趋势，展示近期高频出现与快速增长的开源项目</p>
      </div>

      <!-- 控制栏 -->
      <div class="mb-6 flex gap-2 flex-wrap items-center">
        <button @click="activeTab = 'frequent'" :class="['terminal-action', activeTab === 'frequent' ? 'primary' : '']">
          <svg class="w-4 h-4 mr-1.5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
          </svg>
          高频项目
        </button>
        <button @click="activeTab = 'surging'" :class="['terminal-action', activeTab === 'surging' ? 'primary' : '']">
          <svg class="w-4 h-4 mr-1.5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path>
          </svg>
          上升最快
        </button>
        <div class="flex gap-2 ml-auto">
          <button
            v-for="d in dayOptions" :key="d.value"
            @click="selectedDays = d.value; loadData()"
            :class="['terminal-action text-xs', selectedDays === d.value ? 'primary' : '']"
          >{{ d.label }}</button>
        </div>
      </div>

      <!-- 主内容：列表 + 右侧面板 -->
      <div class="grid gap-6 lg:grid-cols-[1fr_280px]">

        <!-- 左：项目列表 -->
        <div>
          <div v-if="loading" class="terminal-loading">
            <div class="spinner"></div>
            <p class="text-slate-400 mt-4">正在分析趋势数据...</p>
          </div>

          <!-- 高频项目 -->
          <div v-else-if="activeTab === 'frequent'" class="space-y-2">
            <div
              v-for="(project, index) in frequentProjects" :key="project.name"
              class="terminal-panel px-4 py-3 flex items-center gap-4 cursor-pointer hover:border-cyan-400/30 transition-colors"
              @click="viewProjectDetails(project)"
            >
              <!-- 排名 -->
              <span class="text-sm font-mono text-slate-500 w-5 shrink-0 text-right">{{ index + 1 }}</span>

              <!-- 项目信息 -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-sm font-semibold text-slate-100 truncate">{{ project.name }}</span>
                  <span v-if="project.language" class="text-[10px] px-1.5 py-0.5 border border-slate-700 text-slate-400 shrink-0">{{ project.language }}</span>
                </div>
                <p class="text-xs text-slate-500 truncate">{{ project.description }}</p>
                <!-- 上榜频次进度条 -->
                <div class="mt-2 flex items-center gap-2">
                  <div class="flex-1 h-1 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      class="h-full bg-cyan-400/70 rounded-full transition-all duration-500"
                      :style="{ width: `${Math.round((project.count || 0) / maxFreqCount * 100)}%` }"
                    ></div>
                  </div>
                  <span class="text-[10px] text-slate-500 shrink-0">{{ project.count }} 次 / {{ selectedDays }}天</span>
                </div>
              </div>

              <!-- Star -->
              <div class="shrink-0 text-right">
                <div class="text-sm font-semibold text-slate-300">★ {{ formatNumber(project.stars || project.avg_stars || 0) }}</div>
                <div class="text-[10px] text-slate-600 mt-0.5">{{ project.created_at ? String(project.created_at).slice(0, 4) : '—' }}</div>
              </div>
            </div>

            <div v-if="frequentProjects.length === 0" class="terminal-empty">
              <p class="text-slate-500">暂无高频项目数据，请等待更多分析报告生成</p>
            </div>
          </div>

          <!-- 上升最快 -->
          <div v-else-if="activeTab === 'surging'" class="space-y-2">
            <div
              v-for="(project, index) in surgingProjects" :key="project.name"
              class="terminal-panel px-4 py-3 flex items-center gap-4 cursor-pointer hover:border-cyan-400/30 transition-colors"
              @click="viewProjectDetails(project)"
            >
              <!-- 排名 -->
              <span class="text-sm font-mono text-slate-500 w-5 shrink-0 text-right">{{ index + 1 }}</span>

              <!-- 项目信息 -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-sm font-semibold text-slate-100 truncate">{{ project.name }}</span>
                  <span v-if="project.language" class="text-[10px] px-1.5 py-0.5 border border-slate-700 text-slate-400 shrink-0">{{ project.language }}</span>
                </div>
                <p class="text-xs text-slate-500 truncate">{{ project.description }}</p>
                <!-- Star 增长进度条 -->
                <div class="mt-2 flex items-center gap-2">
                  <div class="flex-1 h-1 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      class="h-full bg-green-400/70 rounded-full transition-all duration-500"
                      :style="{ width: `${Math.round((project.star_increase || 0) / maxSurgeCount * 100)}%` }"
                    ></div>
                  </div>
                  <span class="text-[10px] text-slate-500 shrink-0">
                    {{ formatNumber(project.start_stars || 0) }} → {{ formatNumber(project.end_stars || 0) }}
                  </span>
                </div>
              </div>

              <!-- 增量 -->
              <div class="shrink-0 text-right">
                <div class="text-sm font-semibold text-green-300">+{{ formatNumber(project.star_increase || 0) }}</div>
                <div class="text-[10px] text-slate-600 mt-0.5">★ 增长</div>
              </div>
            </div>

            <div v-if="surgingProjects.length === 0" class="terminal-empty">
              <p class="text-slate-500">暂无上升最快数据，请等待更多分析报告生成</p>
            </div>
          </div>
        </div>

        <!-- 右：摘要面板 -->
        <aside class="space-y-4">
          <!-- 语言分布 -->
          <div class="terminal-panel">
            <div class="terminal-panel-head">
              <span>LANGUAGE DIST.</span>
              <span class="text-xs text-slate-500">{{ selectedDays }}天 Top {{ topLanguages.length }}</span>
            </div>
            <div class="px-4 py-3 space-y-3">
              <div v-for="lang in topLanguages" :key="lang.name">
                <div class="flex justify-between text-xs mb-1">
                  <span class="text-slate-300">{{ lang.name }}</span>
                  <span class="text-slate-500">{{ lang.count }} 次</span>
                </div>
                <div class="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    class="h-full rounded-full transition-all duration-500"
                    :class="lang.colorClass"
                    :style="{ width: `${lang.pct}%` }"
                  ></div>
                </div>
              </div>
              <p v-if="topLanguages.length === 0" class="text-xs text-slate-500 text-center py-2">加载中...</p>
            </div>
          </div>

          <!-- 技术领域 -->
          <div class="terminal-panel">
            <div class="terminal-panel-head">
              <span>TECH DOMAINS</span>
              <span class="text-xs text-slate-500">Top {{ techDomains.length }}</span>
            </div>
            <div class="px-4 py-3 space-y-2">
              <div v-for="domain in techDomains" :key="domain.name" class="flex items-center justify-between">
                <span class="text-xs text-slate-300">{{ domain.name }}</span>
                <div class="flex items-center gap-2">
                  <div class="w-20 h-1 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      class="h-full bg-purple-400/60 rounded-full"
                      :style="{ width: `${domain.percentage}%` }"
                    ></div>
                  </div>
                  <span class="text-[10px] text-slate-500 w-8 text-right">{{ domain.percentage }}%</span>
                </div>
              </div>
              <p v-if="techDomains.length === 0" class="text-xs text-slate-500 text-center py-2">加载中...</p>
            </div>
          </div>

          <!-- 快速统计 -->
          <div class="terminal-panel">
            <div class="terminal-panel-head"><span>QUICK STATS</span></div>
            <div class="px-4 py-3 space-y-2">
              <div class="flex justify-between text-xs">
                <span class="text-slate-400">分析时间跨度</span>
                <span class="text-slate-200">{{ selectedDays }} 天</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="text-slate-400">高频项目数</span>
                <span class="text-slate-200">{{ frequentProjects.length }}</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="text-slate-400">最高上榜次数</span>
                <span class="text-cyan-300">{{ maxFreqCount }} 次</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="text-slate-400">最大 Star 增量</span>
                <span class="text-green-300">+{{ formatNumber(maxSurgeCount) }}</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </main>

    <ProjectModal
      :visible="showProjectModal"
      :project-name="selectedProjectName"
      @close="showProjectModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { reportApi, type Project, type TrendsData } from '@/api/reports'
import ProjectModal from '@/components/ProjectModal.vue'

const activeTab = ref<'frequent' | 'surging'>('frequent')
const selectedDays = ref(7)
const loading = ref(false)
const showProjectModal = ref(false)
const selectedProjectName = ref('')

const dayOptions = [
  { label: '7天', value: 7 },
  { label: '30天', value: 30 },
  { label: '180天', value: 182 },
]

const LANG_COLORS = [
  'bg-cyan-400',
  'bg-blue-400',
  'bg-green-400',
  'bg-yellow-400',
  'bg-purple-400',
  'bg-orange-400',
  'bg-pink-400',
  'bg-teal-400',
]

interface FrequentProject extends Project {
  count?: number
  avg_stars?: number
}

interface SurgingProject {
  name: string
  url?: string
  description?: string
  language?: string
  star_increase: number
  start_stars?: number
  end_stars?: number
  stars?: number
}

const frequentProjects = ref<FrequentProject[]>([])
const surgingProjects = ref<SurgingProject[]>([])
const rawLanguages = ref<[string, number][]>([])
const rawDomains = ref<{ name: string; count: number; percentage: number }[]>([])

const maxFreqCount = computed(() =>
  frequentProjects.value.reduce((m, p) => Math.max(m, p.count || 0), 1)
)
const maxSurgeCount = computed(() =>
  surgingProjects.value.reduce((m, p) => Math.max(m, p.star_increase || 0), 1)
)

const topLanguages = computed(() => {
  const total = rawLanguages.value.reduce((s, [, c]) => s + c, 0) || 1
  return rawLanguages.value.slice(0, 8).map(([name, count], i) => ({
    name,
    count,
    pct: Math.round((count / total) * 100),
    colorClass: LANG_COLORS[i % LANG_COLORS.length],
  }))
})

const techDomains = computed(() => rawDomains.value.slice(0, 5))

function formatNumber(num: number): string {
  if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + 'M'
  if (num >= 1_000) return (num / 1_000).toFixed(1) + 'k'
  return String(num)
}

async function loadData() {
  loading.value = true
  try {
    const trends: TrendsData = await reportApi.getTrends({ days: selectedDays.value })

    frequentProjects.value = (trends.most_frequent_projects || []).map(p => ({
      name: p.name,
      url: p.url || `https://github.com/${p.name}`,
      description: p.description || '',
      language: p.language || '',
      stars: p.stars || p.avg_stars || 0,
      forks: p.forks || 0,
      contributor_count: p.contributor_count || 0,
      created_at: p.created_at || '',
      updated_at: p.updated_at || '',
      open_issues: p.open_issues || 0,
      watchers: p.watchers || 0,
      count: (p as any).count || 0,
      avg_stars: p.avg_stars || 0,
    }))

    surgingProjects.value = (trends.surgingProjects || []).map(p => ({
      ...p,
      stars: (p as any).stars || p.end_stars || 0,
    }))

    rawLanguages.value = trends.most_frequent_languages || []
    rawDomains.value = trends.techDomains || []
  } catch (e) {
    console.error('加载趋势数据失败:', e)
    frequentProjects.value = []
    surgingProjects.value = []
  } finally {
    loading.value = false
  }
}

function viewProjectDetails(project: { name: string }) {
  selectedProjectName.value = project.name
  showProjectModal.value = true
}

onMounted(loadData)
</script>
