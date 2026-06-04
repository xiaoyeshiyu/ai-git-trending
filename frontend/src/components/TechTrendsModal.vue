<template>
  <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
    <div class="relative w-full max-w-6xl max-h-[90vh] overflow-hidden rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl animate-fadeIn">
      <!-- 模态框头部 -->
      <div class="sticky top-0 z-10 flex items-center justify-between p-6 bg-slate-900 border-b border-slate-800">
        <h2 class="text-xl font-bold text-white flex items-center">
          <i class="fa fa-line-chart text-primary mr-3"></i>
          技术趋势深度分析
        </h2>
        <div class="flex items-center space-x-3">
          <button class="text-sm px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-300 hover:bg-slate-700 transition-colors">
            导出分析报告
          </button>
          <button class="btn-icon" @click="handleClose">
            <i class="fa fa-times"></i>
          </button>
        </div>
      </div>
      
      <!-- 模态框内容 -->
      <div class="p-6 overflow-y-auto max-h-[calc(90vh-8rem)]">
        <!-- 时间选择器 -->
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center space-x-2">
            <button 
              v-for="window in timeWindows" 
              :key="window.value"
              :class="['text-sm px-4 py-2 rounded-lg transition-colors', selectedWindow === window.value ? 'bg-primary text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700']"
              @click="selectedWindow = window.value"
            >
              {{ window.label }}
            </button>
          </div>
          <div class="flex items-center space-x-3">
            <div class="text-sm text-slate-400">
              显示趋势数据从 {{ formatDate(startDate) }} 至 {{ formatDate(endDate) }}
            </div>
            <button class="btn-icon" @click="refreshTrendsData">
              <i class="fa fa-refresh"></i>
            </button>
          </div>
        </div>
        
        <!-- 主要数据概览卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <!-- 项目活跃度指数 -->
          <div class="glass-card p-6 rounded-xl">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-white">项目活跃度指数</h3>
              <span class="text-xs font-bold text-slate-500">--</span>
            </div>
            <div class="flex items-end space-x-3">
              <div class="text-3xl font-bold text-white">--</div>
              <div class="text-sm text-slate-400 mb-1">活跃度评分</div>
            </div>
          </div>
          
          <!-- 技术创新热度 -->
          <div class="glass-card p-6 rounded-xl">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-white">技术创新热度</h3>
              <span class="text-xs font-bold text-slate-500">--</span>
            </div>
            <div class="flex items-end space-x-3">
              <div class="text-3xl font-bold text-white">--</div>
              <div class="text-sm text-slate-400 mb-1">创新指数</div>
            </div>
          </div>
          
          <!-- 社区参与度 -->
          <div class="glass-card p-6 rounded-xl">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-white">社区参与度</h3>
              <span class="text-xs font-bold text-slate-500">--</span>
            </div>
            <div class="flex items-end space-x-3">
              <div class="text-3xl font-bold text-white">--</div>
              <div class="text-sm text-slate-400 mb-1">参与指数</div>
            </div>
          </div>
        </div>
        
        <!-- 双列图表区域 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <!-- 语言趋势图表 -->
          <div class="glass-card p-6 rounded-xl">
            <h3 class="text-lg font-semibold text-white mb-6">编程语言趋势变化</h3>
            <div class="h-80">
              <canvas id="languageTrendChart"></canvas>
            </div>
          </div>
          
          <!-- 项目类型分布 -->
          <div class="glass-card p-6 rounded-xl">
            <h3 class="text-lg font-semibold text-white mb-6">项目类型分布</h3>
            <div class="h-80">
              <canvas id="projectTypeChart"></canvas>
            </div>
          </div>
        </div>
        
        <!-- 详细分析表格 -->
        <div class="glass-card p-6 rounded-xl mb-8">
          <h3 class="text-lg font-semibold text-white mb-6">热门技术领域深度分析</h3>
          
          <!-- 有数据状态 -->
          <div v-if="techAreas && techAreas.length > 0" class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-slate-800">
                  <th class="text-left py-3 px-4 text-sm font-medium text-slate-400">技术领域</th>
                  <th class="text-left py-3 px-4 text-sm font-medium text-slate-400">项目数量</th>
                  <th class="text-left py-3 px-4 text-sm font-medium text-slate-400">增长率</th>
                  <th class="text-left py-3 px-4 text-sm font-medium text-slate-400">平均Stars</th>
                  <th class="text-left py-3 px-4 text-sm font-medium text-slate-400">活跃度</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(area, index) in techAreas" :key="area.name" class="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
                  <td class="py-3 px-4 text-sm font-medium text-white flex items-center">
                    <div :class="['w-8 h-8 rounded-lg flex items-center justify-center mr-3', area.bgClass]">
                      <component :is="area.icon" class="w-4 h-4 text-white" />
                    </div>
                    {{ area.name }}
                  </td>
                  <td class="py-3 px-4 text-sm text-slate-300">{{ area.project_count }}</td>
                  <td class="py-3 px-4 text-sm">
                    <span :class="area.growth_rate > 0 ? 'text-green-400' : 'text-red-400'">
                      {{ area.growth_rate > 0 ? '+' : '' }}{{ area.growth_rate }}%
                    </span>
                  </td>
                  <td class="py-3 px-4 text-sm text-slate-300">{{ formatNumber(area.avg_stars) }}</td>
                  <td class="py-3 px-4">
                    <div class="w-full bg-slate-700/50 rounded-full h-2 mb-1">
                      <div 
                        class="h-full rounded-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-1000 ease-out"
                        :style="{ width: area.activity_score + '%' }"
                      ></div>
                    </div>
                    <div class="text-xs text-right text-slate-400">{{ area.activity_score }}%</div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- 无数据状态 -->
          <div v-else class="text-center py-8">
            <div class="w-16 h-16 bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-4">
              <i class="fa fa-table text-slate-400 text-xl"></i>
            </div>
            <p class="text-slate-400">暂无技术领域数据</p>
            <p class="text-slate-500 text-sm mt-2">请稍后刷新或联系管理员获取最新数据</p>
          </div>
        </div>
        
        <!-- 趋势洞察报告 -->
        <div class="glass-card p-6 rounded-xl">
          <h3 class="text-lg font-semibold text-white mb-6">趋势洞察分析报告</h3>
          
          <!-- 从后端获取的趋势洞察分析报告 -->
          <!-- 趋势洞察分析报告内容将在有数据时显示 -->
          <div v-if="false" class="prose prose-invert max-w-none">
            <p class="text-slate-300 mb-4">
              根据最近{{ selectedWindow }}的数据分析，我们观察到以下几个显著的技术趋势:
            </p>
            
            <!-- 实际数据将通过API获取后动态渲染 -->
          </div>
          
          <!-- 无数据状态 -->
          <div v-else class="text-center py-8">
            <div class="w-16 h-16 bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-4">
              <i class="fa fa-bar-chart text-slate-400 text-xl"></i>
            </div>
            <p class="text-slate-400">暂无趋势洞察数据</p>
            <p class="text-slate-500 text-sm mt-2">请稍后刷新或联系管理员获取最新报告</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { Chart, registerables, type ChartConfiguration } from 'chart.js'
