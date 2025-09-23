<template>
  <div class="bg-gradient-to-br from-slate-800 to-slate-900 text-slate-100 min-h-screen font-sans theme-transition">
    <!-- 粒子背景效果 -->
    <div class="fixed inset-0 -z-10 overflow-hidden">
      <div class="absolute top-[10%] left-[20%] w-64 h-64 bg-blue-500/20 rounded-full filter blur-3xl animate-pulse-slow"></div>
      <div class="absolute top-[60%] right-[15%] w-80 h-80 bg-purple-500/20 rounded-full filter blur-3xl animate-pulse-slow delay-1000"></div>
      <div class="absolute bottom-[10%] left-[30%] w-72 h-72 bg-pink-500/20 rounded-full filter blur-3xl animate-pulse-slow delay-2000"></div>
    </div>

    <!-- 主内容区 -->
    <div class="container mx-auto px-4 py-12">
      <div class="mb-8">
        <button 
          @click="$router.push('/')"
          class="mb-4 glass-card px-4 py-2 rounded-lg text-slate-300 hover:text-white transition-all duration-200 hover:scale-105 border border-white/10 hover:border-blue-400/50 backdrop-blur-sm flex items-center space-x-2"
        >
          <i class="fa fa-arrow-left"></i>
          <span>返回首页</span>
        </button>
        <h1 class="text-4xl font-bold">
          <span style="background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899); background-clip: text; -webkit-background-clip: text; color: transparent;">
            精选分析报告
          </span>
        </h1>
        <p class="text-slate-400 mt-2">探索 GitHub 每日热门开源项目分析报告</p>
      </div>

      <div class="text-center mb-8">
        <!-- 快速导航栏 -->
        <div class="flex flex-wrap justify-center items-center gap-4 mb-8">
          <div class="glass-card rounded-full px-6 py-3 border border-slate-600/50 hover:border-blue-400/50 transition-all duration-200">
            <div class="flex items-center space-x-3">
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              <input 
                v-model="searchQuery" 
                @input="filterReports"
                type="text" 
                placeholder="搜索报告..." 
                class="bg-transparent text-slate-300 placeholder-slate-500 outline-none w-32 sm:w-48"
              >
            </div>
          </div>
          
          <select 
            v-model="selectedTimeRange" 
            @change="filterReports"
            class="glass-card rounded-full px-4 py-3 border border-slate-600/50 hover:border-purple-400/50 transition-all duration-200 bg-transparent text-slate-300 outline-none cursor-pointer"
          >
            <option value="all">全部时间</option>
            <option value="week">本周</option>
            <option value="month">本月</option>
            <option value="quarter">本季度</option>
          </select>
          
          <div class="glass-card rounded-full px-4 py-3 border border-slate-600/50 hover:border-green-400/50 transition-all duration-200 cursor-pointer" @click="refreshAll">
            <div class="flex items-center space-x-2">
              <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              <span class="text-sm font-medium text-green-400">刷新</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 报告列表 -->
      <div v-if="loading" class="text-center py-20">
        <div class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-slate-300">加载报告列表中...</p>
      </div>

      <div v-else-if="error" class="text-center py-12">
        <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01"></path>
          </svg>
        </div>
        <div class="text-red-400 mb-4">{{ error }}</div>
        <button @click="fetchReports" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors">
          重试
        </button>
      </div>

      <!-- 显示报告列表 -->
      <div v-else-if="filteredReports.length > 0 || reports.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div 
          v-for="(report, index) in (filteredReports.length > 0 || searchQuery || selectedTimeRange !== 'all' ? filteredReports : reports)" 
          :key="report.date"
          class="report-card bg-gradient-to-br from-slate-800/60 to-slate-900/60 rounded-3xl overflow-hidden border border-white/10 hover:border-white/20 cursor-pointer backdrop-blur-xl group transition-all duration-500 hover:transform hover:scale-105 hover:shadow-2xl"
          :style="{ animationDelay: `${index * 0.1}s` }"
          @click="() => openReport(report.date)"
        >
          <!-- 背景装饰 -->
          <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          
          <!-- 最新标识 -->
          <div v-if="index === 0" class="absolute top-4 right-4 z-10">
            <div class="bg-gradient-to-r from-pink-500 to-rose-500 text-white text-xs px-3 py-1 rounded-full shadow-lg">
              <i class="fa fa-star mr-1"></i>最新
            </div>
          </div>
          
          <!-- 卡片内容 -->
          <div class="relative p-6">
            <!-- 日期大标题 -->
            <div class="mb-6">
              <div class="text-slate-400 text-sm font-medium mb-2 flex items-center">
                <i class="fa fa-calendar mr-2 text-blue-400"></i>
                {{ formatDateShort(report.date) }}
              </div>
              <div class="relative">
                <div class="text-6xl font-black text-transparent bg-gradient-to-br from-blue-400 via-purple-400 to-pink-400 bg-clip-text">
                  {{ formatDay(report.date) }}
                </div>
                <div class="absolute -bottom-1 left-0 w-12 h-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full opacity-60"></div>
              </div>
              <div class="text-slate-300 text-sm mt-2 font-medium">
                {{ formatDateWeek(report.date) }}
              </div>
            </div>
            
            <!-- 项目统计 -->
            <div class="mb-6">
              <div class="flex items-center justify-between bg-slate-700/30 rounded-xl p-3 border border-slate-600/30">
                <div class="flex items-center">
                  <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center mr-3">
                    <i class="fa fa-cube text-white text-sm"></i>
                  </div>
                  <div>
                    <div class="text-slate-300 text-sm">项目数量</div>
                    <div class="text-lg font-bold text-white">{{ report.project_count }}</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-slate-400 text-xs">点击查看</div>
                  <div class="text-blue-400 text-lg">
                    <i class="fa fa-arrow-right"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 底部装饰线 -->
          <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-60 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>
      </div>
      
      <!-- 空数据状态 -->
      <div v-else class="text-center py-20">
        <div class="max-w-md mx-auto">
          <div class="w-24 h-24 bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-12 h-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-slate-300 mb-4">暂无报告</h3>
          <p class="text-slate-400 mb-6">还没有生成任何报告</p>
          <button @click="fetchReports" class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors">
            刷新数据
          </button>
        </div>
      </div>
    </div>

    <!-- 报告详情模态框 -->
    <div v-if="showModal" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" @click="closeModal">
      <div class="bg-slate-800 rounded-2xl max-w-5xl w-full max-h-[90vh] overflow-hidden" @click.stop>
        <!-- 模态框头部 -->
        <div class="flex items-center justify-between p-6 border-b border-slate-600">
          <h3 class="text-xl font-bold text-white">报告详情 - {{ formatDateShort(currentReport?.date || '') }}</h3>
          <button @click="closeModal" class="text-slate-400 hover:text-white transition-colors">
            <i class="fa fa-times text-xl"></i>
          </button>
        </div>
        
        <!-- 模态框内容 -->
        <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          <div v-if="loadingContent" class="text-center py-16">
            <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p class="text-slate-400">加载报告内容中...</p>
          </div>
          
          <div v-else-if="reportError" class="text-center py-12">
            <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01"></path>
              </svg>
            </div>
            <div class="text-red-400 mb-4">{{ reportError }}</div>
            <button @click="() => loadReportContent(currentReport?.date)" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors">
              重试
            </button>
          </div>
          
          <div v-else-if="renderedContent" v-html="renderedContent"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { reportApi, type Report } from '../api/reports'
