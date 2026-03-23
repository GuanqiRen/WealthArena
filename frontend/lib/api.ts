export type LoginResponse = {
  user_id: string;
  email: string;
  access_token: string;
  token_type: string;
  expires_in?: number;
};

export type Portfolio = {
  id: string;
  user_id: string;
  name: string;
  created_at?: string;
};

export type Position = {
  symbol: string;
  quantity: number;
  average_price: number;
};

export type Trade = {
  trade_id: string;
  symbol: string;
  quantity: number;
  execution_price: number;
  timestamp_ms?: number;
};

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function request<T>(
  path: string,
  init: RequestInit = {},
  token?: string,
): Promise<T> {
  const headers = new Headers(init.headers || {});
  headers.set("Content-Type", "application/json");
  headers.set("Accept", "application/json");

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers,
  });

  const raw = await response.text();
  let data: unknown = null;
  if (raw) {
    try {
      data = JSON.parse(raw);
    } catch {
      data = { detail: raw };
    }
  }

  if (!response.ok) {
    const detail =
      data &&
      typeof data === "object" &&
      "detail" in data &&
      typeof (data as { detail?: unknown }).detail === "string"
        ? (data as { detail: string }).detail
        : null;
    const message: string = detail ?? `Request failed (${response.status})`;
    throw new ApiError(message, response.status);
  }

  return data as T;
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  return request<LoginResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function getPortfolios(token: string): Promise<Portfolio[]> {
  return request<Portfolio[]>("/portfolios", { method: "GET" }, token);
}

export async function getPositions(token: string, portfolioId: string): Promise<Position[]> {
  const query = new URLSearchParams({ portfolio_id: portfolioId }).toString();
  return request<Position[]>(`/trading/positions?${query}`, { method: "GET" }, token);
}

export async function getTrades(token: string, portfolioId: string): Promise<Trade[]> {
  const query = new URLSearchParams({ portfolio_id: portfolioId }).toString();
  return request<Trade[]>(`/trading/trades?${query}`, { method: "GET" }, token);
}
