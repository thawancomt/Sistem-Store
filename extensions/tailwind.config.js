/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['../flaskr/blueprints/**/templates/*.{html,js}', '../flaskr/templates/**/*.{html,js}'],
  theme: {
    extend: {},
    darkMode : 'media'
  },
  plugins: [],
}

