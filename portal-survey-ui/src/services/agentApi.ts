const AGENT_BASE_URL = import.meta.env.VITE_AGENT_BASE_URL ?? '/agent-api';

export interface AgentMessage {
  role: 'user' | 'assistant';
  content: string;
  requiresConfirmation?: boolean;
}

export interface AgentResponse {
  session_id: string;
  response: string;
  intent: string;
  requires_confirmation: boolean;
  pending_action?: string;
  data: Record<string, unknown>;
}

export async function sendAgentMessage(
  message: string,
  sessionId?: string
): Promise<AgentResponse> {
  const response = await fetch(`${AGENT_BASE_URL}/agent/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || `Agent request failed with status ${response.status}`);
  }

  return response.json() as Promise<AgentResponse>;
}
