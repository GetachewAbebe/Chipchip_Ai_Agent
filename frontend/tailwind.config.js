/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}


// tailwind.config.js
module.exports = {
  // ...
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      animation: {
        fadeIn: "fadeIn 0.2s ease-out",
        scaleIn: "scaleIn 0.2s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: 0 },
          "100%": { opacity: 1 },
        },
        scaleIn: {
          "0%": { transform: "scale(0.95)" },
          "100%": { transform: "scale(1)" },
        },
      },
    },
  },
  plugins: [],
};
