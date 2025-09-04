<template>
  <div class="home-container min-h-screen bg-slate-900 text-slate-100">
    <!-- 顶部导航栏 - 固定在顶部，提供全局入口 -->
    <header class="sticky top-0 z-40 backdrop-blur-lg bg-slate-900/80 border-b border-slate-800/50">
      <div class="container mx-auto px-4 py-3 flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <svg class="w-8 h-8 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <h1 class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500">
            GitTrend Insights
          </h1>
        </div>
        
        <div class="hidden md:flex items-center space-x-6">
          <button class="text-slate-300 hover:text-white transition-colors">发现</button>
          <button class="text-slate-300 hover:text-white transition-colors">排行榜</button>
          <button class="text-slate-300 hover:text-white transition-colors">趋势分析</button>
          <button class="text-slate-300 hover:text-white transition-colors">收藏</button>
        </div>
        
        <div class="flex items-center space-x-3">
          <button class="btn-icon" @click="toggleTheme">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="theme === 'dark'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
            </svg>
          </button>
          <button class="btn-primary">登录</button>
        </div>
      </div>
    </header>

    <!-- 英雄区域 - 突出核心价值 -->
    <section class="relative overflow-hidden bg-gradient-to-b from-slate-800 to-slate-900">
      <div class="absolute inset-0 bg-grid-pattern opacity-10"></div>
      <div class="container mx-auto px-4 py-16 md:py-24 relative z-10">
        <div class="max-w-3xl mx-auto text-center">
          <h2 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 leading-tight animate-fadeIn">
            <span class="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500">
              发现GitHub热门技术趋势
            </span>
          </h2>
          <p class="text-lg text-slate-300 mb-8 animate-fadeInUp" style="animation-delay: 0.2s;">
            每日精选AI与开源领域最具创新性的项目，助您把握技术脉搏，洞察行业前沿
          </p>
          <div class="flex flex-col sm:flex-row justify-center gap-4 animate-fadeInUp" style="animation-delay: 0.4s;">
            <button class="btn-primary text-base py-3 px-8 rounded-xl shadow-lg shadow-primary/20 hover:shadow-xl hover:shadow-primary/30 transition-all"
              @click="viewTodayTrending">
              查看今日热门
            </button>
            <button class="btn-secondary text-base py-3 px-8 rounded-xl">
              <i class="fa fa-bell mr-2"></i>订阅趋势更新
            </button>
          </div>
        </div>
      </div>
      <!-- 波浪装饰 -->
      <div class="absolute bottom-0 left-0 right-0 h-16 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSI1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMCAwaDEwMHY1MEgweiIgZmlsbD0ibm9uZSIvPjxwYXRoIGZpbGwtb3BhY2l0eT0iLjEiIGQ9Ik0gMCw1MCBDIDI1LDMwIDc1LDMwIDEwMCw1MCBMIDEwMCwwIEwgMCwwIFoiLz48L3N2Zz4=')] bg-repeat-x bg-bottom opacity-30"></div>
    </section>

    <!-- 核心内容区域 -->
    <main class="container mx-auto px-4 py-12">
      <!-- 数据概览卡片 - 快速了解平台状态 -->
      <section class="mb-12 animate-fadeInUp">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-white">数据概览</h3>
          <button class="text-sm text-primary flex items-center gap-1 hover:underline">
            查看详情 <i class="fa fa-angle-right"></i>
          </button>
        </div>
        <StatsChart :stats="statsData" />
      </section>

      <!-- 热门趋势项目 - 核心内容模块 -->
      <section class="mb-12">
        <div class="flex items-center justify-between mb-6 animate-fadeInUp">
          <h3 class="text-xl font-bold text-white">热门趋势项目</h3>
          <div class="flex items-center space-x-2">
            <div class="relative">
              <select v-model="timeFilter" class="select-input py-1.5 pl-3 pr-8 text-sm rounded-lg bg-slate-800 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-primary/50 appearance-none cursor-pointer">
                <option value="today">今日</option>
                <option value="week">本周</option>
                <option value="month">本月</option>
              </select>
              <svg class="absolute right-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </div>
            <button class="btn-icon text-sm" @click="refreshData">
              <i class="fa fa-refresh mr-1"></i> 刷新
            </button>
          </div>
        </div>

        <!-- 项目卡片网格 - 响应式布局 -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <ProjectCard 
            v-for="(project, index) in trendingProjects" 
            :key="project.name"
            :project="project"
            :index="index"
            @click="openProjectModal(project)"
          />
        </div>
        
        <div class="text-center mt-8 animate-fadeInUp">
          <button class="btn-outline text-base py-2 px-6 rounded-lg">
            查看更多项目 <i class="fa fa-angle-right ml-1"></i>
          </button>
        </div>
      </section>

      <!-- 技术趋势分析 - 提供深度洞察 -->
      <section class="mb-12">
        <div class="flex items-center justify-between mb-6 animate-fadeInUp">
          <h3 class="text-xl font-bold text-white">技术趋势分析</h3>
          <button class="btn-secondary text-sm" @click="openTechTrendsModal">
            <i class="fa fa-bar-chart mr-1"></i> 查看完整分析
          </button>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- 热门编程语言 -->
          <div class="glass-card rounded-2xl p-6 animate-fadeInUp" style="animation-delay: 0.1s;">
            <h4 class="text-lg font-semibold text-white mb-4">热门编程语言</h4>
            <div class="space-y-4">
              <div v-for="(lang, index) in topLanguages" :key="lang.name" class="flex items-center space-x-3">
                <div class="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-slate-800 border border-slate-700">
                  <span class="text-xs font-bold">{{ index + 1 }}</span>
                </div>
                <div class="flex-grow">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm font-medium text-slate-200">{{ lang.name }}</span>
                    <span class="text-xs text-slate-400">{{ lang.percentage }}%</span>
                  </div>
                  <div class="w-full bg-slate-700/50 rounded-full h-1.5">
                    <div 
                      class="h-full rounded-full transition-all duration-700 ease-out" 
                      :class="lang.colorClass"
                      :style="{ width: lang.percentage + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 新兴技术领域 -->
          <div class="glass-card rounded-2xl p-6 animate-fadeInUp" style="animation-delay: 0.2s;">
            <h4 class="text-lg font-semibold text-white mb-4">新兴技术领域</h4>
            <div class="space-y-3">
              <div v-for="area in emergingAreas" :key="area.name" class="p-3 bg-slate-800/30 rounded-lg flex items-center justify-between hover:bg-slate-800/50 transition-colors cursor-pointer">
                <div class="flex items-center space-x-3">
                  <div :class="['w-8 h-8 rounded-lg flex items-center justify-center', area.bgClass]">
                    <component :is="area.icon" class="w-4 h-4 text-white" />
                  </div>
                  <span class="text-sm font-medium text-slate-200">{{ area.name }}</span>
                </div>
                <span class="text-xs font-bold text-green-400">+{{ area.growth }}%</span>
              </div>
            </div>
          </div>
          
          <!-- 上升最快项目 -->
          <div class="glass-card rounded-2xl p-6 animate-fadeInUp" style="animation-delay: 0.3s;">
            <h4 class="text-lg font-semibold text-white mb-4">上升最快项目</h4>
            <div class="space-y-4">
              <div v-for="project in surgingProjects" :key="project.name" class="flex items-start space-x-3">
                <div class="flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full bg-slate-800 border border-slate-700 text-xs font-bold">
                  {{ project.rank }}
                </div>
                <div class="flex-grow">
                  <h5 class="text-sm font-medium text-slate-200 mb-1 truncate">{{ project.name.split('/')[1] || project.name }}</h5>
                  <p class="text-xs text-slate-400 mb-1 line-clamp-1">{{ project.description }}</p>
                  <div class="flex items-center space-x-3 text-xs">
                    <span class="text-pink-400">🌟 +{{ project.star_increase }}</span>
                    <span 
                      v-if="project.language" 
                      class="language-tag px-2 py-0.5 rounded-full"
                      :class="getLanguageClass(project.language)"
                    >
                      {{ project.language }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 精选报告 - 提供价值内容 -->
      <section class="mb-12">
        <div class="flex items-center justify-between mb-6 animate-fadeInUp">
          <h3 class="text-xl font-bold text-white">精选分析报告</h3>
          <router-link to="/reports" class="text-sm text-primary flex items-center gap-1 hover:underline">
            查看全部 <i class="fa fa-angle-right"></i>
          </router-link>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="(report, index) in featuredReports" 
            :key="report.date"
            class="glass-card rounded-2xl overflow-hidden hover-lift cursor-pointer animate-fadeInUp" 
            :style="{ animationDelay: `${index * 0.1}s` }"
            @click="openReportModal(report)"
            :class="{ 'opacity-50 cursor-not-allowed': isLoading }"
          >
            <div class="p-6">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs font-medium text-primary bg-primary/10 px-2 py-1 rounded-full">{{ formatDate(report.date) }}</span>
                <span class="text-xs text-slate-400">{{ report.project_count }} 个项目</span>
              </div>
              <h4 class="text-lg font-semibold text-white mb-2">GitHub热门项目报告</h4>
              <p class="text-sm text-slate-400 mb-4 line-clamp-2">
                精选当日最具创新性和实用性的开源项目，涵盖AI、Web开发、工具等多个领域...
              </p>
              <div class="flex justify-between items-center">
                <div class="flex items-center space-x-3">
                  <span class="text-xs text-slate-400 flex items-center gap-1">
                    <i class="fa fa-eye"></i> {{ Math.floor(Math.random() * 1000) + 500 }}
                  </span>
                  <span class="text-xs text-slate-400 flex items-center gap-1">
                    <i class="fa fa-comment"></i> {{ Math.floor(Math.random() * 50) + 10 }}
                  </span>
                </div>
                <button class="text-xs text-primary hover:underline flex items-center gap-1">
                  阅读报告 <i class="fa fa-arrow-right"></i>
                </button>
              </div>
            </div>
            <div class="h-1 bg-gradient-to-r from-primary to-secondary"></div>
          </div>
        </div>
        
        <!-- 加载提示 -->
        <div v-if="isLoading" class="fixed inset-0 bg-black/50 flex items-center justify-center z-40">
          <div class="bg-slate-800 rounded-xl p-6 flex flex-col items-center">
            <div class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p class="text-slate-300">加载报告内容中...</p>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="bg-slate-900 border-t border-slate-800">
      <div class="container mx-auto px-4 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div class="flex items-center space-x-2 mb-4">
              <svg class="w-6 h-6 text-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              <h2 class="text-lg font-bold">GitTrend Insights</h2>
            </div>
            <p class="text-sm text-slate-400 mb-4">
              发现GitHub上的热门技术趋势，助您把握行业前沿动态
            </p>
            <div class="flex space-x-3">
              <a href="#" class="text-slate-400 hover:text-white transition-colors">
                <i class="fa fa-github text-xl"></i>
              </a>
              <a href="#" class="text-slate-400 hover:text-white transition-colors">
                <i class="fa fa-twitter text-xl"></i>
              </a>
              <a href="#" class="text-slate-400 hover:text-white transition-colors">
                <i class="fa fa-linkedin text-xl"></i>
              </a>
            </div>
          </div>
          
          <div>
            <h3 class="text-white font-medium mb-4">产品</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-sm text-slate-400 hover:text-white transition-colors">热门趋势</a></li>
              <li><a href="#" class="text-sm text-slate-400 hover:text-white transition-colors">分析报告</a></li>
              <li><a href="#" class="text-sm text-slate-400 hover:text-white transition-colors">技术洞察</a></li>
              <li><a href="#" class="text-sm text-slate-400 hover:text-white transition-colors">开发者社区</a></li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-white font-medium mb-4">资源</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-sm text-slate-400 hover:text-white transition-colors">文档中心</a></li>
              <li><a href="#" class="text-sm text-slate-400 hover:text-white transition-colors">API接口</a></li>
              <li><a href="#" class="text-sm text-slate-400 hover:text-white transition-colors">常见问题</a></li>
              <li><a href="#" class="text-sm text-slate-400 hover:text-white transition-colors">更新日志</a></li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-white font-medium mb-4">订阅更新</h3>
            <p class="text-sm text-slate-400 mb-4">
              获取每周技术趋势精选，直接发送到您的邮箱
            </p>
            <div class="flex">
              <input type="email" placeholder="您的邮箱地址" class="flex-grow px-3 py-2 bg-slate-800 border border-slate-700 rounded-l-lg focus:outline-none focus:ring-1 focus:ring-primary text-sm">
              <button class="bg-primary hover:bg-primary/90 transition-colors px-3 py-2 rounded-r-lg">
                <i class="fa fa-paper-plane"></i>
              </button>
            </div>
          </div>
        </div>
        
        <div class="border-t border-slate-800 mt-12 pt-6 flex flex-col md:flex-row justify-between items-center">
          <p class="text-sm text-slate-500 mb-4 md:mb-0">
            &copy; {{ new Date().getFullYear() }} GitTrend Insights. 保留所有权利。
          </p>
          <div class="flex space-x-6">
            <a href="#" class="text-xs text-slate-500 hover:text-slate-300 transition-colors">隐私政策</a>
            <a href="#" class="text-xs text-slate-500 hover:text-slate-300 transition-colors">服务条款</a>
            <a href="#" class="text-xs text-slate-500 hover:text-slate-300 transition-colors">联系我们</a>
          </div>
        </div>
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
      v-if="isReportModalOpen"
      @close="closeReportModal"
    />

    <!-- 技术趋势分析模态框 -->
    <TechTrendsModal 
      :visible="isTechTrendsModalOpen"
      :trends-data="trendsData"
      @close="closeTechTrendsModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import ProjectCard from '@/components/ProjectCard.vue'
import ProjectModal from '@/components/ProjectModal.vue'
import ReportModal from '@/components/ReportModal.vue'
import StatsChart from '@/components/StatsChart.vue'
import TechTrendsModal from '@/components/TechTrendsModal.vue'
import type { Project, Report, Stats, TrendsData, TrendDataItem } from '@/api/reports'
import { getReports, getStats, getTrends, getReportByDate, getTrendData } from '@/api/reports'

const router = useRouter()

// 响应式数据
const theme = ref<'light' | 'dark'>('dark')
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
  surging_projects: []
})
const trendAreasData = ref<TrendDataItem[]>([]) // 新兴技术领域数据

