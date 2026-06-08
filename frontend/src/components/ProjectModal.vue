<template>
  <transition name="modal">
    <div 
      v-if="visible" 
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm"
      @click="handleBackdropClick"
    >
      <div 
        ref="modalContent"
        class="flex max-h-[90vh] w-full max-w-4xl flex-col overflow-hidden rounded-[1.75rem] border border-cyan-100 bg-gradient-to-br from-[#f4fdff] via-white to-[#e6f7fb] shadow-[0_24px_80px_rgba(8,61,82,0.18)] animate-fadeIn"
        @click.stop
      >
        <!-- 模态框头部 -->
        <div class="flex items-start justify-between border-b border-cyan-100 bg-gradient-to-r from-cyan-50 to-white px-6 py-5">
          <div class="flex min-w-0 flex-1 items-start">
            <div class="mr-4 flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border border-cyan-200 bg-cyan-100 text-cyan-700 shadow-sm">
              <i class="fa fa-github text-xl"></i>
            </div>
            <div class="min-w-0 flex-1">
              <div class="mb-2 flex flex-wrap items-center gap-2">
                <span class="inline-flex items-center rounded-full border border-cyan-200 bg-white px-2.5 py-1 text-[11px] font-medium uppercase tracking-[0.18em] text-cyan-700">
                  Project Detail
                </span>
                <span v-if="project?.language" :class="getLanguageClass(project.language)" class="language-tag">
                  {{ project.language }}
                </span>
              </div>
              <h3 class="truncate text-2xl font-semibold text-slate-900">{{ projectName }}</h3>
              <p class="mt-1 truncate text-sm text-cyan-700/80">{{ project?.url }}</p>
            </div>
            <a
              :href="projectName ? `https://github.com/${projectName}` : '#'"
              target="_blank"
              rel="noopener noreferrer"
              class="terminal-action compact ml-4 hidden shrink-0 items-center gap-2 md:inline-flex"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              在 GitHub 查看
            </a>
          </div>
          <button 
            @click="$emit('close')" 
            class="ml-4 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-cyan-100 bg-white text-slate-400 transition-colors hover:border-cyan-200 hover:text-cyan-700"
          >
            <i class="fa fa-times text-lg"></i>
          </button>
        </div>

        <!-- 模态框内容 -->
        <div class="flex-grow overflow-y-auto">
          <div v-if="loading" class="h-full flex flex-col items-center justify-center py-12">
            <div class="mb-4 h-12 w-12 animate-spin rounded-full border-4 border-cyan-200 border-t-cyan-500"></div>
            <p class="text-slate-500">加载项目详情中...</p>
          </div>

          <div v-else-if="project" class="p-6">
            <!-- 项目描述 -->
            <div class="mb-6">
              <h4 class="mb-3 flex items-center text-lg font-semibold text-slate-900">
                <i class="fa fa-info-circle mr-2 text-cyan-600"></i>
                项目描述
              </h4>
              <p class="rounded-2xl border border-cyan-100 bg-white/90 p-4 leading-7 text-slate-600 shadow-sm">
                {{ project.description || '暂无描述' }}
              </p>
            </div>

            <!-- 技术信息 -->
            <div class="mb-6">
              <h4 class="mb-3 flex items-center text-lg font-semibold text-slate-900">
                <i class="fa fa-code mr-2 text-cyan-600"></i>
                技术信息
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="tech-info-item">
                  <span class="label">主要语言</span>
                  <span 
                    class="value language-tag"
                    :class="getLanguageClass(project.language)"
                  >
                    {{ project.language || '未知' }}
                  </span>
                </div>
                <div class="tech-info-item">
                  <span class="label">创建时间</span>
                  <span class="value">{{ formatFullDate(project.created_at) }}</span>
                </div>
                <div class="tech-info-item">
                  <span class="label">最后更新</span>
                  <span class="value">{{ formatFullDate(project.updated_at) }}</span>
                </div>
                <div class="tech-info-item">
                  <span class="label">开放问题</span>
                  <span class="value">{{ formatNumber(project.open_issues) }}</span>
                </div>
              </div>
            </div>

            <!-- 统计数据 -->
            <div class="mb-6">
              <h4 class="mb-3 flex items-center text-lg font-semibold text-slate-900">
                <i class="fa fa-bar-chart mr-2 text-cyan-600"></i>
                项目统计
              </h4>
              <div class="grid grid-cols-2 gap-4 md:grid-cols-4">
                <div class="stat-card">
                  <div class="stat-icon bg-amber-100 text-amber-600">
                    <i class="fa fa-star"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ formatNumber(project.stars) }}</div>
                    <div class="stat-label">Stars</div>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon bg-emerald-100 text-emerald-600">
                    <i class="fa fa-users"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ formatNumber(project.contributor_count) }}</div>
                    <div class="stat-label">贡献者</div>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon bg-violet-100 text-violet-600">
                    <i class="fa fa-eye"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ formatNumber(project.watchers) }}</div>
                    <div class="stat-label">关注者</div>
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-icon bg-cyan-100 text-cyan-600">
                    <i class="fa fa-code-fork"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ formatNumber(project.forks) }}</div>
                    <div class="stat-label">Forks</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="h-full flex flex-col items-center justify-center py-12">
            <i class="fa fa-exclamation-triangle text-red-400 text-4xl mb-4"></i>
            <p class="text-slate-500">加载项目详情失败</p>
          </div>

          <!-- AI 分析报告 -->
          <div v-if="project?.analysis" class="border-t border-cyan-100 px-6 py-6 bg-gradient-to-b from-cyan-50/35 to-transparent">
            <h4 class="mb-4 flex items-center gap-2 text-lg font-semibold text-slate-900">
              <span class="inline-flex items-center rounded-full border border-cyan-200 bg-cyan-50 px-2 py-0.5 text-xs font-medium text-cyan-700">AI</span>
              分析报告
            </h4>
            <div class="rounded-2xl border border-cyan-100 bg-white/92 p-5 shadow-sm">
              <div
                class="markdown-content max-h-[45vh] overflow-y-auto pr-1 text-sm"
                v-html="renderedAnalysis"
              ></div>
            </div>
          </div>
        </div>

        <!-- 模态框底部 -->
        <div class="flex items-center justify-between border-t border-cyan-100 bg-white/70 px-6 py-5">
          <div class="text-sm text-cyan-700/80">
            分析时间：{{ project?.summary_date ? formatFullDate(project.summary_date) : '未知' }}
          </div>
          <div class="flex space-x-3">
            <a 
              v-if="project?.url" 
              :href="project.url"
              target="_blank"
              rel="noopener noreferrer"
              class="terminal-action primary flex items-center"
            >
              <i class="fa fa-external-link mr-2"></i>
              访问项目
            </a>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { Project } from '@/api/reports'
