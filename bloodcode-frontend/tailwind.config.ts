import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],  
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  prefix: "",  
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      colors: {
        "danger": "#ff5f40",
        "purple-start": "#120D17",
        "purple-end": "#27173F",
        "backgroundColor": "#161B22",
        "buttonColor": "#422171",
        "secondary": "#422171",
        "primary": "#693CA5",
        "info": {
          900: "#234e52",
          800: "#285e61",
        },
        "color-gray": {
          900: "#161B22",
          800: "#30363D",
          700: "#36434E",
          600: "#868e94",
        },
        background: "var(--background)",  
        foreground: "var(--foreground)",
      },
      fontFamily: {
        "poppins": ["Poppins", "sans-serif"],
      },
      keyframes: {
        shimmer: {
          "100%": {
            transform: "translateX(100%)",
          },
        },
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        shimmer: "shimmer 1.5s infinite",
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
  },
  plugins: [
    require("tailwindcss-animate"), 
    require("tailwind-scrollbar"),  
  ],
};

export default config;