// 加载状态
const isLoading = ref(false)

// 模态框状态
const isProjectModalOpen = ref(false)
const isReportModalOpen = ref(false)
const isTechTrendsModalOpen = ref(false)
const selectedProject = ref<Project | null>(null)
const selectedReport = ref<Report>({
  date: '',
  project_count: 0
})

// 计算属性 - 热门编程语言
const topLanguages = computed(() => {
  // 使用从API获取的真实语言数据
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
        percentage: Math.round((count / total) * 100),
        colorClass: colorClasses[index % colorClasses.length]
      }))
  }
  
  // 如果没有真实数据，使用模拟数据作为备选
  return [
    { name: 'TypeScript', percentage: 35, colorClass: 'bg-gradient-to-r from-blue-500 to-blue-600' },
    { name: 'JavaScript', percentage: 28, colorClass: 'bg-gradient-to-r from-yellow-500 to-yellow-600' },
    { name: 'Python', percentage: 20, colorClass: 'bg-gradient-to-r from-green-500 to-green-600' },
    { name: 'Go', percentage: 10, colorClass: 'bg-gradient-to-r from-cyan-500 to-cyan-600' },
    { name: 'Rust', percentage: 7, colorClass: 'bg-gradient-to-r from-orange-500 to-orange-600' }
  ]
})

