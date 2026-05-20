export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      boxShadow: {
        soft: '0 12px 30px rgba(15, 23, 42, 0.08)'
      },
      colors: {
        primary: '#0f172a',
        accent: '#2563eb'
      }
    }
  },
  plugins: []
};
