<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-2 backdrop-blur-sm sm:p-4 animate-fadeIn" @click="handleOverlayClick">
      <div
        class="report-reader max-h-[95vh] w-full max-w-6xl overflow-hidden flex flex-col animate-fadeInUp"
        @click.stop
      >
        <!-- 模态框头部 -->
        <header class="relative border-b border-cyan-100 bg-gradient-to-r from-cyan-50 to-white p-4 lg:p-5">
          <div class="flex justify-between items-center">
              <div class="flex items-center space-x-3 lg:space-x-4 flex-1 min-w-0">
                <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-2xl border border-cyan-200 bg-cyan-100 text-cyan-700 shadow-sm lg:h-11 lg:w-11">
                  <svg class="h-5 w-5 lg:h-6 lg:w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <div class="min-w-0 flex-1">
                  <p class="mb-1 text-[10px] uppercase tracking-[0.22em] text-cyan-700/80">INTELLIGENCE REPORT</p>
                  <h3 class="truncate text-lg font-semibold text-slate-900 lg:text-2xl">
                    GitHub 热门项目报告
                  </h3>
                  <p class="mt-1 truncate text-xs text-slate-500 lg:text-sm">
                    {{ formatDate(report.date) }}
                  </p>
                </div>
              </div>

            <div class="flex items-center space-x-2 lg:space-x-3 flex-shrink-0">
              <!-- 关闭按钮 -->
              <button
                @click="$emit('close')"
                class="reader-icon-button"
                title="关闭"
              >
                <svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- 进度条 -->
          <div class="absolute bottom-0 left-0 h-0.5 w-full bg-cyan-100">
            <div
              class="h-full bg-cyan-500 transition-all duration-300 ease-out"
              :style="{ width: scrollProgress + '%' }"
            ></div>
          </div>
        </header>

        <!-- 模态框内容 -->
        <main 
          ref="contentContainer"
          class="flex-grow overflow-y-auto relative"
          @scroll="updateScrollProgress"
        >
          <div v-if="loading" class="h-full flex flex-col items-center justify-center py-20">
            <div class="relative mb-8">
              <div class="w-16 h-16 border-4 border-cyan-200 rounded-full animate-spin"></div>
              <div class="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-t-cyan-500 rounded-full animate-spin"></div>
            </div>
            <h4 class="text-lg font-medium text-slate-700 mb-2">加载中</h4>
            <p class="text-slate-500">正在解析报告内容...</p>
          </div>

          <div v-else class="p-4 lg:p-6">
            <!-- 报告统计信息 -->
            <div class="mb-5 grid grid-cols-2 gap-3 lg:grid-cols-4">
              <div class="reader-stat">
                <div class="stat-value">{{ report.project_count }}</div>
                <div class="stat-label">项目数量</div>
              </div>
              <div class="reader-stat">
                <div class="stat-value">{{ wordCount.toLocaleString() }}</div>
                <div class="stat-label">字数统计</div>
              </div>
              <div class="reader-stat">
                <div class="stat-value">{{ readingTime }}</div>
                <div class="stat-label">阅读时间</div>
              </div>
              <div class="reader-stat">
                <div class="stat-value">{{ formatDate(report.date).split(' ')[0] }}</div>
                <div class="stat-label">发布日期</div>
              </div>
            </div>

            <!-- Markdown 内容 -->
            <div
              ref="markdownContainer"
              class="markdown-content max-w-none border border-cyan-100 bg-white/80 p-4 text-sm lg:p-6 lg:text-base"
              v-html="renderedContent"
            ></div>
          </div>
          
          <!-- 返回顶部按钮 - 移至左下角避免与导出按钮重叠 -->
          <!-- <button 
            v-show="showBackToTop"
            @click="scrollToTop"
            class="fixed bottom-8 left-8 btn-primary w-12 h-12 rounded-full shadow-lg animate-bounce-gentle z-10"
            title="返回顶部"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11l5-5m0 0l5 5m-5-5v12"></path>
            </svg>
          </button> -->
        </main>

        <!-- 模态框底部 -->
        <footer class="border-t border-cyan-100 bg-gradient-to-r from-white to-cyan-50 p-4 lg:p-5">
          <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center space-y-4 lg:space-y-0">
            <div class="flex flex-wrap items-center gap-4 lg:gap-6 text-xs lg:text-sm text-slate-500">
              <div class="flex items-center space-x-1 lg:space-x-2">
                <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
                <span>{{ report.project_count }} 个项目</span>
              </div>
              <div class="flex items-center space-x-1 lg:space-x-2">
                <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
                <span>{{ wordCount.toLocaleString() }} 字</span>
              </div>
              <div class="flex items-center space-x-1 lg:space-x-2">
                <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>{{ readingTime }}</span>
              </div>
            </div>
            
            <div class="flex flex-wrap gap-2 lg:gap-3 w-full lg:w-auto">
              <button
                @click="copyToClipboard"
                :class="['reader-action flex-1 lg:flex-none text-xs lg:text-sm transition-colors duration-300', isCopying ? 'bg-green-600/20 border-green-500/50 text-green-200' : '']"
                title="复制到剪贴板"
                :disabled="isCopying"
              >
                <svg class="w-3 h-3 lg:w-4 lg:h-4 mr-1 lg:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                </svg>
                {{ isCopying ? '已复制!' : '复制' }}
              </button>
              
              <div class="relative" ref="exportDropdown">
                <button
                  @click="showExportMenu = !showExportMenu"
                  class="reader-action primary flex-1 lg:flex-none text-xs lg:text-sm"
                  title="导出报告"
                >
                  <svg class="w-3 h-3 lg:w-4 lg:h-4 mr-1 lg:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  导出
                  <svg class="w-3 h-3 lg:w-4 lg:h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </button>
                
                <!-- 导出菜单 -->
                <div v-if="showExportMenu" class="absolute bottom-full right-0 mb-2 w-48 border border-cyan-100 bg-white py-2 shadow-lg rounded-lg overflow-hidden">
                  <button @click="exportReport('md')" class="export-menu-item">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    Markdown 格式
                  </button>
                  <button @click="exportReport('html')" class="export-menu-item">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                    </svg>
                    HTML 格式
                  </button>
                </div>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import type { Report } from '../api/reports'
