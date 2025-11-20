/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        neonBlue: "#1D6FFF",
        neonPurple: "#6F00FF",
        neonAqua: "#00F3FF",
        offWhite: "#F8FBFF",
        midnight: "#000319"
      },
      backgroundImage: {
        "hero-gradient": "linear-gradient(135deg,#1D6FFF,#6F00FF,#00F3FF)"
      },
      boxShadow: {
        glow: "0 0 30px rgba(0,243,255,0.4)"
      }
    }
  },
  plugins: []
};

