"use client";

import { useEffect, useMemo, useRef, useState } from "react";

export type LivePosition = {
  symbol: string;
  price: number;
  quantity: number;
  average_price: number;
  pnl: number;
};

export type PortfolioStreamPayload = {
  portfolio_id: string;
  positions: LivePosition[];
  total_pnl: number;
  timestamp_ms: number;
};

type UseWebSocketResult = {
  livePositions: LivePosition[];
  totalPnl: number;
  isConnected: boolean;
  error: string | null;
};

function toWebSocketBaseUrl(apiBaseUrl: string): string {
  if (apiBaseUrl.startsWith("https://")) {
    return apiBaseUrl.replace("https://", "wss://");
  }
  if (apiBaseUrl.startsWith("http://")) {
    return apiBaseUrl.replace("http://", "ws://");
  }
  return apiBaseUrl;
}

export function useWebSocket(portfolioId?: string, token?: string | null): UseWebSocketResult {
  const [livePositions, setLivePositions] = useState<LivePosition[]>([]);
  const [totalPnl, setTotalPnl] = useState(0);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const retryRef = useRef(0);
  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const wsUrl = useMemo(() => {
    if (!portfolioId || !token) {
      return null;
    }

    const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
    const wsBaseUrl = toWebSocketBaseUrl(apiBaseUrl);
    const query = new URLSearchParams({ token }).toString();
    return `${wsBaseUrl}/ws/portfolio/${portfolioId}?${query}`;
  }, [portfolioId, token]);

  useEffect(() => {
    if (!wsUrl) {
      return;
    }

    let socket: WebSocket | null = null;
    let shouldReconnect = true;

    const connect = () => {
      socket = new WebSocket(wsUrl);

      socket.onopen = () => {
        retryRef.current = 0;
        setIsConnected(true);
        setError(null);
      };

      socket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data) as PortfolioStreamPayload;
          setLivePositions(payload.positions || []);
          setTotalPnl(payload.total_pnl || 0);
        } catch {
          setError("Received invalid realtime payload.");
        }
      };

      socket.onerror = () => {
        setError("Realtime connection error.");
      };

      socket.onclose = () => {
        setIsConnected(false);

        if (!shouldReconnect) {
          return;
        }

        retryRef.current += 1;
        const backoffMs = Math.min(1000 * 2 ** retryRef.current, 10000);

        reconnectTimerRef.current = setTimeout(() => {
          connect();
        }, backoffMs);
      };
    };

    connect();

    return () => {
      shouldReconnect = false;
      if (reconnectTimerRef.current) {
        clearTimeout(reconnectTimerRef.current);
      }
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
    };
  }, [wsUrl]);

  return { livePositions, totalPnl, isConnected, error };
}