import type { TrendsData } from '@/api/reports'
import IconCommunity from './icons/IconCommunity.vue'
import IconDocumentation from './icons/IconDocumentation.vue'
import IconEcosystem from './icons/IconEcosystem.vue'
import IconSupport from './icons/IconSupport.vue'
import IconTooling from './icons/IconTooling.vue'

// 注册Chart.js组件
Chart.register(...registerables)

// 定义props
interface TechTrendsModalProps {
  visible: boolean
  trendsData?: TrendsData
}

// 定义emits
const emit = defineEmits<{
  close: []
}>()

const props = withDefaults(defineProps<TechTrendsModalProps>(), {
  visible: false,
  trendsData: () => ({
    time_window_days: 30,
    most_frequent_projects: [],
    most_frequent_languages: [],
    surging_projects: []
  })
})

// 定义技术领域接口
interface TechArea {
  name: string
  project_count: number
  growth_rate: number
  avg_stars: number
  activity_score: number
  bgClass: string
  icon: string
}

// 响应式数据
const selectedWindow = ref<string>('30天')
const languageChart = ref<Chart | null>(null)
const projectTypeChart = ref<Chart | null>(null)

// 时间窗口选项
const timeWindows = [
  { value: '7天', label: '最近7天' },
  { value: '30天', label: '最近30天' },
  { value: '90天', label: '最近90天' },
  { value: '1年', label: '最近1年' }
]

// 计算日期范围
const startDate = computed(() => {
  const today = new Date()
  switch (selectedWindow.value) {
    case '7天':
      return new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000)
    case '30天':
      return new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000)
    case '90天':
      return new Date(today.getTime() - 90 * 24 * 60 * 60 * 1000)
    case '1年':
      return new Date(today.getTime() - 365 * 24 * 60 * 60 * 1000)
    default:
      return new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000)
  }
})

const endDate = computed(() => new Date())

// 初始化技术领域数据为空数组，等待从API获取
const techAreas = ref<TechArea[]>([])

// 监听可见性变化
watch(() => props.visible, (newVisible) => {
  if (newVisible) {
    // 模态框显示后初始化图表
    setTimeout(() => {
      initCharts()
    }, 100)
    // 防止背景滚动
    document.body.style.overflow = 'hidden'
  } else {
    // 模态框隐藏后释放图表资源
    destroyCharts()
    // 恢复背景滚动
    document.body.style.overflow = ''
  }
})

