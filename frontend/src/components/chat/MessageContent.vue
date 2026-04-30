<script setup lang="ts">
import { computed, watch, nextTick, ref } from 'vue'
import { Marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

const props = defineProps<{
  content: string
  isStreaming?: boolean
}>()

const containerRef = ref<HTMLDivElement>()

const marked = new Marked(
  markedHighlight({
    langPrefix: 'hljs language-',
    highlight(code: string, lang: string) {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value
      }
      return hljs.highlightAuto(code).value
    },
  }),
)

marked.setOptions({ breaks: true, gfm: true })

const html = computed(() => {
  try {
    return marked.parse(props.content) as string
  } catch {
    return props.content
  }
})

watch(html, async () => {
  await nextTick()
  if (containerRef.value) {
    const links = containerRef.value.querySelectorAll('a')
    links.forEach((link) => {
      link.setAttribute('target', '_blank')
      link.setAttribute('rel', 'noopener noreferrer')
    })
  }
})
</script>

<template>
  <div ref="containerRef" class="markdown-body" v-html="html" />
  <span v-if="isStreaming" class="cursor-blink">▌</span>
</template>

<style scoped>
.markdown-body {
  font-size: var(--font-base);
  line-height: 1.7;
  color: var(--text-primary);
  word-break: break-word;
}

.markdown-body :deep(a) {
  color: var(--accent);
}

.markdown-body :deep(img) {
  max-width: 100%;
  border-radius: var(--radius-sm);
}

.cursor-blink {
  animation: blink 1s step-end infinite;
  font-size: var(--font-lg);
  color: var(--accent);
}

@keyframes blink {
  50% { opacity: 0; }
}
</style>
