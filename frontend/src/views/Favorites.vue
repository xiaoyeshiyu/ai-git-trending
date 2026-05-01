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
          <router-link to="/rankings" class="terminal-nav">排行榜</router-link>
          <router-link to="/trend-analysis" class="terminal-nav">趋势图谱</router-link>
          <router-link to="/favorites" class="terminal-nav active">收藏</router-link>
        </nav>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="terminal-main">
      <!-- 页面标题 -->
      <div class="mb-8">
        <p class="section-kicker">FAVORITES</p>
        <h2 class="text-3xl font-semibold text-slate-100">我的收藏</h2>
        <p class="mt-2 text-slate-400">
          管理和浏览你收藏的GitHub开源项目
        </p>
      </div>

      <!-- 未登录状态 -->
      <div v-if="!isLoggedIn" class="terminal-empty py-20">
        <svg class="w-16 h-16 text-slate-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
        </svg>
        <h3 class="text-xl font-semibold text-slate-300 mb-3">请先登录</h3>
        <p class="text-slate-500 mb-8">登录后即可查看和管理您的收藏项目</p>
        <button class="terminal-action primary" @click="handleLogin">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
          </svg>
          立即登录
        </button>
      </div>

      <!-- 已登录状态下显示内容 -->
      <div v-else>
        <!-- 搜索栏 -->
        <div class="mb-8">
          <div class="relative max-w-2xl">
            <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索收藏的项目..."
              class="w-full pl-12 pr-4 py-3 terminal-search"
            >
          </div>
        </div>

        <!-- 筛选选项 -->
        <div class="mb-8 flex flex-wrap gap-2">
          <button
            v-for="category in categories"
            :key="category"
            @click="selectedCategory = category"
            :class="[
              'terminal-action',
              selectedCategory === category ? 'primary' : ''
            ]"
          >
            {{ category === 'all' ? '全部' : category }}
          </button>
        </div>

        <!-- 统计信息 -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div class="terminal-metric">
            <span>收藏总数</span>
            <strong>{{ favorites.length }}</strong>
          </div>
          <div class="terminal-metric">
            <span>语言种类</span>
            <strong>{{ uniqueLanguages }}</strong>
          </div>
          <div class="terminal-metric">
            <span>热门语言</span>
            <strong>{{ topLanguage || '-' }}</strong>
          </div>
          <div class="terminal-metric">
            <span>总星标数</span>
            <strong>{{ totalStars }}</strong>
          </div>
        </div>

        <!-- 项目列表 -->
        <div v-if="filteredProjects.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <div
            v-for="(project, index) in filteredProjects"
            :key="index"
            class="terminal-panel overflow-hidden"
          >
            <!-- 项目信息 -->
            <div class="p-5">
              <div class="mb-3">
                <h3 class="font-semibold text-slate-200 text-lg mb-2 line-clamp-1">
                  {{ getProjectDisplayName(project.name) }}
                </h3>
                <p class="text-slate-400 text-sm line-clamp-2 leading-relaxed">
                  {{ project.description || '暂无描述' }}
                </p>
              </div>

              <!-- 项目标签 -->
              <div class="flex items-center justify-between">
                <span
                  v-if="project.language"
                  class="px-2 py-1 text-xs rounded border border-slate-700 text-slate-400"
                >
                  {{ project.language }}
                </span>

                <div class="flex items-center text-sm text-slate-500">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8.75 21V3l8 8m0-8v8m-8 8h16"></path>
                  </svg>
                  {{ formatNumber(project.forks) }}
                </div>
              </div>

              <!-- 更新时间 -->
              <div class="mt-4 pt-4 border-t border-slate-800">
                <div class="text-xs text-slate-500">
                  更新于 {{ formatDate(project.updated_at) }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="terminal-empty">
          <svg class="w-16 h-16 text-slate-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
          </svg>
          <h3 class="text-lg font-medium text-slate-400 mb-2">暂无收藏</h3>
          <p class="text-slate-500">收藏一些项目以便快速访问</p>
        </div>
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
import { ref, computed, onMounted } from 'vue'
import { type Project } from '@/api/reports'
import ProjectModal from '@/components/ProjectModal.vue'

const loading = ref(false)
const favorites = ref<Project[]>([])
const searchQuery = ref('')
const selectedCategory = ref('all')
const showProjectModal = ref(false)
const selectedProjectName = ref('')
const isLoggedIn = ref(false)

const categories = ['all', 'AI', 'Web', 'Mobile', 'DevOps', 'Data Science']

const checkLoginStatus = () => {
  const userData = localStorage.getItem('userData')
  isLoggedIn.value = !!userData
}

const handleLogin = () => {
  localStorage.setItem('userData', JSON.stringify({ loggedIn: true }))
  isLoggedIn.value = true
  loadFavorites()
}

const loadFavorites = () => {
  const storedFavorites = localStorage.getItem('favorites')
  if (storedFavorites) {
    try {
      favorites.value = JSON.parse(storedFavorites)
    } catch (error) {
      console.error('Failed to parse favorites:', error)
      favorites.value = []
    }
  }
}

const saveFavorites = () => {
  localStorage.setItem('favorites', JSON.stringify(favorites.value))
}

const removeFavorite = (index: number) => {
  favorites.value.splice(index, 1)
  saveFavorites()
}

const viewProjectDetails = (projectName: string) => {
  selectedProjectName.value = projectName
  showProjectModal.value = true
}

const openProjectUrl = (projectUrl: string) => {
  window.open(projectUrl, '_blank')
}

const getProjectDisplayName = (name: string): string => {
  if (name.includes('/')) {
    return name.split('/')[1]
  }
  return name
}

const formatNumber = (num: number | undefined): string => {
  if (!num || num === 0) return '0'
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}

const formatDate = (dateStr: string | undefined): string => {
  if (!dateStr || dateStr === 'N/A') return '未知'
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN')
  } catch {
    return '未知'
  }
}

const filteredProjects = computed(() => {
  let result = favorites.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(project =>
      project.name.toLowerCase().includes(query) ||
      project.description?.toLowerCase().includes(query) ||
      project.language?.toLowerCase().includes(query)
    )
  }

  if (selectedCategory.value !== 'all') {
    result = result.filter(project =>
      project.language?.toLowerCase().includes(selectedCategory.value.toLowerCase()) ||
      project.description?.toLowerCase().includes(selectedCategory.value.toLowerCase())
    )
  }

  return result
})

const uniqueLanguages = computed(() => {
  const languages = new Set(favorites.value.map(project => project.language).filter(lang => lang))
  return languages.size
})

const topLanguage = computed(() => {
  const languageCount: Record<string, number> = {}
  favorites.value.forEach(project => {
    if (project.language) {
      languageCount[project.language] = (languageCount[project.language] || 0) + 1
    }
  })

  let maxCount = 0
  let topLang = ''

  Object.entries(languageCount).forEach(([lang, count]) => {
    if (count > maxCount) {
      maxCount = count
      topLang = lang
    }
  })

  return topLang
})

const totalStars = computed(() => {
  return formatNumber(favorites.value.reduce((sum, project) => sum + (project.stars || 0), 0))
})

onMounted(() => {
  checkLoginStatus()

  if (isLoggedIn.value) {
    loadFavorites()
  }
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
