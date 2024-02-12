/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        'color1': 'var(--color-color1)',
        'color2': 'var(--color-color2)',
      },
    },
    screens: {
      'sm': '640px', //tablet
      'md': '768px',
      'lg': '1024px', //laptop
      'xl': '1440px', //desktop
      '2xl': '1700px',
    },
    container: {
      center: true,
      padding: {
        DEFAULT: '1rem',
        sm: '1.3rem',
        md: '2rem',
        lg: '2rem',
        xl: '2.5rem',
        '2xl' : '10rem',
      }
    }
  },
  plugins: [require("daisyui")],
};
