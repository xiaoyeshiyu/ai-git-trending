<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
    <!-- 顶部导航栏 -->
    <header class="bg-slate-800/80 backdrop-blur-sm border-b border-white/10 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0 flex items-center">
              <div class="w-8 h-8 bg-gradient-to-r from-primary to-secondary rounded-lg flex items-center justify-center">
                <i class="fa fa-github text-white text-lg"></i>
              </div>
              <h1 class="ml-3 text-xl font-bold text-white">
                GitTrend Insights
              </h1>
            </div>
            <nav class="ml-8 hidden md:flex space-x-8">
              <router-link to="/" class="text-slate-300 hover:text-white transition-colors px-3 py-2 text-sm font-medium">发现</router-link>
              <router-link to="/rankings" class="text-slate-300 hover:text-white transition-colors px-3 py-2 text-sm font-medium">排行榜</router-link>
              <router-link to="/trend-analysis" class="text-slate-300 hover:text-white transition-colors px-3 py-2 text-sm font-medium">趋势分析</router-link>
              <router-link to="/favorites" class="text-white border-b-2 border-primary px-3 py-2 text-sm font-medium">收藏</router-link>
            </nav>
          </div>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 页面标题 -->
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-white mb-4">我的收藏项目</h2>
        <p class="text-slate-400 max-w-2xl mx-auto">
          管理和浏览你收藏的GitHub开源项目
        </p>
      </div>

      <!-- 未登录状态 -->
      <div v-if="!isLoggedIn" class="max-w-2xl mx-auto py-16 text-center">
        <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-white/10 mb-6">
          <i class="fa fa-lock text-3xl text-white/70"></i>
        </div>
        <h3 class="text-xl font-bold text-white mb-3">请先登录</h3>
        <p class="text-slate-400 mb-8">登录后即可查看和管理您的收藏项目</p>
        <button class="bg-primary hover:bg-primary/90 text-white font-medium py-3 px-8 rounded-lg transition-colors" @click="handleLogin">
          <i class="fa fa-user mr-2"></i>立即登录
        </button>
      </div>

      <!-- 已登录状态下显示内容 -->
      <div v-else>
        <!-- 搜索栏 -->
        <div class="mb-8">
          <div class="relative max-w-2xl mx-auto">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="搜索收藏的项目..."
              class="w-full px-6 py-4 text-lg border-2 border-white/10 bg-white/5 rounded-2xl focus:outline-none focus:border-primary transition-colors pl-14"
            >
            <i class="fa fa-search absolute left-5 top-1/2 transform -translate-y-1/2 text-slate-400 text-lg"></i>
          </div>
        </div>

        <!-- 筛选选项 -->
        <div class="mb-8 flex flex-wrap gap-4 justify-center">
          <button 
            v-for="category in categories" 
            :key="category"
            @click="selectedCategory = category"
            :class="[
              'px-6 py-2 rounded-full text-sm font-medium transition-all',
              selectedCategory === category 
                ? 'bg-primary text-white shadow-lg' 
                : 'bg-white/10 text-slate-300 hover:bg-white/20 border border-white/10'
            ]"
          >
            {{ category }}
          </button>
        </div>

        <!-- 统计信息 -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <div class="text-sm text-slate-400 mb-2">收藏总数</div>
            <div class="text-3xl font-bold text-white">{{ favorites.length }}</div>
          </div>
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <div class="text-sm text-slate-400 mb-2">语言种类</div>
            <div class="text-3xl font-bold text-primary">{{ uniqueLanguages }}</div>
          </div>
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <div class="text-sm text-slate-400 mb-2">热门语言</div>
            <div class="text-lg font-bold text-white">{{ topLanguage || '暂无' }}</div>
          </div>
          <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
            <div class="text-sm text-slate-400 mb-2">总星标数</div>
            <div class="text-lg font-bold text-white">{{ totalStars }}</div>
          </div>
        </div>

        <!-- 项目列表 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div 
            v-for="(project, index) in filteredProjects" 
            :key="index"
            class="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 overflow-hidden transition-all hover:shadow-lg hover:border-white/20"
          >
            <!-- 项目图片/图标 -->
            <div class="h-32 bg-gradient-to-br from-slate-800 to-slate-900 flex items-center justify-center">
              <div class="w-16 h-16 bg-white/10 rounded-lg flex items-center justify-center">
                <i class="fa fa-github text-white text-3xl"></i>
              </div>
            </div>

            <!-- 项目信息 -->
            <div class="p-6">
              <div class="mb-3">
                <h3 class="font-bold text-white text-lg mb-2 line-clamp-1">
                  {{ getProjectDisplayName(project.name) }}
                </h3>
                <p class="text-slate-400 text-sm line-clamp-3 leading-relaxed">
                  {{ project.description || '暂无描述' }}
                </p>
              </div>

              <!-- 项目标签 -->
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <span 
                    v-if="project.language"
                    class="px-2 py-1 text-xs rounded-full font-medium language-tag"
                    :class="getLanguageStyle(project.language)"
                  >
                    {{ project.language }}
                  </span>
                </div>

                <div class="flex items-center text-sm text-slate-500">
                  <i class="fa fa-code-fork mr-1"></i>
                  {{ formatNumber(project.forks) }}
                </div>
              </div>

              <!-- 更新时间 -->
              <div class="mt-4 pt-4 border-t border-white/10">
                <div class="text-xs text-slate-500">
                  更新于 {{ formatDate(project.updated_at) }}
                </div>
              </div>
            </div>
          </div>
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
import { useRouter } from 'vue-router'
import { getProjectsByDate, type Project } from '@/api/reports'
import ProjectModal from '@/components/ProjectModal.vue'

