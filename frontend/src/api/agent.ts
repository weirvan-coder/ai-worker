import type { ChatMessage, UserMessage, AgentResponse } from '@/types'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:18080'

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2)
}

export async function sendMessage(
  content: string,
  onChunk: (chunk: string) => void,
): Promise<ChatMessage> {
  const msg: UserMessage = { role: 'user', content }
  const id = generateId()

  const response = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(msg),
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  const reader = response.body?.getReader()
  if (!reader) throw new Error('No response body')

  const decoder = new TextDecoder()
  let fullContent = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    const text = decoder.decode(value, { stream: true })
    fullContent += text
    onChunk(text)
  }

  return {
    id,
    role: 'assistant',
    content: fullContent,
    timestamp: Date.now(),
  }
}

export async function fetchReports(): Promise<{ reports: string[] }> {
  const response = await fetch(`${API_BASE}/api/reports`)
  if (!response.ok) throw new Error(`Failed to fetch reports: ${response.status}`)
  return response.json()
}

export async function fetchReportContent(filename: string): Promise<string> {
  const response = await fetch(`${API_BASE}/api/reports/${filename}`)
  if (!response.ok) throw new Error(`Failed to fetch report: ${response.status}`)
  return response.text()
}

export async function healthCheck(): Promise<{ ok: boolean; ready: boolean; error: string }> {
  try {
    const response = await fetch(`${API_BASE}/api/health`)
    const data = await response.json()
    return { ok: response.ok, ready: data.ready ?? response.ok, error: data.error || '' }
  } catch {
    return { ok: false, ready: false, error: '无法连接到后端服务' }
  }
}
