// markdown-it插件的类型声明

// markdown-it-mark 插件类型声明
declare module 'markdown-it-mark' {
  import MarkdownIt from 'markdown-it';
  function markdownItMark(md: MarkdownIt): void;
  export = markdownItMark;
}

// markdown-it-sub 插件类型声明
declare module 'markdown-it-sub' {
  import MarkdownIt from 'markdown-it';
  function markdownItSub(md: MarkdownIt): void;
  export = markdownItSub;
}

// markdown-it-sup 插件类型声明
declare module 'markdown-it-sup' {
  import MarkdownIt from 'markdown-it';
  function markdownItSup(md: MarkdownIt): void;
  export = markdownItSup;
}

// markdown-it-ins 插件类型声明
declare module 'markdown-it-ins' {
  import MarkdownIt from 'markdown-it';
  function markdownItIns(md: MarkdownIt): void;
  export = markdownItIns;
}

// markdown-it-mermaid 插件类型声明
declare module 'markdown-it-mermaid';