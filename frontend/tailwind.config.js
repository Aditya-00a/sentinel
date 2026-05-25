/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'val-red': '#FF4655',
        'val-red-deep': '#D1313C',
        'val-red-glow': 'rgba(255, 70, 85, 0.15)',
        'val-dark': '#0A0E13',
        'val-card': '#0F1923',
        'val-card-2': '#141E2B',
        'val-border': '#1F2937',
        'val-border-light': '#2D3A4A',
        'val-text': '#E2E8F0',
        'val-gray': '#94A3B8',
        'val-dim': '#64748B',
        'val-muted': '#475569',
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
