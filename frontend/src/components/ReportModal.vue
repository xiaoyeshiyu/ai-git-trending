<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-2 sm:p-4 animate-fadeIn backdrop-blur-sm" @click="handleOverlayClick">
      <div 
        class="glass-card rounded-2xl lg:rounded-3xl max-w-6xl w-full max-h-[95vh] overflow-hidden flex flex-col animate-fadeInUp shadow-2xl"
        @click.stop
      >
        <!-- 模态框头部 -->
        <header class="relative p-4 lg:p-6 border-b border-white/10 bg-gradient-to-r from-slate-800/50 to-slate-700/50">
          <div class="flex justify-between items-center">
              <div class="flex items-center space-x-3 lg:space-x-4 flex-1 min-w-0">
                <div class="w-10 h-10 lg:w-12 lg:h-12 bg-gradient-primary rounded-xl flex items-center justify-center flex-shrink-0">
                  <svg class="w-5 h-5 lg:w-6 lg:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <div class="min-w-0 flex-1">
                  <h3 style="background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899); background-clip: text; -webkit-background-clip: text; color: transparent;" class="text-lg lg:text-2xl font-bold truncate">
                    GitHub 热门项目报告
                  </h3>
                  <p class="text-xs lg:text-sm text-slate-400 mt-1 truncate">
                    {{ formatDate(report.date) }}
                  </p>
                </div>
              </div>
            
            <div class="flex items-center space-x-2 lg:space-x-3 flex-shrink-0">
              <!-- 关闭按钮 -->
              <button
                @click="$emit('close')"
                class="btn-icon hover:bg-red-500/20 hover:border-red-500/30 hover:text-red-400"
                title="关闭"
              >
                <svg class="w-4 h-4 lg:w-5 lg:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
          </div>
          
          <!-- 进度条 -->
          <div class="absolute bottom-0 left-0 w-full h-0.5 lg:h-1 bg-slate-700/50">
            <div 
              class="h-full bg-gradient-primary transition-all duration-300 ease-out"
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
              <div class="w-16 h-16 border-4 border-blue-500/30 rounded-full animate-spin"></div>
              <div class="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-t-blue-500 rounded-full animate-spin"></div>
            </div>
            <h4 class="text-lg font-medium text-slate-300 mb-2">加载中</h4>
            <p class="text-slate-400">正在解析报告内容...</p>
          </div>
          
          <div v-else class="p-4 lg:p-8">
            <!-- 报告统计信息 -->
            <div class="mb-6 lg:mb-8 grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4">
              <div class="glass-card rounded-xl p-3 lg:p-4 text-center hover:shadow-lg transition-shadow">
                <div class="text-lg lg:text-2xl font-bold text-blue-400 mb-1">{{ report.project_count }}</div>
                <div class="text-xs lg:text-sm text-slate-400">项目数量</div>
              </div>
              <div class="glass-card rounded-xl p-3 lg:p-4 text-center hover:shadow-lg transition-shadow">
                <div class="text-lg lg:text-2xl font-bold text-green-400 mb-1">{{ wordCount.toLocaleString() }}</div>
                <div class="text-xs lg:text-sm text-slate-400">字数统计</div>
              </div>
              <div class="glass-card rounded-xl p-3 lg:p-4 text-center hover:shadow-lg transition-shadow">
                <div class="text-lg lg:text-2xl font-bold text-purple-400 mb-1">{{ readingTime }}</div>
                <div class="text-xs lg:text-sm text-slate-400">阅读时间</div>
              </div>
              <div class="glass-card rounded-xl p-3 lg:p-4 text-center hover:shadow-lg transition-shadow">
                <div class="text-lg lg:text-2xl font-bold text-pink-400 mb-1">{{ formatDate(report.date).split(' ')[0] }}</div>
                <div class="text-xs lg:text-sm text-slate-400">发布日期</div>
              </div>
            </div>
            

            
            <!-- Markdown 内容 -->
            <div 
              ref="markdownContainer"
              class="markdown-content prose prose-invert max-w-none bg-slate-900/30 rounded-xl p-4 lg:p-6 border border-slate-600/30 text-sm lg:text-base"
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
        <footer class="p-4 lg:p-6 border-t border-white/10 bg-slate-800/30">
          <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center space-y-4 lg:space-y-0">
            <div class="flex flex-wrap items-center gap-4 lg:gap-6 text-xs lg:text-sm text-slate-400">
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
                :class="['btn-secondary flex-1 lg:flex-none text-xs lg:text-sm transition-colors duration-300', isCopying ? 'bg-green-600/80 border-green-500/50' : '']"
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
                  class="btn-primary flex-1 lg:flex-none text-xs lg:text-sm"
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
                <div v-if="showExportMenu" class="absolute bottom-full right-0 mb-2 w-48 glass-card rounded-xl py-2 shadow-xl">
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
import { ref, computed, onMounted, nextTick, onUnmounted, watch } from 'vue'
import type { Report } from '../api/reports'
import MarkdownIt from 'markdown-it'
// 导入已安装的markdown-it插件
import abbrPlugin from 'markdown-it-abbr'
import anchorPlugin from 'markdown-it-anchor'
import * as emojiPlugin from 'markdown-it-emoji'
import footnotePlugin from 'markdown-it-footnote'
import insPlugin from 'markdown-it-ins'
import markPlugin from 'markdown-it-mark'
import subPlugin from 'markdown-it-sub'
import supPlugin from 'markdown-it-sup'
import taskListsPlugin from 'markdown-it-task-lists'
import tocPlugin from 'markdown-it-toc-done-right'