// 更新热门趋势项目数据
function updateTrendingProjects() {
  if (trendsData.value && trendsData.value.most_frequent_projects && trendsData.value.most_frequent_projects.length > 0) {
    // 直接使用后端返回的完整项目数据，不再需要生成默认值
    trendingProjects.value = trendsData.value.most_frequent_projects.slice(0, 12).map(project => ({
      name: project.name,
      url: project.url || `https://github.com/${project.name}`,
      description: project.description,
      language: project.language,
      stars: project.stars || project.avg_stars || 0,
      forks: project.forks || 0,
      contributor_count: project.contributor_count || 0,
      created_at: project.created_at || new Date().toISOString(),
      updated_at: project.updated_at || new Date().toISOString(),
      open_issues: project.open_issues || 0,
      watchers: project.watchers || 0,
      summary_date: project.created_at ? new Date(project.created_at).toISOString().split('T')[0] : new Date().toISOString().split('T')[0]
    }))
  } else {
    // 如果没有真实数据，使用模拟数据
    trendingProjects.value = generateMockProjectsByTimeFilter(12)
  }
}

// 计算属性 - 新兴技术领域
const emergingAreas = computed(() => {
  // 使用从API获取的真实新兴技术领域数据
  if (trendAreasData.value && trendAreasData.value.length > 0) {
    // 为不同的技术领域分配图标和背景色
    const techIcons = ['IconEcosystem', 'IconTooling', 'IconCommunity', 'IconDocumentation']
    const bgClasses = ['bg-purple-500/20', 'bg-blue-500/20', 'bg-green-500/20', 'bg-pink-500/20']
    
    // 技术领域名称映射
    const areaNameMap: Record<string, string> = {
      '新项目': '生成式AI',
      '活跃项目': 'WebAssembly',
      '热门项目': '边缘计算',
      '趋势项目': '低代码平台'
    }
    
    return trendAreasData.value.slice(0, 4).map((item, index) => ({
      name: areaNameMap[item.label] || item.label,
      growth: item.change * 100, // 假设API返回的是小数，转换为百分比
      bgClass: bgClasses[index % bgClasses.length],
      icon: techIcons[index % techIcons.length]
    }))
  }
  
  // 如果没有真实数据，使用模拟数据作为备选
  return [
    { name: '生成式AI', growth: 125, bgClass: 'bg-purple-500/20', icon: 'IconEcosystem' },
    { name: 'WebAssembly', growth: 87, bgClass: 'bg-blue-500/20', icon: 'IconTooling' },
    { name: '边缘计算', growth: 63, bgClass: 'bg-green-500/20', icon: 'IconCommunity' },
    { name: '低代码平台', growth: 45, bgClass: 'bg-pink-500/20', icon: 'IconDocumentation' }
  ]
})

