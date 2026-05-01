<template>
  <div class="terminal-page">
    <!-- 顶部导航栏 -->
    <header class="terminal-header">
      <div class="mx-auto flex max-w-[1500px] items-center justify-between px-4 py-3 lg:px-6">
        <div class="flex items-center gap-3">
          <button
            @click="$router.go(-1)"
            class="p-2 rounded-lg hover:bg-cyan-400/10 transition-colors"
          >
            <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          <div class="flex h-9 w-9 items-center justify-center border border-cyan-400/30 bg-cyan-400/10 text-cyan-300">
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
          </div>
          <div>
            <h1 class="text-sm font-semibold text-slate-100">{{ displayDate }} 热门项目</h1>
            <p class="text-[10px] text-slate-500">{{ projectCount }} 个项目</p>
          </div>
        </div>

        <!-- 筛选和排序 -->
        <div class="flex items-center gap-4">
          <select
            v-model="sortBy"
            class="terminal-select"
          >
            <option value="stars">按 Stars 排序</option>
            <option value="forks">按 Forks 排序</option>
            <option value="contributors">按贡献者排序</option>
            <option value="name">按名称排序</option>
          </select>
          <div class="relative">
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索项目..."
              class="terminal-search pl-10"
            >
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容 -->
    <main class="terminal-main">
      <!-- 加载状态 -->
      <div v-if="loading" class="terminal-loading">
        <div class="spinner"></div>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="terminal-empty">
        <svg class="text-red-400 w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
        </svg>
        <h3 class="text-lg font-medium text-red-400 mb-2">加载失败</h3>
        <p class="text-slate-500 mb-4">{{ error }}</p>
        <button class="terminal-action primary" @click="loadProjects">
          重试
        </button>
      </div>

      <!-- 项目网格 -->
      <div v-else-if="filteredProjects.length > 0">
        <!-- 统计信息 -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div class="terminal-metric">
            <span>项目总数</span>
            <strong>{{ projectCount }}</strong>
          </div>
          <div class="terminal-metric">
            <span>平均 Stars</span>
            <strong>{{ averageStars }}</strong>
          </div>
          <div class="terminal-metric">
            <span>最多语言</span>
            <strong>{{ topLanguage }}</strong>
          </div>
          <div class="terminal-metric">
            <span>总 Forks</span>
            <strong>{{ totalForks }}</strong>
          </div>
        </div>

        <!-- 项目卡片网格 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <ProjectCard
            v-for="(project, index) in filteredProjects"
            :key="project.name"
            :project="project"
            :index="index"
            @click="handleProjectClick"
          />
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="terminal-empty">
        <svg class="w-16 h-16 text-slate-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
        </svg>
        <p class="text-slate-500">未找到项目</p>
      </div>
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
import { useRoute } from 'vue-router'
import ProjectCard from '@/components/ProjectCard.vue'
import ProjectModal from '@/components/ProjectModal.vue'
import { getProjectsByDate, type Project } from '@/api/reports'

const route = useRoute()

const loading = ref(false)
const error = ref('')
const projects = ref<Project[]>([])
const searchQuery = ref('')
const sortBy = ref('stars')
const showProjectModal = ref(false)
const selectedProjectName = ref('')

const date = computed(() => route.params.date as string)

const displayDate = computed(() => {
  try {
    const dateObj = new Date(date.value)
    return dateObj.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'long'
    })
  } catch {
    return date.value
  }
})

const filteredProjects = computed(() => {
  let result = [...projects.value]

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(project =>
      project.name.toLowerCase().includes(query) ||
      (project.description && project.description.toLowerCase().includes(query)) ||
      (project.language && project.language.toLowerCase().includes(query))
    )
  }

  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'stars':
        return Number(b.stars || 0) - Number(a.stars || 0)
      case 'forks':
        return Number(b.forks || 0) - Number(a.forks || 0)
      case 'contributors':
        return Number(b.contributor_count || 0) - Number(a.contributor_count || 0)
      case 'name':
        return a.name.localeCompare(b.name)
      default:
        return 0
    }
  })

  return result
})

const projectCount = computed(() => projects.value.length)

const averageStars = computed(() => {
  if (projects.value.length === 0) return '0'
  const total = projects.value.reduce((sum, project) => sum + Number(project.stars || 0), 0)
  const avg = total / projects.value.length
  return avg >= 1000 ? `${(avg / 1000).toFixed(1)}K` : Math.round(avg).toString()
})

const topLanguage = computed(() => {
  const languageCount = projects.value.reduce((acc, project) => {
    if (project.language && project.language !== 'N/A') {
      acc[project.language] = (acc[project.language] || 0) + 1
    }
    return acc
  }, {} as Record<string, number>)

  const sortedLanguages = Object.entries(languageCount).sort(([, a], [, b]) => b - a)
  return sortedLanguages[0]?.[0] || 'N/A'
})

const totalForks = computed(() => {
  const total = projects.value.reduce((sum, project) => sum + Number(project.forks || 0), 0)
  return total >= 1000 ? `${(total / 1000).toFixed(1)}K` : total.toString()
})

const loadProjects = async () => {
  if (!date.value) return

  loading.value = true
  error.value = ''

  try {
    projects.value = await getProjectsByDate(date.value)
  } catch (err) {
    error.value = '加载项目列表失败'
    console.error('Failed to load projects:', err)
  } finally {
    loading.value = false
  }
}

const handleProjectClick = (project: Project) => {
  selectedProjectName.value = project.name
  showProjectModal.value = true
}

watch(() => route.params.date, loadProjects, { immediate: true })

onMounted(() => {
  loadProjects()
})
</script>