// 创建增强的MarkdownIt实例，添加更多配置以支持复杂的markdown格式
const md = new MarkdownIt({
  html: true,
  xhtmlOut: false,
  breaks: true,
  langPrefix: 'language-',
  linkify: true,
  typographer: true,
  highlight: function(str, lang) {
    // 添加代码高亮支持
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value;
      } catch (__) {}
    }
    return ''; // use external default escaping
  }
})

// 启用所有已安装的markdown-it插件
try {
  md.use(abbrPlugin)
  md.use(anchorPlugin, {
    level: 1,
    permalink: true,
    permalinkClass: 'header-anchor',
    permalinkSymbol: '🔗'
  })
  md.use(emojiPlugin)
  md.use(footnotePlugin)
  md.use(insPlugin)
  md.use(markPlugin)
  md.use(subPlugin)
  md.use(supPlugin)
  md.use(taskListsPlugin)
  md.use(tocPlugin, {
    level: 2,
    title: '目录'
  })
} catch (error) {
  console.error('Error loading markdown-it plugins:', error)
}

// 引入highlight.js用于代码高亮
import hljs from 'highlight.js/lib/core';
// 导入常用语言的高亮支持
import javascript from 'highlight.js/lib/languages/javascript';
import python from 'highlight.js/lib/languages/python';
import typescript from 'highlight.js/lib/languages/typescript';
import go from 'highlight.js/lib/languages/go';
import rust from 'highlight.js/lib/languages/rust';
import html from 'highlight.js/lib/languages/xml';
import css from 'highlight.js/lib/languages/css';

// 注册语言
hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('python', python);
hljs.registerLanguage('typescript', typescript);
hljs.registerLanguage('go', go);
hljs.registerLanguage('rust', rust);
hljs.registerLanguage('html', html);
hljs.registerLanguage('css', css);

