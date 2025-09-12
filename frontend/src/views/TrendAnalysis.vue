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
              <router-link to="/trend-analysis" class="text-white border-b-2 border-primary px-3 py-2 text-sm font-medium">趋势分析</router-link>
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
        <h2 class="text-3xl font-bold text-white mb-4">开源项目趋势分析</h2>
        <p class="text-slate-400 max-w-2xl mx-auto">
          探索技术发展趋势，发现新兴项目和热门技术领域
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
            v-for="analysisType in analysisTypes" 
            :key="analysisType.value"
            @click="selectedAnalysisType = analysisType.value"
            :class="[
              'px-5 py-2 rounded-lg text-sm font-medium transition-all',
              selectedAnalysisType === analysisType.value 
                ? 'bg-white/10 text-white border border-white/20' 
                : 'bg-white/5 text-slate-300 hover:bg-white/10 border border-transparent'
            ]"
          >
            {{ analysisType.label }}
          </button>
        </div>
      </div>

      <!-- 统计图表区域 -->
      <div v-if="loading" class="flex justify-center items-center py-16">
        <div class="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      </div>

      <div v-else class="space-y-8">
        <!-- 语言趋势图 -->
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <h3 class="text-xl font-bold text-white mb-6">技术语言趋势</h3>
          <div class="h-80 bg-slate-800/30 rounded-lg flex items-center justify-center">
            <p class="text-slate-400">图表数据加载中...</p>
          </div>
        </div>

        <!-- 热门领域趋势 -->
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <h3 class="text-xl font-bold text-white mb-6">热门技术领域</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="h-80 bg-slate-800/30 rounded-lg flex items-center justify-center">
              <p class="text-slate-400">图表数据加载中...</p>
            </div>
            <div class="h-80 bg-slate-800/30 rounded-lg flex items-center justify-center">
              <p class="text-slate-400">图表数据加载中...</p>
            </div>
          </div>
        </div>

        <!-- 趋势项目列表 -->
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <h3 class="text-xl font-bold text-white mb-6">新兴趋势项目</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ProjectCard 
              v-for="(project, index) in trendingProjects" 
              :key="project.name"
              :project="project"
              :index="index"
              @click="viewProjectDetails(project)"
            />
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
const selectedPeriod = ref('monthly')
const selectedAnalysisType = ref('language')
const trendingProjects = ref<Project[]>([])
const showProjectModal = ref(false)
const selectedProjectName = ref('')

const timePeriods = [
  { label: '本周', value: 'weekly' },
  { label: '本月', value: 'monthly' },
  { label: '全年', value: 'yearly' }
]

const analysisTypes = [
  { label: '语言趋势', value: 'language' },
  { label: '领域分布', value: 'domain' },
  { label: '增长速度', value: 'growth' }
]

// 模拟图表数据
const languageData = ref({
  labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
  datasets: [
    {
      label: 'JavaScript',
      data: [65, 59, 80, 81, 56, 55],
      borderColor: '#F7DF1E',
      backgroundColor: 'rgba(247, 223, 30, 0.1)',
      tension: 0.4
    },
    {
      label: 'Python',
      data: [28, 48, 40, 45, 86, 95],
      borderColor: '#3776AB',
      backgroundColor: 'rgba(55, 118, 171, 0.1)',
      tension: 0.4
    },
    {
      label: 'TypeScript',
      data: [45, 32, 46, 50, 58, 70],
      borderColor: '#3178C6',
      backgroundColor: 'rgba(49, 120, 198, 0.1)',
      tension: 0.4
    },
    {
      label: 'Go',
      data: [20, 25, 35, 40, 45, 55],
      borderColor: '#00ADD8',
      backgroundColor: 'rgba(0, 173, 216, 0.1)',
      tension: 0.4
    }
  ]
})

const domainData = ref({
  labels: ['AI/ML', 'Web', 'Mobile', 'DevOps', 'Data Science', 'Blockchain'],
  datasets: [
    {
      label: '项目数量',
      data: [120, 80, 60, 45, 30, 20],
      backgroundColor: [
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 99, 132, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)'
      ]
    }
  ]
})

const domainPieData = ref({
  labels: ['AI/ML', 'Web', 'Mobile', 'DevOps', 'Data Science'],
  datasets: [
    {
      data: [40, 25, 15, 10, 10],
      backgroundColor: [
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 99, 132, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)'
      ]
    }
  ]
})

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#94a3b8'
      }
    }
  },
  scales: {
    y: {
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      },
      ticks: {
        color: '#94a3b8'
      }
    },
    x: {
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      },
      ticks: {
        color: '#94a3b8'
      }
    }
  }
})

const pieChartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right' as const,
      labels: {
        color: '#94a3b8'
      }
    }
  }
})

const loadTrendingProjects = async () => {
  loading.value = true
  try {
    const date = new Date().toISOString().split('T')[0]
    const data = await getProjectsByDate(date)
    // 模拟趋势数据，按照增长率排序
    trendingProjects.value = [...data].sort((a, b) => {
      const growthA = (a.stars || 0) / ((a.created_at ? (new Date().getTime() - new Date(a.created_at).getTime()) / (1000 * 60 * 60 * 24) : 1)) || 0
      const growthB = (b.stars || 0) / ((b.created_at ? (new Date().getTime() - new Date(b.created_at).getTime()) / (1000 * 60 * 60 * 24) : 1)) || 0
      return growthB - growthA
    }).slice(0, 6)
  } catch (error) {
    console.error('Failed to load trending projects:', error)
  } finally {
    loading.value = false
  }
}

const viewProjectDetails = (project: Project) => {
  selectedProjectName.value = project.name
  showProjectModal.value = true
}

// 监听筛选条件变化
const handleFilterChange = () => {
  loadTrendingProjects()
}

// 初始加载数据
onMounted(() => {
  loadTrendingProjects()
})
</script>

<style scoped>
/* 自定义图表样式 */
.chart-container {
  position: relative;
  height: 100%;
  width: 100%;
}
</style>