// 计算属性 - 上升最快项目
const surgingProjects = computed(() => {
  // 使用从API获取的真实上升最快项目数据
  if (trendsData.value && trendsData.value.surging_projects && trendsData.value.surging_projects.length > 0) {
    return trendsData.value.surging_projects.slice(0, 4).map((project, index) => ({
      ...project,
      rank: index + 1
    }))
  }
  
  // 如果没有真实数据，使用模拟数据作为备选
  return [
    {
      rank: 1,
      name: 'facebook/react',
      description: 'A declarative, efficient, and flexible JavaScript library for building user interfaces.',
      language: 'JavaScript',
      star_increase: 5280
    },
    {
      rank: 2,
      name: 'vercel/next.js',
      description: 'The React Framework for Production',
      language: 'TypeScript',
      star_increase: 4720
    },
    {
      rank: 3,
      name: 'tensorflow/tensorflow',
      description: 'An Open Source Machine Learning Framework for Everyone',
      language: 'Python',
      star_increase: 3890
    },
    {
      rank: 4,
      name: 'rust-lang/rust',
      description: 'Empowering everyone to build reliable and efficient software.',
      language: 'Rust',
      star_increase: 2980
    }
  ]
})

// 初始化数据
onMounted(async () => {
  await loadInitialData()
  // 初始化主题
  applyTheme(theme.value)
  
  // 监听系统主题变化
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (e.matches) {
      setTheme('dark')
    } else {
      setTheme('light')
    }
  })
})

