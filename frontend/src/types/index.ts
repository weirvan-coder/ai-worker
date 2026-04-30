export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
  isStreaming?: boolean
}

export interface UserMessage {
  role: 'user'
  content: string
}

export interface AgentResponse {
  content: string
  done: boolean
}

export interface ReportMeta {
  filename: string
  filepath: string
  title: string
  created_at: string
}

export type NavItem = {
  id: string
  label: string
  icon: string
  route: string
}

export type ProviderId = 'ollama' | 'dashscope' | 'openai' | 'gemini' | 'deepseek' | 'custom'

export interface ProviderInfo {
  id: ProviderId
  name: string
  description: string
  needsKey: boolean
}
