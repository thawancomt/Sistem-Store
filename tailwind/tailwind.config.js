/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ["../System/templates/**/*.{html,js}", "System/templates/*.{html,js}"],
  theme: {
    extend: {
      transitionProperty: {
        'height': 'height',
      }
    },
  },
  plugins: [],
}