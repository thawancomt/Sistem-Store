/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ["../blueprints/**/templates/*.{html,js}", "../templates/*.{html,js}"],
  theme: {
    extend: {
      transitionProperty: {
        'height': 'height',
      }
    },
  },
  plugins: [],
}