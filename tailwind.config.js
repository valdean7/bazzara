/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      './templates/**/*.{html,js}',
      './registro/templates/*.{html,js}',
      './endereco/templates/*.{html,js}',
      './produtos/templates/*.{html,js}',
      './pedidos/templates/*.{html,js}',
    ],
    theme: {
      extend: {
          colors: {
              'nude': {
              100: '#ffffff',
              200: '#f0edea',
              300: '#e1dbd4',
              400: '#d1c9bf',
              500: '#c2b7a9',
              },
              'semiblack': '#353535',
              'grafite': '#2B2B2B',
              'ligth-gray': '#DCDCDC',
              'ligth-blue': '#007185',
              'milk': '#F5F5F5',
              'ligth-milk': '#FFFEFB',
          },
          fontFamily: {
              Raleway: ['Raleway', 'sans-serif']
          },
          fontSize: {'1xl': '0.9rem'},
          spacing: {
              '470px': '470px',
              '115px': '115px',
              '18px': '18px',
              '525px': '525px',
              '415px': '415px',
              '40px': '40px',
          },
          screens: {
              'sm': '0px',
          }
      },
    },
    plugins: [],
  }
  
  