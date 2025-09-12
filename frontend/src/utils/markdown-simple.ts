import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'

// 导出类型定义，避免直接引用未初始化的模块
import type MarkdownIt from 'markdown-it'

type PluginType = any

// 创建一个异步函数来初始化markdown-it和所有插件
let markdownInstance: MarkdownIt | null = null

/**
 * 初始化并获取MarkdownIt实例
 * @returns Promise<MarkdownIt>
 */
async function getInitializedMarkdownInstance(): Promise<MarkdownIt> {
  if (markdownInstance) {
    return markdownInstance
  }

  try {
    // 使用动态导入加载所有模块
    const [
      { default: MarkdownIt },
      { default: emojiPlugin },
      { default: taskListsPlugin },
      { default: anchorPlugin },
      { default: tocDoneRightPlugin },
      { default: footnotePlugin },
      { default: markPlugin },
      { default: subPlugin },
      { default: supPlugin },
      { default: insPlugin }
    ] = await Promise.all([
      import('markdown-it'),
      import('markdown-it-emoji'),
      import('markdown-it-task-lists'),
      import('markdown-it-anchor'),
      import('markdown-it-toc-done-right'),
      import('markdown-it-footnote'),
      import('markdown-it-mark'),
      import('markdown-it-sub'),
      import('markdown-it-sup'),
      import('markdown-it-ins')
    ])

    // 初始化MarkdownIt实例
    const md = new MarkdownIt({
      html: true,           // 启用HTML标签
      xhtmlOut: false,      // 使用 '/' 闭合单标签
      breaks: true,         // 转换段落里的\n到<br>
      langPrefix: 'language-', // 代码块的CSS类前缀
      linkify: true,        // 自动识别链接
      typographer: true,    // 启用一些语言替换和排版
      highlight: function(str, lang) {
        if (lang && hljs.getLanguage(lang)) {
          try {
            return hljs.highlight(str, { language: lang }).value
          } catch (__) {
            // 忽略高亮错误
          }
        }
        
        try {
          return hljs.highlightAuto(str).value
        } catch (__) {
          // 忽略自动高亮错误
        }
        
        return '' // 使用默认转义
      }
    })

    // 注册插件
    md.use(emojiPlugin)
    md.use(taskListsPlugin, {
      enabled: true,
      label: true,
      labelAfter: true
    })
    md.use(anchorPlugin, {
      permalink: true,
      permalinkClass: 'header-anchor',
      permalinkSymbol: '🔗',
      permalinkBefore: false
    })
    md.use(tocDoneRightPlugin, {
      level: [1, 2, 3],
      title: '## 目录',
      tocClassName: 'markdown-toc',
      containerClassName: 'toc-container'
    })
    md.use(footnotePlugin)
    md.use(markPlugin)
    md.use(subPlugin)
    md.use(supPlugin)
    md.use(insPlugin)

    markdownInstance = md
    return md
  } catch (error) {
    console.error('Failed to initialize markdown-it:', error)
    // 创建一个简化版的markdown-it实例作为备用
    const MarkdownIt = (await import('markdown-it')).default
    const md = new MarkdownIt({
      html: true,
      breaks: true,
      linkify: true,
      typographer: true
    })
    markdownInstance = md
    return md
  }
}

/**
 * 预处理Markdown内容
 * @param content 原始Markdown内容
 * @returns 预处理后的Markdown内容
 */
function preprocessMarkdown(content: string): string {
  if (!content) return ''
  
  // 清理内容
  let processedContent = content.trim()
  
  // 移除可能存在的Markdown代码块标记
  if (processedContent.startsWith('```markdown')) {
    processedContent = processedContent.slice(11).trim()
  }
  if (processedContent.startsWith('```')) {
    processedContent = processedContent.slice(3).trim()
  }
  if (processedContent.endsWith('```')) {
    processedContent = processedContent.slice(0, -3).trim()
  }
  
  // 确保有正确的换行
  processedContent = processedContent.replace(/\r\n/g, '\n')
  
  return processedContent
}

/**
 * 渲染Markdown内容为HTML
 * @param content Markdown内容
 * @returns Promise<string> 渲染后的HTML
 */
export async function renderMarkdown(content: string): Promise<string> {
  if (!content) return ''
  
  // 预处理Markdown内容
  const processedContent = preprocessMarkdown(content)
  
  try {
    // 渲染Markdown为HTML
    const md = await getInitializedMarkdownInstance()
    return md.render(processedContent)
  } catch (error) {
    console.error('Markdown渲染错误:', error)
    // 渲染失败时返回原始内容的格式化版本
    return `<pre class="whitespace-pre-wrap text-slate-300 bg-slate-800/50 p-4 rounded-lg">${content}</pre>`
  }
}

/**
 * 获取MarkdownIt实例
 * @returns Promise<MarkdownIt> MarkdownIt实例
 */
export async function getMarkdownInstance(): Promise<MarkdownIt> {
  return getInitializedMarkdownInstance()
}

/**
 * 增强Markdown显示效果
 * @param container 包含Markdown内容的DOM元素
 */
export function enhanceMarkdownDisplay(container: HTMLElement): void {
  if (!container) return
  
  try {
    // 为代码块添加复制功能
    const codeBlocks = container.querySelectorAll('pre code')
    codeBlocks.forEach((codeBlock) => {
      // 检查父元素pre
      const preElement = codeBlock.parentElement
      if (preElement && preElement.tagName === 'PRE') {
        // 创建复制按钮
        const copyButton = document.createElement('button')
        copyButton.className = 'copy-code-button absolute top-2 right-2 p-2 bg-slate-800/80 hover:bg-slate-700/80 text-white rounded-md text-xs transition-all'
        copyButton.title = '复制代码'
        copyButton.innerHTML = '📋'
        
        // 设置pre元素为相对定位
        preElement.style.position = 'relative'
        
        // 添加复制事件
        copyButton.addEventListener('click', async () => {
          try {
            await navigator.clipboard.writeText(codeBlock.textContent || '')
            copyButton.innerHTML = '✅'
            setTimeout(() => {
              copyButton.innerHTML = '📋'
            }, 2000)
          } catch (error) {
            console.error('复制代码失败:', error)
            copyButton.innerHTML = '❌'
            setTimeout(() => {
              copyButton.innerHTML = '📋'
            }, 2000)
          }
        })
        
        // 添加按钮到pre元素
        preElement.appendChild(copyButton)
      }
    })
    
    // 为链接添加target="_blank"属性
    const links = container.querySelectorAll('a:not([target])')
    links.forEach((link) => {
      const href = link.getAttribute('href')
      if (href && !href.startsWith('#')) {
        link.setAttribute('target', '_blank')
        link.setAttribute('rel', 'noopener noreferrer')
      }
    })
    
    // 增强表格样式
    const tables = container.querySelectorAll('table')
    tables.forEach((table) => {
      table.classList.add('w-full', 'border-collapse')
      // 添加响应式表格容器
      const wrapper = document.createElement('div')
      wrapper.className = 'overflow-x-auto my-4'
      table.parentNode?.insertBefore(wrapper, table)
      wrapper.appendChild(table)
    })
    
    // 为图片添加懒加载
    const images = container.querySelectorAll('img:not([loading])')
    images.forEach((img) => {
      img.setAttribute('loading', 'lazy')
    })
    
  } catch (error) {
    console.error('增强Markdown显示效果失败:', error)
  }
}