// 监听时间窗口变化，更新图表
watch(selectedWindow, () => {
  updateCharts()
})

// 初始化图表
function initCharts() {
  // 确保之前的图表实例已经销毁
  destroyCharts()
  
  // 初始化语言趋势图表
  const languageCtx = document.getElementById('languageTrendChart') as HTMLCanvasElement
  if (languageCtx) {
    languageChart.value = new Chart(languageCtx, getLanguageTrendChartConfig())
  }
  
  // 初始化项目类型分布图表
  const projectTypeCtx = document.getElementById('projectTypeChart') as HTMLCanvasElement
  if (projectTypeCtx) {
    projectTypeChart.value = new Chart(projectTypeCtx, getProjectTypeChartConfig())
  }
}

// 更新图表
function updateCharts() {
  if (languageChart.value) {
    languageChart.value.data = getLanguageTrendChartConfig().data
    languageChart.value.update()
  }
  
  if (projectTypeChart.value) {
    projectTypeChart.value.data = getProjectTypeChartConfig().data
    projectTypeChart.value.update()
  }
}

// 销毁图表
function destroyCharts() {
  if (languageChart.value) {
    languageChart.value.destroy()
    languageChart.value = null
  }
  
  if (projectTypeChart.value) {
    projectTypeChart.value.destroy()
    projectTypeChart.value = null
  }
}

// 获取语言趋势图表配置
function getLanguageTrendChartConfig() {
  // 从props获取真实数据
  const labels = generateTimeLabels()
  
  // 准备图表数据
  const datasets: ChartConfiguration<'line'>['data']['datasets'] = []
  
  // 如果有真实的语言数据，使用它
  if (props.trendsData && props.trendsData.most_frequent_languages && props.trendsData.most_frequent_languages.length > 0) {
    // 语言颜色映射
    const languageColors = {
      'TypeScript': '#6366f1',
      'JavaScript': '#f59e0b',
      'Python': '#10b981',
      'Go': '#3b82f6',
      'Rust': '#f43f5e',
      'Java': '#ef4444',
      'C++': '#0ea5e9'
    }
    
    // 将后端数据转换为图表格式
    props.trendsData.most_frequent_languages.slice(0, 4).forEach(([language, count]) => {
      const color = languageColors[language as keyof typeof languageColors] || '#94a3b8'
      
      // 对于真实数据，这里应该有历史数据，但由于我们没有完整的历史数据，
      // 我们创建一个简单的数据集来展示当前值
      const data = new Array(labels.length).fill(0)
      data[data.length - 1] = count // 只在最后一个点显示当前值
      
      datasets.push({
        label: language,
        data: data,
        borderColor: color,
        backgroundColor: `${color}19`, // 10% opacity
        fill: false,
        tension: 0.3,
        borderWidth: 2,
        pointRadius: 2,
        pointBackgroundColor: color
      })
    })
  }
  
  return {
    type: 'line' as const,
    data: {
      labels: labels,
      datasets: datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top' as const,
          labels: {
            color: '#94a3b8',
            font: {
              size: 12
            },
            padding: 15
          }
        },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.9)',
          titleColor: '#e2e8f0',
          bodyColor: '#94a3b8',
          borderColor: 'rgba(100, 116, 139, 0.3)',
          borderWidth: 1,
          padding: 12,
          boxPadding: 6,
          usePointStyle: true,
          callbacks: {
            label: function(context: any) {
              return `${context.dataset.label}: ${context.raw} 个项目`
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            color: 'rgba(100, 116, 139, 0.1)',
            drawBorder: false
          },
          ticks: {
            color: '#94a3b8',
            font: {
              size: 10
            },
            maxRotation: 45,
            minRotation: 0
          }
        },
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(100, 116, 139, 0.1)',
            drawBorder: false
          },
          ticks: {
            color: '#94a3b8',
            font: {
              size: 10
            },
            callback: function(value: any) {
              return value.toString()
            }
          }
        }
      },
      interaction: {
        intersect: false,
        mode: 'index' as const
      },
      elements: {
        line: {
          borderWidth: 2
        },
        point: {
          radius: 0,
          hoverRadius: 5
        }
      }
    }
  }
}

