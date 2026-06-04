import axios, { AxiosError } from 'axios'

// 根据环境变量或开发/生产环境自动选择API地址
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'
const STATIC_BASE = import.meta.env.BASE_URL || '/'

// 静态模式：通过 VITE_STATIC_MODE 环境变量控制，GitHub Pages 构建时设为 true
const isStaticMode = import.meta.env.VITE_STATIC_MODE === 'true'

// 创建axios实例并配置
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: isStaticMode ? 3000 : 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 静态 JSON 数据回退 — GitHub Pages 没有后端
async function fetchStatic<T>(path: string): Promise<T> {
  const url = `${STATIC_BASE}data/${path}`
  const resp = await fetch(url)
  if (!resp.ok) throw new Error(`Static data not found: ${path}`)
  return resp.json()
}

function isApiUnreachable(err: unknown): boolean {
  if (err instanceof Error) {
    const msg = err.message
    return msg.includes('无法连接到服务器')
      || msg.includes('NetworkError')
      || msg.includes('Failed to fetch')
      || msg.includes('ECONNREFUSED')
      || msg.includes('ERR_CONNECTION_REFUSED')
      || msg.includes('timeout')
  }
  return false
}

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.config.url} - ${response.status}`)
    return response
  },
  (error: AxiosError) => {
    console.error(`❌ API Error: ${error.config?.url}`, error.message)
    
    // 统一错误处理
    if (error.code === 'ECONNREFUSED') {
      throw new Error('无法连接到服务器，请检查后端服务是否启动')
    }
    if (error.response?.status === 404) {
      throw new Error('请求的资源不存在')
    }
    if (error.response?.status === 500) {
      throw new Error('服务器内部错误，请稍后重试')
    }
    if (error.code === 'ECONNABORTED') {
      throw new Error('请求超时，请检查网络连接')
    }
    
    throw new Error(error.message || '请求失败')
  }
)

export interface Report {
  date: string
  project_count: number
  content?: string  // 可选，用于详情页
}

export interface ReportContent {
  mdContent: string
}

export interface Project {
  name: string
  url: string
  description: string
  language: string
  stars: number
  forks: number
  contributor_count: number
  created_at: string
  updated_at: string
  open_issues: number
  watchers: number
  summary_date?: string
  analysis?: string
}

export interface Stats {
  totalReports: number
  totalProjects: number
  topLanguage: string
  weeklyNew: number
  totalForks: string
  avgContributors: number
  activityScore: number
  activityBreakdown?: {
    recentlyActive: number
    stable: number
    needsAttention: number
  }
}

export interface LanguageData {
  name: string
  count: number
  percentage: number
  colorClass: string
}

export interface TrendDataItem {
  label: string
  value: number
  change: number
  colorClass: string
}

export interface TrendsData {
  time_window_days: number
  most_frequent_projects: {
    name: string
    url: string
    description: string
    language: string
    count: number
    avg_stars: number
    stars?: number
    forks?: number
    contributor_count?: number
    created_at?: string
    updated_at?: string
    open_issues?: number
    watchers?: number
  }[]
  most_frequent_languages: [string, number][]
  programmingLanguages: [string, number][]
  surgingProjects: {
    name: string
    url: string
    description: string
    language: string
    star_increase: number
    start_stars: number
    end_stars: number
  }[]
  techDomains: { name: string; count: number; percentage: number }[]
}

export interface Developer {
  username: string
  display_name: string
  type: string
  bio: string
  followers: number
  public_repos: number
  created_at: string
  avatar_url: string
  profile_url: string
  trending_repo: string | null
  trending_repo_url: string | null
  top_repos: { name: string; stars: number; language: string }[]
  main_languages: string[]
}

export interface TrendingData {
  repositories: Project[]
  developers: Developer[]
  updated_at: string
}

async function staticGetProjects(params: {
  date_from?: string
  date_to?: string
  language?: string
  sort_by?: string
  order?: string
  page?: number
  page_size?: number
  search?: string
}): Promise<{ items: Project[]; total: number; page: number; page_size: number; total_pages: number }> {
  let all: Project[] = await fetchStatic<Project[]>('projects.json')

  if (params.language) {
    all = all.filter(p => p.language?.toLowerCase() === params.language!.toLowerCase())
  }
  if (params.search) {
    const q = params.search.toLowerCase()
    all = all.filter(p => p.name.toLowerCase().includes(q) || p.description?.toLowerCase().includes(q))
  }

  const sortBy = params.sort_by || 'stars'
  const order = params.order || 'desc'
  all.sort((a, b) => {
    const aVal = (a as any)[sortBy] ?? 0
    const bVal = (b as any)[sortBy] ?? 0
    if (typeof aVal === 'string') return order === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal)
    return order === 'asc' ? (aVal as number) - (bVal as number) : (bVal as number) - (aVal as number)
  })

  const page = params.page || 1
  const pageSize = params.page_size || 20
  const total = all.length
  const totalPages = Math.ceil(total / pageSize)
  const start = (page - 1) * pageSize
  const items = all.slice(start, start + pageSize)

  return { items, total, page, page_size: pageSize, total_pages: totalPages }
}

// 统一提取响应数据 — 兼容有 envelope 和 raw 两种格式
function unwrapResponse<T>(responseData: any): T {
  if (responseData === null || responseData === undefined) return [] as any
  // { success: true, data: [...] }
  if (responseData.success !== undefined && responseData.data !== undefined) {
    return responseData.data as T
  }
  // { data: { items: [...] } }
  if (responseData.data?.items !== undefined) {
    return responseData.data.items as T
  }
  // { data: [...] }
  if (Array.isArray(responseData.data)) {
    return responseData.data as T
  }
  // raw array or object
  return responseData as T
}

export const reportApi = {
  // 获取报告列表
  async getReports(): Promise<Report[]> {
    if (isStaticMode) {
      return fetchStatic<Report[]>('reports.json')
    }
    try {
      const response = await api.get('/api/reports')
      const reports = unwrapResponse<Report[]>(response.data)
      console.log(`📋 获取到 ${reports.length} 个报告`)
      return reports
    } catch (error) {
      if (isApiUnreachable(error)) {
        console.warn('API 不可用，回退到静态数据')
        return fetchStatic<Report[]>('reports.json')
      }
      console.error('获取报告列表失败:', error)
      throw error
    }
  },

  // 获取具体报告内容
  async getReportContent(date: string): Promise<Report> {
    if (isStaticMode) {
      return fetchStatic<Report>(`reports/${date}.json`)
    }
    try {
      const response = await api.get(`/api/report/${date}`)
      console.log(`📄 获取报告内容: ${date}`)
      return unwrapResponse(response.data)
    } catch (error) {
      if (isApiUnreachable(error)) {
        console.warn('API 不可用，回退到静态数据')
        return fetchStatic<Report>(`reports/${date}.json`)
      }
      console.error(`获取报告内容失败 (${date}):`, error)
      throw error
    }
  },

  // 获取指定日期的项目列表
  async getProjectsByDate(date: string): Promise<Project[]> {
    if (isStaticMode) {
      const all: Project[] = await fetchStatic<Project[]>('projects.json')
      return all.filter(p => p.summary_date === date)
    }
    try {
      const response = await api.get(`/api/projects/${date}`)
      const projects = response.data.data || []
      console.log(`🚀 获取到 ${projects.length} 个项目 (${date})`)
      return projects
    } catch (error) {
      if (isApiUnreachable(error)) {
        console.warn('API 不可用，回退到静态数据')
        const all: Project[] = await fetchStatic<Project[]>('projects.json')
        return all.filter(p => p.summary_date === date)
      }
      console.error(`获取项目列表失败 (${date}):`, error)
      throw error
    }
  },

  // 获取项目列表（支持日期范围、排序、筛选）
  async getProjects(params: {
    date_from?: string
    date_to?: string
    language?: string
    sort_by?: string
    order?: string
    page?: number
    page_size?: number
    search?: string
  }): Promise<{ items: Project[]; total: number; page: number; page_size: number; total_pages: number }> {
    if (isStaticMode) {
      return staticGetProjects(params)
    }
    try {
      const response = await api.get('/api/projects', { params })
      console.log(`🚀 获取项目列表:`, params)
      return unwrapResponse(response.data)
    } catch (error) {
      if (isApiUnreachable(error)) {
        console.warn('API 不可用，回退到静态数据（客户端筛选）')
        return staticGetProjects(params)
      }
      console.error('获取项目列表失败:', error)
      throw error
    }
  },

  // 获取单个项目详情
  async getProjectDetails(projectName: string): Promise<Project> {
    if (isStaticMode) {
      const all: Project[] = await fetchStatic<Project[]>('projects.json')
      const found = all.find(p => p.name === projectName)
      if (found) return found
      throw new Error(`项目 ${projectName} 未找到`)
    }
    try {
      const response = await api.get('/api/project', {
        params: { project_name: projectName }
      })
      console.log(`📦 获取项目详情: ${projectName}`)
      return unwrapResponse(response.data)
    } catch (error) {
      if (isApiUnreachable(error)) {
        console.warn('API 不可用，回退到静态数据')
        const all: Project[] = await fetchStatic<Project[]>('projects.json')
        const found = all.find(p => p.name === projectName)
        if (found) return found
        throw new Error(`项目 ${projectName} 未找到`)
      }
      console.error(`获取项目详情失败 (${projectName}):`, error)
      throw error
    }
  },

  // 获取统计数据
  async getStats(): Promise<Stats> {
    if (isStaticMode) {
      return fetchStatic<Stats>('stats.json')
    }
    try {
      const response = await api.get('/api/stats')
      console.log('📊 获取统计数据成功')
      return unwrapResponse(response.data)
    } catch (error) {
      if (isApiUnreachable(error)) {
        console.warn('API 不可用，回退到静态数据')
        return fetchStatic<Stats>('stats.json')
      }
      console.error('获取统计数据失败:', error)
      throw error
    }
  },

  // 获取趋势数据（静态模式下从预生成 JSON 读取）
  async getTrends(params?: { days?: number }): Promise<TrendsData> {
    if (isStaticMode) {
      try {
        const trends = await fetchStatic<any>('trends.json')
        const key = (params?.days || 7) <= 7 ? 'daily' : 'monthly'
        return trends[key] || trends.daily || trends
      } catch {
        return { time_window_days: params?.days || 7, most_frequent_projects: [], most_frequent_languages: [], programmingLanguages: [], surgingProjects: [], techDomains: [] }
      }
    }
    try {
      const response = await api.get('/api/trends', { params })
      console.log(`📈 获取趋势数据成功 (时间范围: ${params?.days || 7}天)`)
      return unwrapResponse(response.data)
    } catch (error) {
      console.error('获取趋势数据失败:', error)
      throw error
    }
  },

  // 获取所有技术领域分类
  async getTechDomains(): Promise<{ name: string; count: number }[]> {
    if (isStaticMode) return []
    try {
      const response = await api.get('/api/tech-domains')
      return response.data.data || []
    } catch (error) {
      console.error('获取技术领域失败:', error)
      return []
    }
  },

  // 获取编程语言分布
  async getLanguageDistribution(): Promise<{ name: string; count: number }[]> {
    if (isStaticMode) return []
    try {
      const response = await api.get('/api/language-distribution')
      return response.data.data || []
    } catch (error) {
      console.error('获取语言分布失败:', error)
      return []
    }
  },

  // 获取项目趋势
  async getProjectTrend(days: number = 7): Promise<{ date: string; count: number }[]> {
    if (isStaticMode) return []
    try {
      const response = await api.get('/api/project-trend', { params: { days } })
      return response.data.data || []
    } catch (error) {
      console.error('获取项目趋势失败:', error)
      return []
    }
  },

  // 获取实时 Trending 数据（仓库 + 开发者）—— 需要后端实时抓取
  async getTrending(): Promise<TrendingData> {
    if (isStaticMode) {
      return { repositories: [], developers: [], updated_at: new Date().toISOString() }
    }
    try {
      const response = await api.get('/api/trending')
      return response.data
    } catch (error) {
      console.error('获取 Trending 数据失败:', error)
      throw error
    }
  },

  // 健康检查
  async healthCheck(): Promise<boolean> {
    try {
      await api.get('/api/stats')
      return true
    } catch {
      return false
    }
  },

  // 获取语言分布数据（从 trends API 获取）
  async getLanguageDistribution(): Promise<LanguageData[]> {
    if (isStaticMode) return []
    try {
      const response = await api.get('/api/trends')
      console.log('🌐 获取语言分布数据成功', response.data)
      const langData = response.data.data?.programmingLanguages || response.data.data?.most_frequent_languages || []
      const colorClasses = ['bg-blue-500', 'bg-green-500', 'bg-yellow-500', 'bg-purple-500', 'bg-red-500', 'bg-cyan-500', 'bg-pink-500']
      return langData.map((item: [string, number], index: number) => ({
        name: item[0],
        count: item[1],
        percentage: Math.round((item[1] / langData.reduce((sum: number, i: [string, number]) => sum + i[1], 0)) * 100),
        colorClass: colorClasses[index % colorClasses.length]
      }))
    } catch (error) {
      console.error('获取语言分布数据失败:', error)
      throw error
    }
  },

  // 获取趋势数据
  async getTrendData(): Promise<TrendDataItem[]> {
    if (isStaticMode) {
      try {
        const trends = await fetchStatic<any>('trends.json')
        const data = trends.daily || trends
        const domains = data.techDomains || []
        return domains.map((domain: any, index: number) => ({
          label: domain.name,
          value: domain.count,
          change: domain.percentage || 0,
          colorClass: ['text-green-400', 'text-blue-400', 'text-purple-400', 'text-pink-400', 'text-yellow-400'][index % 5]
        }))
      } catch { return [] }
    }
    try {
      const response = await api.get('/api/trends')
      console.log('📈 获取趋势数据成功', response.data)
      const data = response.data.data
      const techDomains = data?.techDomains || []
      return techDomains.map((domain: any, index: number) => ({
        label: domain.name,
        value: domain.count,
        change: domain.percentage,
        colorClass: ['text-green-400', 'text-blue-400', 'text-purple-400', 'text-pink-400', 'text-yellow-400'][index % 5]
      }))
    } catch (error) {
      console.error('获取趋势数据失败:', error)
      throw error
    }
  }
}

// 导出便利函数
export const getReports = reportApi.getReports
export const getProjectsByDate = reportApi.getProjectsByDate
export const getProjects = reportApi.getProjects
export const getProjectDetails = reportApi.getProjectDetails
export const getReportByDate = reportApi.getReportContent
export const getStats = reportApi.getStats
export const getTrends = reportApi.getTrends
export const getTrending = reportApi.getTrending
export const healthCheck = reportApi.healthCheck
export const getTrendData = reportApi.getTrendData
export const getTechDomains = reportApi.getTechDomains
export const getLanguageDistribution = reportApi.getLanguageDistribution
export const getProjectTrend = reportApi.getProjectTrend

// 导出API基础URL用于调试
export const getApiBaseUrl = () => API_BASE_URL

export default api