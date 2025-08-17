/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Colores principales definidos según las preferencias del usuario
                primary: {
                    600: '#4b5563', // Color primario (gris)
                    700: '#374151', // Color secundario (gris oscuro)
                },
                accent: {
                    500: '#ef4444', // Error/Pendiente (ROJO)
                    600: '#dc2626', // Énfasis/Acentos (ROJO)
                },
                secondary: {
                    600: '#64748B', // Texto secundario
                    900: '#1E293B', // Texto principal
                },
                success: '#10B981',
                warning: '#F59E0B',
                background: {
                    main: '#F1F5F9',
                    card: '#FFFFFF',
                }
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