// 加载初始数据
async function loadInitialData() {
  try {
    // 并行请求数据
  const [statsResponse, reportsResponse, trendsResponse, trendAreasResponse] = await Promise.all([
    getStats(),
    getReports(),
    getTrends(),
    getTrendData()
  ])
  
  // 更新统计数据
  statsData.value = statsResponse
  
  // 更新报告数据
  featuredReports.value = reportsResponse.slice(0, 3)
  
  // 更新趋势数据
  trendsData.value = trendsResponse
  
  // 更新新兴技术领域数据
  trendAreasData.value = trendAreasResponse
    
    // 使用真实数据而不是模拟数据
    // 根据时间过滤器获取相应的真实项目数据
    updateTrendingProjects()
  } catch (error) {
    console.error('加载数据失败:', error)
    // 加载失败时使用模拟数据
    loadMockData()
  }
}

// 加载模拟数据
function loadMockData() {
  // 模拟统计数据
    statsData.value = {
      totalReports: 156,
      totalProjects: 1245,
      topLanguage: 'TypeScript',
      weeklyNew: 48,
      totalForks: '56,234',
      avgContributors: 128,
      activityScore: 85
    }
  
  // 模拟报告数据
  const today = new Date()
  featuredReports.value = [
    {
      date: today.toISOString().split('T')[0],
      project_count: 27
    },
    {
      date: new Date(today.getTime() - 86400000).toISOString().split('T')[0],
      project_count: 25
    },
    {
      date: new Date(today.getTime() - 172800000).toISOString().split('T')[0],
      project_count: 30
    }
  ]
  
  // 根据当前时间过滤器生成模拟项目数据
  trendingProjects.value = generateMockProjectsByTimeFilter(12)
}