import { renderMarkdown, enhanceMarkdownDisplay } from '../utils/markdown-simple'

const router = useRouter()

// 响应式数据
const reports = ref<Report[]>([])
const filteredReports = ref<Report[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const showModal = ref(false)
const currentReport = ref<Report | null>(null)
const reportContent = ref<string | null>(null)
const renderedContent = ref<string | null>(null)
const loadingContent = ref(false)
const reportError = ref<string | null>(null)

// 搜索和筛选相关数据
const searchQuery = ref('')
const selectedTimeRange = ref('all')

// 生命周期钩子
onMounted(() => {
  fetchReports()
})

// 获取报告列表
async function fetchReports() {
  try {
    loading.value = true
    error.value = null
    console.log('📊 开始获取报告列表...')
    
    const reportsData = await reportApi.getReports();
    reports.value = reportsData || []
    filteredReports.value = reports.value
    
    console.log('✅ 报告获取成功:', reports.value.length, '个报告')
  } catch (err: any) {
    error.value = err.message || '获取报告列表失败'
    console.error('❌ 获取报告失败:', err)
  } finally {
    loading.value = false
  }
}

// 筛选报告
function filterReports() {
  let filtered = [...reports.value]
  
  // 按搜索关键词筛选
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter(report => 
      report.date.toLowerCase().includes(query) ||
      formatDateShort(report.date).toLowerCase().includes(query)
    )
  }
  
  // 按时间范围筛选
  if (selectedTimeRange.value !== 'all') {
    const now = new Date()
    const cutoffDate = new Date()
    
    switch (selectedTimeRange.value) {
      case 'week':
        cutoffDate.setDate(now.getDate() - 7)
        break
      case 'month':
        cutoffDate.setMonth(now.getMonth() - 1)
        break
      case 'quarter':
        cutoffDate.setMonth(now.getMonth() - 3)
        break
    }
    
    filtered = filtered.filter(report => {
      const reportDate = new Date(report.date)
      return reportDate >= cutoffDate
    })
  }
  
  filteredReports.value = filtered
}

