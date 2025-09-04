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
          <div class="glass-card p-6 rounded-xl">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-white">项目活跃度指数</h3>
              <span class="text-xs font-bold text-green-400">+12.8%</span>
            </div>
            <div class="flex items-end space-x-3">
              <div class="text-3xl font-bold text-white">87.4</div>
              <div class="text-sm text-slate-400 mb-1">活跃度评分</div>
            </div>
          </div>
          
          <div class="glass-card p-6 rounded-xl">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-white">技术创新热度</h3>
              <span class="text-xs font-bold text-green-400">+23.5%</span>
            </div>
            <div class="flex items-end space-x-3">
              <div class="text-3xl font-bold text-white">76.2</div>
              <div class="text-sm text-slate-400 mb-1">创新指数</div>
            </div>
          </div>
          
          <div class="glass-card p-6 rounded-xl">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-white">社区参与度</h3>
              <span class="text-xs font-bold text-red-400">-2.1%</span>
            </div>
            <div class="flex items-end space-x-3">
              <div class="text-3xl font-bold text-white">62.8</div>
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
          <div class="overflow-x-auto">
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
        </div>
        
        <!-- 趋势洞察报告 -->
        <div class="glass-card p-6 rounded-xl">
          <h3 class="text-lg font-semibold text-white mb-6">趋势洞察分析报告</h3>
          <div class="prose prose-invert max-w-none">
            <p class="text-slate-300 mb-4">
              根据最近{{ selectedWindow }}的数据分析，我们观察到以下几个显著的技术趋势:
            </p>
            
            <h4 class="text-white text-lg font-medium mb-2">生成式AI持续爆发增长</h4>
            <p class="text-slate-300 mb-4">
              生成式AI相关项目在过去{{ selectedWindow }}中增长了<span class="text-green-400 font-semibold">125%</span>，特别是在代码生成、内容创作和多模态AI领域出现了大量创新项目。这一趋势反映了开发者社区对AI辅助工具的强烈需求。
            </p>
            
            <h4 class="text-white text-lg font-medium mb-2">TypeScript仍是主流选择</h4>
            <p class="text-slate-300 mb-4">
              TypeScript继续保持其主导地位，在所有新项目中占比达到<span class="text-primary font-semibold">35%</span>，超过了JavaScript成为最受欢迎的开发语言。其静态类型系统和现代JavaScript特性为大型项目开发提供了更好的保障。
            </p>
            
            <h4 class="text-white text-lg font-medium mb-2">WebAssembly应用范围扩大</h4>
            <p class="text-slate-300 mb-4">
              WebAssembly技术在过去{{ selectedWindow }}展现出<span class="text-green-400 font-semibold">87%</span>的增长率，其应用场景已从Web前端扩展到云原生、边缘计算等领域，为高性能Web应用提供了新的可能性。
            </p>
            
            <h4 class="text-white text-lg font-medium mb-2">结论与建议</h4>
            <p class="text-slate-300">
              开发者和技术团队应密切关注生成式AI与各自领域的结合点，同时考虑在新项目中采用TypeScript以提高代码质量和开发效率。对于性能敏感型应用，WebAssembly也是一个值得探索的方向。建议团队在技术选型时充分评估这些新兴技术的潜力和适用场景。
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
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

// 模拟技术领域数据
const techAreas = ref([
  {
    name: '生成式AI',
    project_count: 156,
    growth_rate: 125,
    avg_stars: 4872,
    activity_score: 92,
    bgClass: 'bg-purple-500/20',
    icon: 'IconEcosystem'
  },
  {
    name: 'WebAssembly',
    project_count: 87,
    growth_rate: 87,
    avg_stars: 3245,
    activity_score: 85,
    bgClass: 'bg-blue-500/20',
    icon: 'IconTooling'
  },
  {
    name: '边缘计算',
    project_count: 63,
    growth_rate: 63,
    avg_stars: 2876,
    activity_score: 78,
    bgClass: 'bg-green-500/20',
    icon: 'IconCommunity'
  },
  {
    name: '低代码平台',
    project_count: 45,
    growth_rate: 45,
    avg_stars: 3124,
    activity_score: 72,
    bgClass: 'bg-pink-500/20',
    icon: 'IconDocumentation'
  },
  {
    name: '区块链应用',
    project_count: 38,
    growth_rate: 12,
    avg_stars: 1987,
    activity_score: 65,
    bgClass: 'bg-orange-500/20',
    icon: 'IconSupport'
  },
  {
    name: '量子计算',
    project_count: 24,
    growth_rate: 35,
    avg_stars: 2654,
    activity_score: 60,
    bgClass: 'bg-cyan-500/20',
    icon: 'IconEcosystem'
  }
])

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
  // 根据选择的时间窗口生成模拟数据
  const labels = generateTimeLabels()
  
  return {
    type: 'line' as const,
    data: {
      labels: labels,
      datasets: [
        {
          label: 'TypeScript',
          data: generateTrendData(labels.length, 100, 350, 10),
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99, 102, 241, 0.1)',
          fill: true,
          tension: 0.3,
          borderWidth: 2,
          pointRadius: 2,
          pointBackgroundColor: '#6366f1'
        },
        {
          label: 'JavaScript',
          data: generateTrendData(labels.length, 80, 300, 5),
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
          fill: true,
          tension: 0.3,
          borderWidth: 2,
          pointRadius: 2,
          pointBackgroundColor: '#f59e0b'
        },
        {
          label: 'Python',
          data: generateTrendData(labels.length, 70, 280, 8),
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          fill: true,
          tension: 0.3,
          borderWidth: 2,
          pointRadius: 2,
          pointBackgroundColor: '#10b981'
        },
        {
          label: 'Go',
          data: generateTrendData(labels.length, 30, 120, 3),
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          fill: true,
          tension: 0.3,
          borderWidth: 2,
          pointRadius: 2,
          pointBackgroundColor: '#3b82f6'
        }
      ]
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
  return {
    type: 'doughnut' as const,
    data: {
      labels: ['前端框架', '后端服务', 'AI/ML', '工具库', 'DevOps', '其他'],
      datasets: [
        {
          data: [28, 22, 20, 15, 10, 5],
          backgroundColor: [
            '#6366f1', // 主色
            '#8b5cf6', // 次要色
            '#ec4899', // 强调色
            '#10b981', // 成功色
            '#f59e0b', // 警告色
            '#6b7280'  // 中性色
          ],
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
            padding: 20,
            usePointStyle: true,
            pointStyle: 'circle'
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
              const label = context.label || ''
              const value = context.raw || 0
              return `${label}: ${value}%`
            }
          }
        }
      },
      animation: {
        animateRotate: true,
        animateScale: true
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

// 生成趋势数据
function generateTrendData(count: number, min: number, max: number, trend: number) {
  const data: number[] = []
  let currentValue = Math.floor(Math.random() * (max - min)) + min
  
  for (let i = 0; i < count; i++) {
    // 添加一些随机波动
    const fluctuation = Math.floor(Math.random() * 20) - 10
    currentValue = Math.max(min, Math.min(max, currentValue + fluctuation + trend))
    data.push(currentValue)
  }
  
  return data
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
function refreshTrendsData() {
  // 这里可以添加实际的数据刷新逻辑
  updateCharts()
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