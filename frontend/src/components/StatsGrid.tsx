const stats = [
  { label: "Bulk speed", value: "500 IDs / min", caption: "CSV, Excel, photo URLs" },
  { label: "Verification", value: "0.8s scan", caption: "QR + NFC one tap" },
  { label: "Export", value: "PNG · PDF · Wallet", caption: "Print-ready @300DPI" },
  { label: "Trust", value: "AES256 token", caption: "A card that verifies itself." }
];

const StatsGrid = () => {
  return (
    <section className="px-6 -mt-4">
      <div className="max-w-6xl mx-auto grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="glass-panel p-6 text-center border border-white/10">
            <p className="text-sm uppercase tracking-[0.4em] text-white/60">{stat.label}</p>
            <p className="text-2xl font-semibold mt-3 text-offWhite">{stat.value}</p>
            <p className="text-white/70 text-sm mt-2">{stat.caption}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default StatsGrid;