const router = useRouter()

const loading = ref(false)
const favorites = ref<Project[]>([])
const searchQuery = ref('')
const selectedCategory = ref('all')
const showProjectModal = ref(false)
const selectedProjectName = ref('')
const isLoggedIn = ref(false)

const categories = ['all', 'AI', 'Web', 'Mobile', 'DevOps', 'Data Science']

// 检查用户登录状态
const checkLoginStatus = () => {
  // 这里模拟从localStorage检查登录状态
  // 在实际应用中，可能需要通过API验证token或会话
  const userData = localStorage.getItem('userData')
  isLoggedIn.value = !!userData
}

// 处理登录
const handleLogin = () => {
  // 在实际应用中，这里应该跳转到登录页面
  // 现在我们只是模拟登录成功
  localStorage.setItem('userData', JSON.stringify({ loggedIn: true }))
  isLoggedIn.value = true
  loadFavorites()
}

// 加载收藏数据
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

// 保存收藏数据
const saveFavorites = () => {
  localStorage.setItem('favorites', JSON.stringify(favorites.value))
}

// 移除收藏
const removeFavorite = (index: number) => {
  favorites.value.splice(index, 1)
  saveFavorites()
}

// 查看项目详情
const viewProjectDetails = (projectName: string) => {
  selectedProjectName.value = projectName
  showProjectModal.value = true
}

// 打开项目URL
const openProjectUrl = (projectUrl: string) => {
  window.open(projectUrl, '_blank')
}

// 获取项目显示名称
const getProjectDisplayName = (name: string): string => {
  if (name.includes('/')) {
    return name.split('/')[1]
  }
  return name
}

// 格式化数字
const formatNumber = (num: number | undefined): string => {
  if (!num || num === 0) return '0'
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}

// 格式化日期
const formatDate = (dateStr: string | undefined): string => {
  if (!dateStr || dateStr === 'N/A') return '未知'
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN')
  } catch {
    return '未知'
  }
}

// 获取语言样式
const getLanguageStyle = (language: string): string => {
  const styles: Record<string, string> = {
    JavaScript: 'bg-yellow-100 text-yellow-800',
    TypeScript: 'bg-blue-100 text-blue-800',
    Python: 'bg-blue-100 text-blue-800',
    Java: 'bg-red-100 text-red-800',
    Go: 'bg-blue-100 text-blue-800',
    Rust: 'bg-orange-100 text-orange-800',
    Ruby: 'bg-red-100 text-red-800',
    PHP: 'bg-purple-100 text-purple-800',
    C: 'bg-blue-100 text-blue-800',
    'C++': 'bg-blue-100 text-blue-800',
    'C#': 'bg-purple-100 text-purple-800',
    Swift: 'bg-orange-100 text-orange-800',
    Kotlin: 'bg-blue-100 text-blue-800',
    Dart: 'bg-blue-100 text-blue-800',
    HTML: 'bg-orange-100 text-orange-800',
    CSS: 'bg-blue-100 text-blue-800'
  }
  return styles[language] || 'bg-gray-100 text-gray-800'
}

// 计算过滤后的项目
const filteredProjects = computed(() => {
  let result = favorites.value
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(project => 
      project.name.toLowerCase().includes(query) ||
      project.description?.toLowerCase().includes(query) ||
      project.language?.toLowerCase().includes(query)
    )
  }
  
  // 分类过滤
  if (selectedCategory.value !== 'all') {
    result = result.filter(project => 
      project.language?.toLowerCase().includes(selectedCategory.value.toLowerCase()) ||
      project.description?.toLowerCase().includes(selectedCategory.value.toLowerCase())
    )
  }
  
  return result
})

// 计算唯一语言数量
const uniqueLanguages = computed(() => {
  const languages = new Set(favorites.value.map(project => project.language).filter(lang => lang))
  return languages.size
})

// 计算顶级语言
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

// 计算总星标数
const totalStars = computed(() => {
  return formatNumber(favorites.value.reduce((sum, project) => sum + (project.stars || 0), 0))
})

// 初始化加载收藏数据
onMounted(() => {
  checkLoginStatus()
  
  if (isLoggedIn.value) {
    loadFavorites()
    
    // 如果没有收藏数据，使用模拟数据
    if (favorites.value.length === 0) {
      // 使用模拟数据填充收藏列表
      loading.value = true
      try {
        const date = new Date().toISOString().split('T')[0]
        getProjectsByDate(date).then(data => {
          // 随机选择几个项目作为模拟收藏
          const mockFavorites = data.slice(0, 3)
          favorites.value = mockFavorites
          saveFavorites()
        })
      } catch (error) {
        console.error('Failed to load mock favorites:', error)
      } finally {
        loading.value = false
      }
    }
  }
})
</script>

<style scoped>
/* 自定义样式 */
.language-tag {
  background-color: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}
</style>