/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'val-red': '#C89B3C',
        'val-red-deep': '#A0792A',
        'val-red-glow': 'rgba(200, 155, 60, 0.15)',
        'val-dark': '#010A13',
        'val-card': '#0A1428',
        'val-card-2': '#0F1E35',
        'val-border': '#1E2D40',
        'val-border-light': '#2A3F57',
        'val-text': '#C8AA6E',
        'val-gray': '#A09B8C',
        'val-dim': '#5B5A56',
        'val-muted': '#3C3C35',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
      letterSpacing: {
        'widest-xl': '0.2em',
        'wide-lg': '0.08em',
      },
    },
  },
  plugins: [],
}