// 获取项目类型分布图表配置
function getProjectTypeChartConfig() {
  // 项目类型颜色映射
  const typeColors = [
    '#6366f1', // 主色
    '#8b5cf6', // 次要色
    '#ec4899', // 强调色
    '#10b981', // 成功色
    '#f59e0b', // 警告色
    '#6b7280'  // 中性色
  ]
  
  // 仅使用从props获取的真实数据
  // 使用类型断言安全地访问project_types属性
  const projectTypes = props.trendsData && (props.trendsData as any).project_types && (props.trendsData as any).project_types.length > 0
    ? (props.trendsData as any).project_types
    : []
  
  // 转换为图表数据格式
  const labels = projectTypes.map((item: { type: string }) => item.type)
  const data = projectTypes.map((item: { count: number }) => item.count)
  const backgroundColor = typeColors.slice(0, data.length)
  
  return {
    type: 'doughnut' as const,
    data: {
      labels: labels,
      datasets: [
        {
          data: data,
          backgroundColor: backgroundColor,
          borderColor: 'rgba(15, 23, 42, 0.3)',
          borderWidth: 2,
          hoverOffset: 8
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: {
        legend: {
          position: 'bottom' as const,
          labels: {
            color: '#94a3b8',
            font: {
              size: 12
            },
            padding: 15
          }
        },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.9)',
          titleColor: '#e2e8f0',
          bodyColor: '#94a3b8',
          borderColor: 'rgba(100, 116, 139, 0.3)',
          borderWidth: 1,
          padding: 12,
          callbacks: {
            label: function(context: any) {
              const total = context.dataset.data.reduce((sum: number, value: number) => sum + value, 0)
              const percentage = Math.round((context.raw / total) * 100)
              return `${context.label}: ${context.raw} 个项目 (${percentage}%)`
            }
          }
        }
      }
    }
  }
}

// 生成时间标签
function generateTimeLabels() {
  const labels: string[] = []
  const today = new Date()
  let daysCount = 7
  
  // 根据选择的时间窗口确定生成多少个标签
  switch (selectedWindow.value) {
    case '7天':
      daysCount = 7
      break
    case '30天':
      daysCount = 6 // 每5天一个标签
      break
    case '90天':
      daysCount = 6 // 每15天一个标签
      break
    case '1年':
      daysCount = 6 // 每2个月一个标签
      break
  }
  
  // 生成标签
  for (let i = daysCount - 1; i >= 0; i--) {
    let date: Date
    let labelFormat: Intl.DateTimeFormatOptions
    
    switch (selectedWindow.value) {
      case '7天':
        date = new Date(today.getTime() - i * 24 * 60 * 60 * 1000)
        labelFormat = { month: 'short', day: 'numeric' }
        break
      case '30天':
        date = new Date(today.getTime() - i * 5 * 24 * 60 * 60 * 1000)
        labelFormat = { month: 'short', day: 'numeric' }
        break
      case '90天':
        date = new Date(today.getTime() - i * 15 * 24 * 60 * 60 * 1000)
        labelFormat = { month: 'short', day: 'numeric' }
        break
      case '1年':
        date = new Date(today.getFullYear(), today.getMonth() - i * 2, 1)
        labelFormat = { year: '2-digit', month: 'short' }
        break
      default:
        date = new Date(today.getTime() - i * 5 * 24 * 60 * 60 * 1000)
        labelFormat = { month: 'short', day: 'numeric' }
    }
    
    labels.push(date.toLocaleDateString('zh-CN', labelFormat))
  }
  
  return labels
}

// 格式化日期
function formatDate(date: Date): string {
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 格式化数字
function formatNumber(num: number): string {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

// 刷新趋势数据
async function refreshTrendsData() {
  // 这里可以添加实际的数据刷新逻辑，从API获取最新数据
  // 例如：
  // try {
  //   const newTrendsData = await getTrends({ days: getDaysFromWindow(selectedWindow.value) })
  //   // 更新组件数据
  // } catch (error) {
  //   console.error('刷新趋势数据失败:', error)
  // }
  
  // 目前仅更新图表显示
  updateCharts()
}

// 将时间窗口转换为天数
function getDaysFromWindow(window: string): number {
  switch (window) {
    case '7天':
      return 7
    case '30天':
      return 30
    case '90天':
      return 90
    case '1年':
      return 365
    default:
      return 30
  }
}

// 关闭模态框
function handleClose() {
  emit('close')
}

// 组件卸载时销毁图表
onMounted(() => {
  if (props.visible) {
    initCharts()
  }
})
</script>

<style scoped>
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

/* 玻璃态卡片样式 */
.glass-card {
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(100, 116, 139, 0.2);
}

/* 动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease forwards;
}

/* 滚动条样式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(100, 116, 139, 0.1);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(100, 116, 139, 0.5);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(100, 116, 139, 0.7);
}

/* 自定义滚动条样式 */
.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: rgba(100, 116, 139, 0.1);
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: rgba(100, 116, 139, 0.5);
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(100, 116, 139, 0.7);
}

/* 表格样式 */
table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  padding: 8px;
  text-align: left;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .time-windows {
    overflow-x: auto;
    padding-bottom: 10px;
  }
  
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  .max-w-6xl {
    max-width: 100%;
  }
}
</style>