import { renderMarkdown, enhanceMarkdownDisplay } from '../utils/markdown-simple'

// Props
const props = defineProps<{
  report: Report
  theme: 'light' | 'dark' // Add theme prop
}>()

// Emits
const emit = defineEmits<{
  close: []
}>()

// 响应式数据
const loading = ref(false)
const markdownContainer = ref<HTMLElement>()
const isCopying = ref(false)
const contentContainer = ref<HTMLElement>()
const exportDropdown = ref<HTMLElement>()
const showExportMenu = ref(false)
const scrollProgress = ref(0)
const showBackToTop = ref(false)

// 使用ref存储渲染后的内容
const renderedContent = ref('<p class="text-slate-400">暂无报告内容</p>')

const wordCount = computed(() => {
  if (!props.report.content) return 0
  return props.report.content.replace(/\s/g, '').length
})

const readingTime = computed(() => {
  const wordsPerMinute = 300 // 中文阅读速度
  const minutes = Math.ceil(wordCount.value / wordsPerMinute)
  return minutes + ' 分钟'
})

// 异步渲染Markdown内容
async function updateRenderedContent(content: string) {
  if (!content) {
    renderedContent.value = '<p class="text-slate-400">暂无报告内容</p>'
    return
  }
  try {
    const html = await renderMarkdown(content)
    renderedContent.value = html
  } catch (error) {
    console.error('渲染Markdown内容失败:', error)
    renderedContent.value = `<div class="text-red-500 p-4 border border-red-200 rounded-lg bg-red-50">渲染失败: ${error}</div>`
  }
}

