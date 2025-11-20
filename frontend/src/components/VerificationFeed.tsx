import { useLiveScans } from "../hooks/useLiveScans";

const VerificationFeed = () => {
  const events = useLiveScans();

  return (
    <div className="glass-panel p-6 border border-white/10 h-full">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-offWhite">Live verification feed</h3>
        <p className="text-xs text-white/60">Print it. Scan it. Trust it.</p>
      </div>
      <div className="space-y-3 max-h-80 overflow-y-auto pr-2">
        {events.map((event) => (
          <div key={event.timestamp + event.identity_id} className="bg-white/5 border border-white/10 rounded-2xl px-4 py-3">
            <p className="font-semibold text-offWhite">{event.full_name}</p>
            <p className="text-sm text-neonAqua">{event.role}</p>
            <p className="text-xs text-white/60">
              {new Date(event.timestamp).toLocaleTimeString()} • {event.channel.toUpperCase()} • {event.location || "HQ Gate"}
            </p>
          </div>
        ))}
        {!events.length && <p className="text-white/60 text-sm">No scans yet. Open the scanner to begin.</p>}
      </div>
    </div>
  );
};

export default VerificationFeed;

