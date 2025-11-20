const heroBullets = [
  "AI face detection, cleanup & alignment",
  "Auto-branding with logo, colors & typography",
  "QR/NFC tokens that verify in one tap",
  "Bulk generation + live attendance analytics"
];

const Hero = () => {
  return (
    <section className="px-6 py-12 md:py-16">
      <div className="max-w-6xl mx-auto grid md:grid-cols-[1.2fr,0.8fr] gap-10 items-center glass-panel p-10">
        <div>
          <p className="uppercase tracking-[0.4em] text-neonAqua text-sm mb-4">Identity meets intelligence</p>
          <h1 className="text-4xl md:text-5xl font-semibold leading-tight neon-title text-offWhite">
            Smart IDs for smarter institutions.
          </h1>
          <p className="text-lg text-white/80 mt-4 max-w-2xl">
            We don’t just create ID cards; we secure identities. Upload faces, logos or entire spreadsheets and let the
            AI render print-ready cards, digital wallet passes and encrypted QR/NFC tokens that verify themselves in
            real time.
          </p>
          <ul className="mt-6 grid gap-3">
            {heroBullets.map((item) => (
              <li key={item} className="flex items-center gap-3 text-white/85">
                <span className="inline-flex h-2 w-8 rounded-full bg-gradient-to-r from-neonBlue to-neonPurple" />
                {item}
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-gradient-to-br from-neonBlue/30 via-neonPurple/20 to-neonAqua/20 rounded-3xl p-6 border border-white/10 shadow-glow">
          <h3 className="text-xl font-semibold mb-2 text-offWhite">Elevator pitch</h3>
          <p className="text-white/80 text-sm leading-relaxed">
            “We don’t just create ID cards; we secure identities. Our system turns normal ID cards into AI-generated
            smart identities with QR/NFC verification, institution-based auto-branding and one-click bulk generation.”
          </p>
          <div className="mt-6 space-y-3 text-sm text-white/70">
            <p>Identity that protects itself.</p>
            <p>Print it. Scan it. Trust it.</p>
            <p>A card that verifies itself.</p>
            <p>Your identity, now intelligent.</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;