// 根据时间过滤器生成模拟项目数据
function generateMockProjectsByTimeFilter(count: number): Project[] {
  const languages = ['TypeScript', 'JavaScript', 'Python', 'Go', 'Rust', 'Java', 'C++']
  const projects: Project[] = []
  
  // 根据时间过滤器调整数据生成逻辑
  let timeRange = 0
  let starMultiplier = 1
  
  switch (timeFilter.value) {
    case 'today':
      timeRange = 86400000 // 24小时
      starMultiplier = 1.5 // 今日项目获得更多星星
      break
    case 'week':
      timeRange = 604800000 // 7天
      starMultiplier = 1.2
      break
    case 'month':
      timeRange = 2592000000 // 30天
      starMultiplier = 1
      break
  }
  
  // 预定义一些更真实的项目名称和描述，让数据看起来更逼真
  const projectTemplates = [
    { name: 'deep-learning-framework', desc: 'Advanced neural network framework with distributed training support' },
    { name: 'web3-wallet', desc: 'Secure cryptocurrency wallet with multi-chain support and dApp integration' },
    { name: 'data-visualization', desc: 'Powerful data visualization library with real-time rendering capabilities' },
    { name: 'cloud-infrastructure', desc: 'Modular cloud infrastructure management system with auto-scaling' },
    { name: 'ai-assistant', desc: 'Intelligent personal assistant with natural language processing' },
    { name: 'devops-toolkit', desc: 'Comprehensive DevOps toolkit for CI/CD pipelines and infrastructure automation' },
    { name: 'security-scanner', desc: 'Automated security vulnerability scanner for web applications' },
    { name: 'edge-computing', desc: 'Edge computing platform for low-latency applications and IoT devices' },
    { name: 'mobile-framework', desc: 'Cross-platform mobile development framework with native performance' },
    { name: 'quantum-computing', desc: 'Quantum computing simulator and algorithm development environment' }
  ]
  
  for (let i = 0; i < count; i++) {
    const language = languages[Math.floor(Math.random() * languages.length)]
    const templateIndex = Math.floor(Math.random() * projectTemplates.length)
    const template = projectTemplates[templateIndex]
    const owner = ['google', 'facebook', 'microsoft', 'apple', 'amazon', 'github', 'apache', 'mozilla', 'netflix', 'spotify'][Math.floor(Math.random() * 10)]
    
    // 根据时间过滤器设置项目更新时间
    const updateTime = new Date(Date.now() - Math.floor(Math.random() * timeRange))
    
    projects.push({
      name: `${owner}/${template.name}`,
      url: `https://github.com/${owner}/${template.name}`,
      description: template.desc,
      language: language,
      stars: Math.floor((Math.random() * 10000 + 100) * starMultiplier),
      forks: Math.floor(Math.random() * 1000) + 10,
      contributor_count: Math.floor(Math.random() * 100) + 1,
      created_at: new Date(updateTime.getTime() - Math.floor(Math.random() * 31536000000)).toISOString(),
      updated_at: updateTime.toISOString(),
      open_issues: Math.floor(Math.random() * 100),
      watchers: Math.floor(Math.random() * 5000) + 50
    })
  }
  
  // 按星星数量排序，让热门项目更突出
  return projects.sort((a, b) => b.stars - a.stars)
}

// 为了兼容性保留原函数
function generateMockProjects(count: number): Project[] {
  return generateMockProjectsByTimeFilter(count)
}

