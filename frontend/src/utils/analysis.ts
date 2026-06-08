export interface ParsedAnalysis {
  summary: string
  detailMarkdown: string
}

export interface AnalysisDetail {
  title: string
  text: string
}

const SECTION_TITLES = '它是什么|能解决什么痛点|适合谁用|怎么上手|可以用在哪些场景|技术看点|近期动向与发展方向|同类对比|注意事项'

export function cleanAnalysisMarkdown(content: string): string {
  return content
    .replace(/^###\s*✨[^\n]*\n/, '')
    .replace(/^\s*>?\s*(?:\*\*)?一句话(?:点评|总结)?(?:\*\*)?[:：]?\s*/m, '')
    .trim()
}

export function isAnalysisSectionHeading(line: string): boolean {
  return new RegExp(`^\\s*(?:[-*]\\s+)?(?:\\*\\*)?(?:${SECTION_TITLES})(?:\\*\\*)?[:：]`).test(line)
}

function normalizeAnalysisText(content: string): string {
  return cleanAnalysisMarkdown(content)
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/\*\*/g, '')
    .replace(/`/g, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/^\s*[-*]\s+/gm, '')
    .replace(/\n{2,}/g, '\n')
    .trim()
}

export function extractAnalysisPreview(content: string, maxLength: number = 180): string {
  const cleaned = cleanAnalysisMarkdown(content)
  if (!cleaned) return ''

  const lines = cleaned.split('\n')
  const firstSectionIndex = lines.findIndex((line) => isAnalysisSectionHeading(line))
  const summaryMarkdown = firstSectionIndex === -1 ? cleaned : lines.slice(0, firstSectionIndex).join('\n').trim()
  const normalized = normalizeAnalysisText(summaryMarkdown || cleaned)

  if (!normalized) return ''

  const summaryLines = normalized
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
    .filter((line) => !/^github\s*:/i.test(line))

  return summaryLines.join(' ').slice(0, maxLength).trim()
}

export function splitAnalysisContent(content: string): ParsedAnalysis {
  const cleaned = cleanAnalysisMarkdown(content)
  if (!cleaned) {
    return { summary: '', detailMarkdown: '' }
  }

  const lines = cleaned.split('\n')
  const firstSectionIndex = lines.findIndex((line) => isAnalysisSectionHeading(line))

  if (firstSectionIndex === -1) {
    return {
      summary: extractAnalysisPreview(cleaned),
      detailMarkdown: cleaned
    }
  }

  return {
    summary: extractAnalysisPreview(lines.slice(0, firstSectionIndex).join('\n').trim() || cleaned),
    detailMarkdown: lines.slice(firstSectionIndex).join('\n').trim()
  }
}

export function extractAnalysisDetails(content: string, limit: number = 2): AnalysisDetail[] {
  const cleaned = cleanAnalysisMarkdown(content)
  if (!cleaned) return []

  const lines = cleaned.split('\n')
  const details: AnalysisDetail[] = []
  let current: AnalysisDetail | null = null

  for (const rawLine of lines) {
    const line = rawLine.trim()
    if (!line || /^- \*\*GitHub\*\*/.test(line)) {
      continue
    }

    const matched = line.match(new RegExp(`^- \\*\\*(${SECTION_TITLES})\\*\\*[：:]\\s*(.*)$`))
    if (matched) {
      if (current) {
        details.push(current)
      }
      current = {
        title: matched[1],
        text: matched[2].trim()
      }
      continue
    }

    if (current) {
      current.text = `${current.text} ${line.replace(/^[-*]\s+/, '')}`.trim()
    }
  }

  if (current) {
    details.push(current)
  }

  return details
    .map((item) => ({
      title: item.title,
      text: item.text
        .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
        .replace(/`/g, '')
        .replace(/\*\*/g, '')
        .trim()
    }))
    .filter((item) => item.text)
    .slice(0, limit)
}
