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
      <div class="mb-6">
        <p class="section-kicker">TRENDING ANALYSIS</p>
        <h2 class="text-3xl font-semibold text-slate-100">趋势分析</h2>
        <p class="mt-2 text-slate-400 max-w-2xl">
          基于历史分析数据的项目趋势，展示近期高频出现与快速增长的开源项目
        </p>
      </div>

      <!-- 时间范围 + 子标签 -->
      <div class="mb-6 flex gap-2 flex-wrap">
        <button
          @click="activeTab = 'frequent'"
          :class="['terminal-action', activeTab === 'frequent' ? 'primary' : '']"
        >
          <svg class="w-4 h-4 mr-1.5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
          </svg>
          高频项目
        </button>
        <button
          @click="activeTab = 'surging'"
          :class="['terminal-action', activeTab === 'surging' ? 'primary' : '']"
        >
          <svg class="w-4 h-4 mr-1.5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path>
          </svg>
          上升最快
        </button>

        <div class="flex gap-2 ml-auto">
          <button
            v-for="d in dayOptions"
            :key="d.value"
            @click="selectedDays = d.value; loadData()"
            :class="['terminal-action text-xs', selectedDays === d.value ? 'primary' : '']"
          >
            {{ d.label }}
          </button>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="terminal-loading">
        <div class="spinner"></div>
        <p class="text-slate-400 mt-4">正在分析趋势数据...</p>
      </div>

      <!-- 高频项目 -->
      <div v-else-if="activeTab === 'frequent'" class="space-y-4">
        <div
          v-for="(project, index) in frequentProjects"
          :key="project.name"
          class="terminal-panel p-4 flex items-center gap-4 cursor-pointer hover:border-cyan-400/30 transition-colors"
          @click="viewProjectDetails(project)"
        >
          <div class="w-10 h-10 rounded-lg bg-cyan-400/10 border border-cyan-400/30 flex items-center justify-center text-cyan-300 font-bold text-lg flex-shrink-0">
            {{ index + 1 }}
          </div>
          <div class="flex-1 min-w-0">
            <ProjectCard :project="project" />
          </div>
          <div class="flex-shrink-0 text-right">
            <div class="text-lg font-semibold text-cyan-300">{{ project.count || project.avg_stars || 0 }}</div>
            <div class="text-[10px] text-slate-500 uppercase">次上榜</div>
          </div>
        </div>
        <div v-if="frequentProjects.length === 0" class="terminal-empty">
          <p class="text-slate-500">暂无高频项目数据，请等待更多分析报告生成</p>
        </div>
      </div>

      <!-- 上升最快 -->
      <div v-else-if="activeTab === 'surging'" class="space-y-4">
        <div
          v-for="(project, index) in surgingProjects"
          :key="project.name"
          class="terminal-panel p-4 flex items-center gap-4 cursor-pointer hover:border-cyan-400/30 transition-colors"
          @click="viewProjectDetails(project)"
        >
          <div class="w-10 h-10 rounded-lg bg-green-400/10 border border-green-400/30 flex items-center justify-center text-green-300 font-bold text-lg flex-shrink-0">
            {{ index + 1 }}
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-base font-semibold text-slate-100">{{ project.name }}</h3>
            <p class="text-sm text-slate-400 mt-0.5 line-clamp-1">{{ project.description }}</p>
            <div class="flex items-center gap-3 mt-1.5 text-xs text-slate-500">
              <span v-if="project.language" class="text-cyan-400">{{ project.language }}</span>
              <span>⭐ {{ formatNumber(project.end_stars || project.stars || 0) }}</span>
            </div>
          </div>
          <div class="flex-shrink-0 text-right">
            <div class="text-lg font-semibold text-green-300">+{{ formatNumber(project.star_increase || 0) }}</div>
            <div class="text-[10px] text-slate-500 uppercase">⭐ 增长</div>
          </div>
        </div>
        <div v-if="surgingProjects.length === 0" class="terminal-empty">
          <p class="text-slate-500">暂无上升最快数据，请等待更多分析报告生成</p>
        </div>
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
import { ref, onMounted } from 'vue'
import { reportApi, type Project, type TrendsData } from '@/api/reports'
import ProjectCard from '@/components/ProjectCard.vue'
import ProjectModal from '@/components/ProjectModal.vue'

const activeTab = ref<'frequent' | 'surging'>('frequent')
const selectedDays = ref(7)
const loading = ref(false)
const showProjectModal = ref(false)
const selectedProjectName = ref('')

const dayOptions = [
  { label: '7天', value: 7 },
  { label: '30天', value: 30 },
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

function formatNumber(num: number): string {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(1) + 'k'
  return num.toString()
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
  } catch (e: any) {
    console.error('加载趋势数据失败:', e)
    frequentProjects.value = []
    surgingProjects.value = []
  } finally {
    loading.value = false
  }
}

function viewProjectDetails(project: Project | FrequentProject) {
  selectedProjectName.value = project.name
  showProjectModal.value = true
}

onMounted(loadData)
</script>
