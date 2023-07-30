import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';
import 'dayjs/locale/zh-cn'
import locale from 'element-plus/lib/locale/lang/zh-cn'

// 引入echarts
import echarts from 'echarts'
require('echarts-wordcloud')
// 全局注册
// main.js
import VueMarkdownEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
// 引入你所使用的主题 此处以 github 主题为例
import githubTheme from '@kangc/v-md-editor/lib/theme/github';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import '@/assets/css/global.css'
import duoImageViewer from 'duo-image-viewer'


import Prism from 'prismjs';
// highlightjs
import hljs from 'highlight.js';

import $ from 'jquery';
window.jQuery = $;
window.$ = $;

VMdPreview.use(githubTheme, {
    Hljs: hljs,
});

VueMarkdownEditor.use(vuepressTheme, {
    Prism,
});

// 链式编程，使用ElementPlus、VueMarkdownEditor等插件，并创建App
createApp(App).use(store).use(router).use(duoImageViewer).use(ElementPlus, { locale, size: "small"}).use(VueMarkdownEditor).use(VMdPreview).mount('#app');
