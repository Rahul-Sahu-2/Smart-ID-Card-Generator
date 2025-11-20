const posterLines = [
  "Futuristic holographic smart ID cards floating with glassmorphism panels",
  "Face detection frame overlay + glowing QR + NFC icon in neon blue/purple/aqua gradient",
  "Headline: “Smart Identity Generator” in premium minimal typography",
  "Taglines: “A card that verifies itself.” “Identity that protects itself.”",
  "Background: blue-purple cyber-tech gradient with soft particles and circuit textures"
];

const PosterBrief = () => {
  return (
    <div className="glass-panel p-6 border border-white/10">
      <h3 className="text-lg font-semibold text-offWhite mb-3">Poster / UI direction</h3>
      <p className="text-white/70 text-sm mb-4">
        “Futuristic holographic smart ID cards, glowing QR, NFC symbol, blue-purple neon cyber-tech gradients, face
        detection frame, glassmorphism, premium minimal high-tech UI, glowing title ‘Smart Identity Generator’, modern
        clean typography, digital authentication theme.”
      </p>
      <ul className="list-disc list-inside space-y-2 text-sm text-white/80 marker:text-neonAqua">
        {posterLines.map((line) => (
          <li key={line}>{line}</li>
        ))}
      </ul>
    </div>
  );
};

export default PosterBrief;

