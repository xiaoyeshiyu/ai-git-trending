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
              <router-link to="/rankings" class="text-white border-b-2 border-primary px-3 py-2 text-sm font-medium">排行榜</router-link>
              <router-link to="/trend-analysis" class="text-slate-300 hover:text-white transition-colors px-3 py-2 text-sm font-medium">趋势分析</router-link>
              <router-link to="/favorites" class="text-slate-300 hover:text-white transition-colors px-3 py-2 text-sm font-medium">收藏</router-link>
            </nav>
          </div>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 页面标题 -->
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-white mb-4">GitHub项目排行榜</h2>
        <p class="text-slate-400 max-w-2xl mx-auto">
          查看最受欢迎的开源项目，按不同类别和时间段进行排名
        </p>
      </div>

      <!-- 筛选选项 -->
      <div class="mb-8 flex flex-wrap gap-4 justify-center">
        <div class="flex space-x-2">
          <button 
            v-for="period in timePeriods" 
            :key="period.value"
            @click="selectedPeriod = period.value"
            :class="[
              'px-5 py-2 rounded-lg text-sm font-medium transition-all',
              selectedPeriod === period.value 
                ? 'bg-primary text-white' 
                : 'bg-white/10 text-slate-300 hover:bg-white/20'
            ]"
          >
            {{ period.label }}
          </button>
        </div>
        <div class="flex space-x-2">
          <button 
            v-for="category in categories" 
            :key="category"
            @click="selectedCategory = category"
            :class="[
              'px-5 py-2 rounded-lg text-sm font-medium transition-all',
              selectedCategory === category 
                ? 'bg-white/10 text-white border border-white/20' 
                : 'bg-white/5 text-slate-300 hover:bg-white/10 border border-transparent'
            ]"
          >
            {{ category }}
          </button>
        </div>
      </div>

      <!-- 项目列表 -->
      <div v-if="loading" class="flex justify-center items-center py-16">
        <div class="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>

      <div v-else-if="projects.length === 0" class="text-center py-20">
        <i class="fa fa-trophy text-6xl text-slate-700 mb-4"></i>
        <h3 class="text-xl font-semibold text-slate-400 mb-2">暂无排名数据</h3>
        <p class="text-slate-500">请尝试选择其他时间段或分类</p>
      </div>

      <div v-else class="space-y-4">
        <div 
          v-for="(project, index) in projects"
          :key="project.name"
          class="bg-white/5 backdrop-blur-sm rounded-xl p-5 border border-white/10 hover:bg-white/10 transition-colors"
        >
          <div class="flex items-center">
            <!-- 排名 -->
            <div class="w-10 h-10 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center text-white font-bold text-lg mr-4">
              {{ index + 1 }}
            </div>
            
            <!-- 项目卡片 -->
            <div class="flex-1 cursor-pointer" @click="viewProjectDetails(project)">
              <ProjectCard :project="project" />
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProjectsByDate, type Project } from '@/api/reports'
import ProjectCard from '@/components/ProjectCard.vue'
import ProjectModal from '@/components/ProjectModal.vue'

const router = useRouter()

const loading = ref(false)
const projects = ref<Project[]>([])
const selectedPeriod = ref('weekly')
const selectedCategory = ref('all')
const showProjectModal = ref(false)
const selectedProjectName = ref('')

const timePeriods = [
  { label: '今日', value: 'daily' },
  { label: '本周', value: 'weekly' },
  { label: '本月', value: 'monthly' },
  { label: '全年', value: 'yearly' }
]

const categories = ['all', 'AI', 'Web', 'Mobile', 'DevOps', 'Data Science']

const loadProjects = async () => {
  loading.value = true
  try {
    const date = new Date().toISOString().split('T')[0]
    const data = await getProjectsByDate(date)
    // 模拟排名数据，按照stars排序
    projects.value = [...data].sort((a, b) => (b.stars || 0) - (a.stars || 0)).slice(0, 20)
  } catch (error) {
    console.error('Failed to load projects:', error)
  } finally {
    loading.value = false
  }
}

const viewProjectDetails = (project: Project) => {
  selectedProjectName.value = project.name
  showProjectModal.value = true
}

// 监听筛选条件变化
selectedPeriod.value = 'weekly'
selectedCategory.value = 'all'

// 初始加载数据
onMounted(() => {
  loadProjects()
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