import { getProjectDetails } from '@/api/reports'
import { renderMarkdown } from '../utils/markdown-simple'

interface Props {
  visible: boolean
  projectName?: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
}>()

const modalContent = ref<HTMLElement>()
const loading = ref(false)
const project = ref<Project | null>(null)

const renderedAnalysis = ref('')

function enforceExternalLinksNewTab(html: string): string {
  return html.replace(/<a\s+/g, '<a target="_blank" rel="noopener noreferrer" ')
}

watch(
  () => project.value?.analysis,
  async (analysis) => {
    if (!analysis) { renderedAnalysis.value = ''; return }
    // Strip the repeated header line (### ✨ name) — already shown in modal header
    const cleaned = analysis.replace(/^###\s*✨[^\n]*\n/, '').trim()
    renderedAnalysis.value = enforceExternalLinksNewTab(await renderMarkdown(cleaned))
  },
  { immediate: true }
)

watch(() => props.visible, async (visible) => {
  if (visible && props.projectName) {
    await loadProjectDetails()
  }
})

const loadProjectDetails = async () => {
  if (!props.projectName) return
  
  loading.value = true
  try {
    // 修改为使用查询参数，而不是路径参数，以更好地处理包含特殊字符的项目名称
    project.value = await getProjectDetails(props.projectName)
  } catch (error) {
    console.error('Failed to load project details:', error)
    project.value = null
  } finally {
    loading.value = false
  }
}

const handleBackdropClick = (event: MouseEvent) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

const formatNumber = (num: number | string): string => {
  if (typeof num === 'string') return num
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}

const formatFullDate = (dateStr: string): string => {
  if (!dateStr || dateStr === 'N/A') return '未知'
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch {
    return '未知'
  }
}

const getLanguageClass = (language: string): string => {
  const languageColors: Record<string, string> = {
    'JavaScript': 'bg-amber-50 text-amber-700 border border-amber-200',
    'TypeScript': 'bg-blue-50 text-blue-700 border border-blue-200',
    'Python': 'bg-emerald-50 text-emerald-700 border border-emerald-200',
    'Java': 'bg-orange-50 text-orange-700 border border-orange-200',
    'Go': 'bg-cyan-50 text-cyan-700 border border-cyan-200',
    'Rust': 'bg-rose-50 text-rose-700 border border-rose-200',
    'C++': 'bg-violet-50 text-violet-700 border border-violet-200',
    'C': 'bg-slate-100 text-slate-700 border border-slate-200',
    'PHP': 'bg-indigo-50 text-indigo-700 border border-indigo-200',
    'Ruby': 'bg-red-50 text-red-700 border border-red-200',
    'Swift': 'bg-orange-50 text-orange-700 border border-orange-200',
    'Kotlin': 'bg-purple-50 text-purple-700 border border-purple-200'
  }
  
  return languageColors[language] || 'bg-slate-100 text-slate-700 border border-slate-200'
}
</script>

<style scoped>
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.tech-info-item {
  @apply flex items-center justify-between rounded-2xl border border-cyan-100 bg-white/90 p-4 shadow-sm;
}

.tech-info-item .label {
  @apply text-sm text-slate-500;
}

.tech-info-item .value {
  @apply font-medium text-slate-900;
}

.language-tag {
  @apply px-2 py-1 rounded-full text-xs font-medium;
}

.stat-card {
  @apply flex items-center space-x-3 rounded-2xl border border-cyan-100 bg-white/90 p-4 shadow-sm transition-colors hover:border-cyan-200;
}

.stat-icon {
  @apply flex h-10 w-10 items-center justify-center rounded-xl;
}

.stat-content {
  @apply flex-1;
}

.stat-value {
  @apply text-lg font-bold text-slate-900;
}

.stat-label {
  @apply text-xs text-slate-500;
}
</style>
