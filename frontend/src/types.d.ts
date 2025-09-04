// markdown-it插件的类型声明

declare module 'markdown-it-mark' {
  import MarkdownIt = require('markdown-it');
  function plugin(md: MarkdownIt): void;
  export = plugin;
}

declare module 'markdown-it-sub' {
  import MarkdownIt = require('markdown-it');
  function plugin(md: MarkdownIt): void;
  export = plugin;
}

declare module 'markdown-it-sup' {
  import MarkdownIt = require('markdown-it');
  function plugin(md: MarkdownIt): void;
  export = plugin;
}

declare module 'markdown-it-ins' {
  import MarkdownIt = require('markdown-it');
  function plugin(md: MarkdownIt): void;
  export = plugin;
}