// 监听报告内容变化
watch(() => props.report.content, async (newContent: string | undefined) => {
  await updateRenderedContent(newContent || '')
}, { immediate: true })

// 生命周期钩子
onMounted(async () => {
  // 添加事件监听器
  document.addEventListener('keydown', handleKeydown)
  document.addEventListener('click', handleOutsideClick)
  
  // 防止背景滚动
  document.body.style.overflow = 'hidden'
  
  // 等待DOM渲染完成后增强Markdown显示效果
  await nextTick()
  if (markdownContainer.value) {
    enhanceMarkdownDisplay(markdownContainer.value)
  }
})

onUnmounted(() => {
  // 清理事件监听器
  document.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('click', handleOutsideClick)
  
  // 恢复背景滚动
  document.body.style.overflow = ''
})

// 事件处理函数
function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    emit('close')
  }
}

// 点击背景遮罩层关闭模态框
function handleOverlayClick() {
  emit('close')
}

function handleOutsideClick(e: Event) {
  // 处理导出菜单关闭
  if (showExportMenu.value && exportDropdown.value && !exportDropdown.value.contains(e.target as Node)) {
    showExportMenu.value = false
  }
  
  // 处理点击模态框外部关闭整个模态框
  const targetElement = e.target as HTMLElement
  
  // 获取模态框背景遮罩层
  const modalOverlay = document.querySelector('.fixed.inset-0')
  
  // 获取模态框内容区域
  const modalContent = document.querySelector('.report-reader')
  
  // 当点击的是背景遮罩层，且不是点击在内容区域上时，关闭模态框
  if (modalOverlay && modalContent && 
      (targetElement === modalOverlay || modalOverlay.contains(targetElement)) && 
      !modalContent.contains(targetElement)) {
    emit('close')
  }
}

function updateScrollProgress() {
  if (!contentContainer.value) return
  
  const { scrollTop, scrollHeight, clientHeight } = contentContainer.value
  const progress = (scrollTop / (scrollHeight - clientHeight)) * 100
  scrollProgress.value = Math.min(100, Math.max(0, progress))
  
  // 显示/隐藏返回顶部按钮
  showBackToTop.value = scrollTop > 300
}

function scrollToTop() {
  if (contentContainer.value) {
    contentContainer.value.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }
}


// 工具函数
function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
}