// 预处理Markdown内容的函数
function preprocessMarkdown(content: string): string {
  if (!content) return ''
  
  // 添加调试日志（可根据需要启用）
  // console.log('原始内容预览:', content.substring(0, 100) + '...')
  
  // 清理可能存在的特殊字符和格式问题
  let processedContent = content
    // 处理转义字符问题 - 正确处理实际的转义序列
    .replace(/\\([\nrt])/g, (match, char) => {
      const escapeMap = { 'n': '\n', 'r': '\r', 't': '\t' }
      return escapeMap[char as keyof typeof escapeMap] || match
    })
    // 修复表格格式问题
    .replace(/\|\s+\|/g, '||')
    // 确保代码块的正确格式
    .replace(/```([\w]+)?\s*\n/g, (match, lang) => {
      return '```' + (lang || '') + '\n'
    })
    // 修复标题格式 - 确保标题前没有多余空格
    .replace(/^(\s*#)/gm, (match) => match.trimStart())
    // 处理列表项 - 确保列表标记后的空格正确
    .replace(/^(\s*[*+-]|\d+\.)\s*/gm, (match) => {
      // 确保列表标记后至少有一个空格
      return match.trimEnd() + ' '
    })
    // 处理可能存在的引用格式问题
    .replace(/^(\s*>)/gm, (match) => match.trimEnd() + ' ')
    
  // 调试日志
  // console.log('处理后内容预览:', processedContent.substring(0, 100) + '...')
  
  return processedContent
}

// 渲染Markdown内容
function renderMarkdown(content: string): string {
  const processedContent = preprocessMarkdown(content || '')
  return md.render(processedContent)
}

// 增强Markdown显示的函数，现在在内容更新后也会调用
function enhanceMarkdownDisplay(container: HTMLElement): void {
  // 确保container存在
  if (!container) return;
  // 添加代码块复制功能
  const codeBlocks = container.querySelectorAll('pre code')
  codeBlocks.forEach(block => {
    const pre = block.parentElement
    if (!pre) return
    
    const button = document.createElement('button')
    button.className = 'absolute top-2 right-2 bg-slate-700/80 hover:bg-slate-600/80 text-white rounded px-2 py-1 text-xs transition-colors'
    button.textContent = '复制'
    button.onclick = () => {
      navigator.clipboard.writeText(block.textContent || '')
        .then(() => {
          const originalText = button.textContent
          button.textContent = '已复制!'
          button.classList.add('bg-green-600/80')
          setTimeout(() => {
            button.textContent = originalText
            button.classList.remove('bg-green-600/80')
          }, 2000)
        })
        .catch(err => {
          console.error('复制失败:', err)
          button.textContent = '复制失败'
          button.classList.add('bg-red-600/80')
          setTimeout(() => {
            button.textContent = '复制'
            button.classList.remove('bg-red-600/80')
          }, 2000)
        })
    }
    
    pre.style.position = 'relative'
    pre.appendChild(button)
  })
  
  // 添加链接打开新窗口的target属性
  const links = container.querySelectorAll('a:not([target])')
  links.forEach(link => {
    link.setAttribute('target', '_blank')
    link.setAttribute('rel', 'noopener noreferrer')
  })
}

// Props
const props = defineProps<{
  report: Report
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

// 计算属性
const renderedContent = computed(() => {
  if (!props.report.content) return '<p class="text-slate-400">暂无报告内容</p>'
  return renderMarkdown(props.report.content)
})

// 监听content变化，重新应用增强显示
watch(() => props.report.content, async () => {
  await nextTick()
  if (markdownContainer.value) {
    enhanceMarkdownDisplay(markdownContainer.value)
  }
})

const wordCount = computed(() => {
  if (!props.report.content) return 0
  return props.report.content.replace(/\s/g, '').length
})

const readingTime = computed(() => {
  const wordsPerMinute = 300 // 中文阅读速度
  const minutes = Math.ceil(wordCount.value / wordsPerMinute)
  return minutes + ' 分钟'
})

// 生命周期钩子
onMounted(async () => {
  await nextTick()
  if (markdownContainer.value) {
    enhanceMarkdownDisplay(markdownContainer.value)
  }
  
  // 添加事件监听器
  document.addEventListener('keydown', handleKeydown)
  document.addEventListener('click', handleOutsideClick)
  
  // 防止背景滚动
  document.body.style.overflow = 'hidden'
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
  const modalOverlay = document.querySelector('.fixed.inset-0.bg-black\/80')
  
  // 获取模态框内容区域
  const modalContent = document.querySelector('.glass-card.rounded-2xl')
  
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
  /* 增强markdown样式 */
  .markdown-content :deep(h1),
  .markdown-content :deep(h2),
  .markdown-content :deep(h3),
  .markdown-content :deep(h4),
  .markdown-content :deep(h5),
  .markdown-content :deep(h6) {
    color: #e2e8f0;
    margin-top: 1.5em;
    margin-bottom: 0.75em;
  }
  
  .markdown-content :deep(h1) {
    font-size: 1.8rem;
    border-bottom: 2px solid #475569;
    padding-bottom: 0.3em;
  }
  
  .markdown-content :deep(h2) {
    font-size: 1.5rem;
    border-bottom: 1px solid #475569;
    padding-bottom: 0.3em;
  }
  
  .markdown-content :deep(p) {
    margin: 1em 0;
    line-height: 1.7;
  }
  
  .markdown-content :deep(blockquote) {
    border-left: 4px solid #8b5cf6;
    padding-left: 1em;
    margin: 1em 0;
    color: #94a3b8;
    background-color: rgba(139, 92, 246, 0.1);
    padding: 1em;
    border-radius: 0 0.5rem 0.5rem 0;
  }
  
  .markdown-content :deep(ul),
  .markdown-content :deep(ol) {
    margin: 1em 0;
    padding-left: 2em;
  }
  
  .markdown-content :deep(li) {
    margin: 0.5em 0;
  }
  
  .markdown-content :deep(code) {
    background-color: #334155;
    color: #e2e8f0;
    padding: 0.2em 0.4em;
    border-radius: 0.375rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.875em;
  }
  
  .markdown-content :deep(pre) {
    background-color: #1e293b;
    padding: 1em;
    border-radius: 0.5rem;
    overflow-x: auto;
    margin: 1.5em 0;
  }
  
  .markdown-content :deep(pre code) {
    background-color: transparent;
    padding: 0;
    display: block;
    line-height: 1.5;
  }
  
  .markdown-content :deep(a) {
    color: #8b5cf6;
    text-decoration: none;
    transition: color 0.2s ease;
  }
  
  .markdown-content :deep(a:hover) {
    color: #a78bfa;
    text-decoration: underline;
  }
  
  .markdown-content :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
  }
  
  .markdown-content :deep(th) {
    background-color: #334155;
    color: #e2e8f0;
    text-align: left;
    padding: 0.75em;
    border: 1px solid #475569;
  }
  
  .markdown-content :deep(td) {
    padding: 0.75em;
    border: 1px solid #475569;
  }
  
  .markdown-content :deep(tr:nth-child(even)) {
    background-color: #0f172a;
  }
  
  .markdown-content :deep(img) {
    max-width: 100%;
    height: auto;
    border-radius: 0.375rem;
    margin: 1em 0;
  }
  
  /* 代码高亮样式 */
  .markdown-content :deep(.hljs) {
    background: #1e293b;
    color: #e2e8f0;
  }
  
  .markdown-content :deep(.hljs-comment),
  .markdown-content :deep(.hljs-quote) {
    color: #94a3b8;
    font-style: italic;
  }
  
  .markdown-content :deep(.hljs-keyword),
  .markdown-content :deep(.hljs-selector-tag),
  .markdown-content :deep(.hljs-subst) {
    color: #f472b6;
    font-weight: bold;
  }
  
  .markdown-content :deep(.hljs-number),
  .markdown-content :deep(.hljs-literal),
  .markdown-content :deep(.hljs-variable),
  .markdown-content :deep(.hljs-template-variable),
  .markdown-content :deep(.hljs-tag .hljs-attr) {
    color: #fbbf24;
  }
  
  .markdown-content :deep(.hljs-string),
  .markdown-content :deep(.hljs-doctag) {
    color: #4ade80;
  }
  
  .markdown-content :deep(.hljs-title),
  .markdown-content :deep(.hljs-section),
  .markdown-content :deep(.hljs-selector-id) {
    color: #60a5fa;
    font-weight: bold;
  }
  
  .markdown-content :deep(.hljs-subst) {
    font-weight: normal;
  }
  
  .markdown-content :deep(.hljs-type),
  .markdown-content :deep(.hljs-class .hljs-title) {
    color: #60a5fa;
    font-weight: bold;
  }
  
  .markdown-content :deep(.hljs-tag),
  .markdown-content :deep(.hljs-name),
  .markdown-content :deep(.hljs-attribute) {
    color: #93c5fd;
    font-weight: normal;
  }
  
  .markdown-content :deep(.hljs-regexp),
  .markdown-content :deep(.hljs-link) {
    color: #4ade80;
  }
  
  .markdown-content :deep(.hljs-symbol),
  .markdown-content :deep(.hljs-bullet) {
    color: #60a5fa;
  }
  
  .markdown-content :deep(.hljs-built_in),
  .markdown-content :deep(.hljs-builtin-name) {
    color: #f472b6;
  }
  
  .markdown-content :deep(.hljs-meta) {
    color: #94a3b8;
    font-weight: bold;
  }
  
  .markdown-content :deep(.hljs-deletion) {
    background: #ef4444;
    color: #ffffff;
  }
  
  .markdown-content :deep(.hljs-addition) {
    background: #10b981;
    color: #ffffff;
  }
  
  .markdown-content :deep(.hljs-emphasis) {
    font-style: italic;
  }
  
  .markdown-content :deep(.hljs-strong) {
    font-weight: bold;
  }
</style>
