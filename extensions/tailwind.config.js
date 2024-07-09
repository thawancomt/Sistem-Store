/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['../store/blueprints/**/templates/*.{html,js}', '../store/templates/**/*.{html,js}', '../store/blueprints/**/**.{html,js}'],
  theme: {
    extend: {},
    darkMode : 'media'
  },
  plugins: [],
}

