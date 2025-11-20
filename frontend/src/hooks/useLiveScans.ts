import { useEffect, useState } from "react";

interface LiveScan {
  identity_id: number;
  full_name: string;
  role?: string;
  timestamp: string;
  location?: string;
  channel: string;
}

export const useLiveScans = () => {
  const [events, setEvents] = useState<LiveScan[]>([]);

  useEffect(() => {
    const base = (import.meta.env.VITE_WS_BASE_URL as string) || "ws://localhost:8000/api/scan/live";
    const socket = new WebSocket(base);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setEvents((prev) => [data, ...prev].slice(0, 10));
    };

    socket.onerror = () => {
      console.warn("Live scan socket disconnected");
    };

    return () => socket.close();
  }, []);

  return events;
};