// 刷新数据
async function refreshData() {
  isLoading.value = true
  try {
      // 根据timeFilter映射到相应的days参数
      let days = 7; // 默认7天
      switch (timeFilter.value) {
        case 'today':
          days = 7; // 后端目前只支持固定天数，所以'today'也映射到7天
          break;
        case 'week':
          days = 7;
          break;
        case 'month':
          days = 30;
          break;
      }
      
      // 并行获取趋势数据和新兴技术领域数据
      const [newTrendsResponse, newTrendAreasResponse] = await Promise.all([
        getTrends({ days }),
        getTrendData()
      ]);
    
      // 更新趋势数据和新兴技术领域数据
      trendsData.value = newTrendsResponse
      trendAreasData.value = newTrendAreasResponse
    
    // 更新项目数据
    updateTrendingProjects()
  } catch (error) {
    console.error('刷新数据失败:', error)
    // 如果失败，使用模拟数据
    trendingProjects.value = generateMockProjectsByTimeFilter(12)
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
    const element = document.querySelector('section:nth-of-type(3)')
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  })
}

// 主题切换
function toggleTheme() {
  const newTheme = theme.value === 'dark' ? 'light' : 'dark'
  setTheme(newTheme)
}

// 设置主题
function setTheme(newTheme: 'light' | 'dark') {
  theme.value = newTheme
  applyTheme(newTheme)
}

// 应用主题
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
  try {
    // 先显示加载状态
    isLoading.value = true;
    // 获取报告完整内容
    const fullReport = await getReportByDate(report.date);
    selectedReport.value = fullReport;
    isReportModalOpen.value = true;
  } catch (error) {
    console.error('加载报告内容失败:', error);
    // 可以添加错误提示
  } finally {
    isLoading.value = false;
  }
}

// 关闭报告详情模态框
function closeReportModal() {
  isReportModalOpen.value = false
}

// 打开技术趋势分析模态框
function openTechTrendsModal() {
  isTechTrendsModalOpen.value = true
}

// 关闭技术趋势分析模态框
function closeTechTrendsModal() {
  isTechTrendsModalOpen.value = false
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

// 获取编程语言样式
function getLanguageClass(language: string): string {
  const languageColors: Record<string, string> = {
    'JavaScript': 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30',
    'TypeScript': 'bg-blue-500/20 text-blue-400 border border-blue-500/30',
    'Python': 'bg-green-500/20 text-green-400 border border-green-500/30',
    'Java': 'bg-orange-500/20 text-orange-400 border border-orange-500/30',
    'Go': 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30',
    'Rust': 'bg-red-500/20 text-red-400 border border-red-500/30',
    'C++': 'bg-purple-500/20 text-purple-400 border border-purple-500/30',
    'C': 'bg-gray-500/20 text-gray-400 border border-gray-500/30',
    'PHP': 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30',
    'Ruby': 'bg-red-600/20 text-red-400 border border-red-600/30',
    'Swift': 'bg-orange-600/20 text-orange-400 border border-orange-600/30',
    'Kotlin': 'bg-purple-600/20 text-purple-400 border border-purple-600/30'
  }
  
  return languageColors[language] || 'bg-slate-500/20 text-slate-400 border border-slate-500/30'
}
</script>

<style scoped>
/* 背景网格图案 */
.bg-grid-pattern {
  background-image: linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
}

/* 按钮样式 */
.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: 1px solid rgba(99, 102, 241, 0.3);
  color: white;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border-color: rgba(99, 102, 241, 0.5);
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}

/* 输入框样式 */
.select-input {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(100, 116, 139, 0.5);
  color: #e2e8f0;
  transition: all 0.2s ease;
}

.select-input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* 动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

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

.animate-fadeIn {
  animation: fadeIn 0.5s ease forwards;
}

.animate-fadeInUp {
  animation: fadeInUp 0.5s ease forwards;
}

/* 玻璃态卡片样式 */
.glass-card {
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(100, 116, 139, 0.2);
  transition: all 0.3s ease;
}

.glass-card:hover {
  background: rgba(15, 23, 42, 0.6);
  border-color: rgba(100, 116, 139, 0.3);
  transform: translateY(-2px);
}

/* 悬停提升效果 */
.hover-lift {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
}
</style>