function exportReport(format: 'md' | 'html' = 'md') {
  if (!props.report.content) return
  
  let content: string
  let mimeType: string
  let extension: string
  
  switch (format) {
    case 'html':
      // 使用简单的字符串拼接避免模板字符串解析问题
      let htmlContent = ''
      htmlContent += '<!DOCTYPE html>\n'
      htmlContent += '<html lang="zh-CN">\n'
      htmlContent += '<head>\n'
      htmlContent += '  <meta charset="UTF-8">\n'
      htmlContent += '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
      htmlContent += '  <title>GitHub 热门项目报告 - ' + props.report.date + '</title>\n'
      htmlContent += '  <style>\n'
      htmlContent += '    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }\n'
      htmlContent += '    h1, h2, h3, h4, h5, h6 { color: #2c3e50; margin-top: 1.5em; margin-bottom: 0.5em; }\n'
      htmlContent += '    p { margin: 1em 0; }\n'
      htmlContent += '    code { background: #f4f4f4; padding: 2px 4px; border-radius: 3px; font-family: "Consolas", "Monaco", monospace; }\n'
      htmlContent += '    pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }\n'
      htmlContent += '    pre code { background: transparent; padding: 0; }\n'
      htmlContent += '    a { color: #3498db; text-decoration: none; }\n'
      htmlContent += '    a:hover { text-decoration: underline; }\n'
      htmlContent += '    blockquote { border-left: 4px solid #ddd; padding-left: 1em; margin: 1em 0; color: #666; }\n'
      htmlContent += '    ul, ol { margin: 1em 0; padding-left: 2em; }\n'
      htmlContent += '    li { margin: 0.5em 0; }\n'
      htmlContent += '    img { max-width: 100%; height: auto; }\n'
      htmlContent += '    table { border-collapse: collapse; width: 100%; margin: 1em 0; }\n'
      htmlContent += '    th, td { padding: 8px 12px; border: 1px solid #ddd; text-align: left; }\n'
      htmlContent += '    th { background-color: #f4f4f4; }\n'
      htmlContent += '  </style>\n'
      htmlContent += '</head>\n'
      htmlContent += '<body>\n'
      htmlContent += renderedContent.value + '\n'
      htmlContent += '</body>\n'
      htmlContent += '</html>'
      
      content = htmlContent
      mimeType = 'text/html'
      extension = 'html'
      break
    default:
      content = props.report.content
      mimeType = 'text/markdown'
      extension = 'md'
  }
  
  const blob = new Blob([content], { type: mimeType + ';charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'github_trending_' + props.report.date + '.' + extension
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
  
  showExportMenu.value = false
  console.log('📥 报告已导出为 ' + format.toUpperCase() + ' 格式')
}

async function copyToClipboard() {
  if (!props.report.content) return
  
  try {
    await navigator.clipboard.writeText(props.report.content)
    console.log('📋 内容已复制到剪贴板')
    
    // 设置复制状态为成功
    isCopying.value = true
    
    // 2秒后恢复原始状态
    setTimeout(() => {
      isCopying.value = false
    }, 2000)
  } catch (err) {
    console.error('复制失败:', err)
    
    // 可以添加复制失败的处理逻辑，例如弹出错误提示
    alert('复制失败，请重试')
  }
}

</script>

<style scoped>
  .report-reader {
    position: relative;
    border: 1px solid rgba(26, 150, 184, 0.2);
    border-radius: 1.25rem;
    background: linear-gradient(160deg, #f4fdff 0%, #ffffff 45%, #e6f7fb 100%);
    box-shadow: 0 24px 80px rgba(8, 61, 82, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.6);
  }

  .reader-icon-button {
    display: inline-flex;
    height: 2.5rem;
    width: 2.5rem;
    align-items: center;
    justify-content: center;
    border-radius: 9999px;
    border: 1px solid rgba(26, 150, 184, 0.18);
    background: #ffffff;
    color: #94a3b8;
    transition: all 0.2s ease;
  }

  .reader-icon-button:hover {
    border-color: rgba(248, 113, 113, 0.4);
    background: rgba(254, 226, 226, 0.6);
    color: #f87171;
  }

  .reader-stat {
    border: 1px solid rgba(26, 150, 184, 0.18);
    background: rgba(255, 255, 255, 0.85);
    border-radius: 0.75rem;
    padding: 0.85rem;
    text-align: center;
  }

  .stat-value {
    margin-bottom: 0.3rem;
    overflow-wrap: anywhere;
    font-size: 1.35rem;
    font-weight: 600;
    color: #0e7490;
  }

  .stat-label {
    font-size: 0.72rem;
    color: #3a9ab8;
  }

  .reader-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 0.5rem;
    border: 1px solid rgba(26, 150, 184, 0.25);
    background: #ffffff;
    padding: 0.55rem 0.85rem;
    color: #127a98;
    transition: all 0.2s ease;
  }

  .reader-action:hover {
    border-color: rgba(26, 150, 184, 0.5);
    background: rgba(26, 150, 184, 0.08);
    color: #0a2d3d;
  }

  .reader-action.primary {
    border-color: rgba(26, 150, 184, 0.45);
    background: rgba(26, 150, 184, 0.12);
    color: #0a2d3d;
  }

  .export-menu-item {
    display: flex;
    width: 100%;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    font-size: 0.82rem;
    color: #127a98;
    text-align: left;
    transition: background 0.15s ease, color 0.15s ease;
  }

  .export-menu-item:hover {
    background: rgba(26, 150, 184, 0.08);
    color: #0a2d3d;
  }

</style>