// 刷新所有数据
async function refreshAll() {
  searchQuery.value = ''
  selectedTimeRange.value = 'all'
  await fetchReports()
}

// 加载报告内容
async function loadReportContent(date?: string) {
  if (!date) return
  
  try {
    loadingContent.value = true
    reportError.value = null
    console.log('📄 加载报告内容:', date)
    const report = await reportApi.getReportContent(date)
    reportContent.value = report.content || '暂无内容'
    
    // 渲染Markdown内容
    const html = await renderMarkdown(reportContent.value)
    renderedContent.value = html
    
    console.log('✅ 报告内容加载成功')
  } catch (err: any) {
    reportError.value = err.message || '加载报告内容失败'
    renderedContent.value = null
    console.error('❌ 加载报告内容失败:', err)
  } finally {
    loadingContent.value = false
  }
}

// 打开报告
async function openReport(date: string) {
  console.log('🎯 点击报告卡片:', date)
  const report = reports.value.find(r => r.date === date)
  if (report) {
    // 确保加载报告内容后再打开模态框
    await loadReportContent(date)
    
    // 更新报告内容
    report.content = reportContent.value || '' // 确保 content 不是 null/undefined
    currentReport.value = report
    showModal.value = true
    console.log('📂 打开报告模态框')
  } else {
    console.error('❌ 未找到报告:', date)
  }
}

// 关闭模态框
function closeModal() {
  console.log('📋 关闭模态框')
  showModal.value = false
  currentReport.value = null
  reportContent.value = null
  renderedContent.value = null
  reportError.value = null
  loadingContent.value = false
}

// 日期格式化函数
function formatDateShort(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    weekday: 'short'
  })
}

function formatDay(dateStr: string): string {
  const date = new Date(dateStr)
  return date.getDate().toString()
}

function formatDateWeek(dateStr: string): string {
  const date = new Date(dateStr)
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  return weekdays[date.getDay()]
}
</script>

<style scoped>
.glass-card {
  background: rgba(30, 40, 50, 0.6);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.glass-card:hover {
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.theme-transition {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(30, 40, 50, 0.6);
}

::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.4);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.6);
}

/* 动画效果 */
@keyframes pulse-slow {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.6; }
}

.animate-pulse-slow {
  animation: pulse-slow 8s ease-in-out infinite;
}
</style>