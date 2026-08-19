/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brandDark: "#0B1F3A",
        brandRoyal: "#185FA5",
        brandEmerald: "#0F6E56",
        brandNeutral: "#444441",
        brandSand: "#F1EFE8",
      }
    },
  },
  plugins: [],
}
