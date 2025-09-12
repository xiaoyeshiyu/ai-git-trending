// Markdown-it插件类型声明
// markdown-it-emoji 插件类型声明
declare module 'markdown-it-emoji' {
  import MarkdownIt from 'markdown-it';
  function markdownItEmoji(md: MarkdownIt, options?: any): void;
  export = markdownItEmoji;
}

// markdown-it-task-lists 插件类型声明
declare module 'markdown-it-task-lists' {
  import MarkdownIt from 'markdown-it';
  function markdownItTaskLists(md: MarkdownIt, options?: any): void;
  export = markdownItTaskLists;
}

// markdown-it-anchor 插件类型声明
declare module 'markdown-it-anchor' {
  import MarkdownIt from 'markdown-it';
  
  interface MarkdownItAnchorOptions {
    level?: number[];
    permalink?: boolean | string;
    permalinkClass?: string;
    permalinkSymbol?: string;
    permalinkBefore?: boolean;
    slugify?: (s: string) => string;
    uniqueSlugStartIndex?: number;
    callback?: (tokens: any[], idx: number, title: string, slug: string) => void;
  }
  
  function markdownItAnchor(md: MarkdownIt, options?: MarkdownItAnchorOptions): void;
  export = markdownItAnchor;
}

// markdown-it-toc-done-right 插件类型声明
declare module 'markdown-it-toc-done-right' {
  import MarkdownIt from 'markdown-it';
  
  interface MarkdownItTocDoneRightOptions {
    level?: number[];
    title?: string;
    slugify?: (s: string) => string;
    tocClassName?: string;
    containerClassName?: string;
    listType?: 'ul' | 'ol';
  }
  
  function markdownItTocDoneRight(md: MarkdownIt, options?: MarkdownItTocDoneRightOptions): void;
  export = markdownItTocDoneRight;
}

// markdown-it-footnote 插件类型声明
declare module 'markdown-it-footnote' {
  import MarkdownIt from 'markdown-it';
  function markdownItFootnote(md: MarkdownIt): void;
  export = markdownItFootnote;
}

// markdown-it-table 插件类型声明
declare module 'markdown-it-table' {
  import MarkdownIt from 'markdown-it';
  function markdownItTable(md: MarkdownIt): void;
  export = markdownItTable;
}