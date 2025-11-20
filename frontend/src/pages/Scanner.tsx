import { useState } from "react";
import toast from "react-hot-toast";

import client from "../api/client";

const Scanner = () => {
  const [token, setToken] = useState("");
  const [location, setLocation] = useState("Gateway A");
  const [result, setResult] = useState<{ full_name: string; role?: string; status: string } | null>(null);
  const [loading, setLoading] = useState(false);

  const verify = async () => {
    if (!token.trim()) {
      toast.error("Paste the QR/NFC token");
      return;
    }
    setLoading(true);
    try {
      const { data } = await client.post("/scan/verify", { token, location, channel: "web" });
      setResult(data);
      toast.success("Verified");
    } catch (error) {
      console.error(error);
      toast.error("Verification failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="px-6 py-12">
      <div className="max-w-3xl mx-auto glass-panel p-8 border border-white/10">
        <h2 className="text-2xl font-semibold text-offWhite mb-4">Real-time verification</h2>
        <p className="text-white/70 text-sm mb-6">
          Scan QR or tap NFC to receive the encrypted token. Paste or auto-fill it here to simulate instant verification.
        </p>
        <textarea
          value={token}
          onChange={(e) => setToken(e.target.value)}
          placeholder="Paste encrypted token from QR / NFC"
          rows={4}
          className="w-full bg-white/5 border border-white/10 rounded-3xl px-4 py-3 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-neonAqua/60"
        />
        <div className="mt-4 grid md:grid-cols-2 gap-4">
          <input className="input" value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Location" />
          <button
            onClick={verify}
            disabled={loading}
            className="px-6 py-3 rounded-full bg-gradient-to-r from-neonBlue to-neonPurple text-white font-semibold shadow-glow disabled:opacity-50"
          >
            {loading ? "Verifying..." : "Verify token"}
          </button>
        </div>
        {result && (
          <div className="mt-6 p-4 bg-white/5 border border-white/10 rounded-2xl">
            <p className="text-sm text-neonAqua">{result.status}</p>
            <p className="text-xl font-semibold text-offWhite">{result.full_name}</p>
            <p className="text-white/70">{result.role}</p>
          </div>
        )}
      </div>
    </section>
  );
};

export default Scanner;

