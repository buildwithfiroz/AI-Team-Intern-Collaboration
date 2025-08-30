//  Configure dark mode and extend theme with custom fonts and animations
tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            fontFamily: { sans: ['Inter', 'ui-sans-serif', 'system-ui'] },
            animation: {
                'fade-in': 'fadeIn 1s ease-out forwards',
                'slide-up': 'slideUp 0.6s ease-out forwards',
                'float': 'float 6s ease-in-out infinite',
            },
            keyframes: {
                fadeIn: { '0%': { opacity: 0 }, '100%': { opacity: 1 } },
                slideUp: { '0%': { opacity: 0, transform: 'translateY(20px)' }, '100%': { opacity: 1, transform: 'translateY(0)' } },
                float: { '0%,100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-10px)' } },
            },
        },
    },
};

// Theme Toggle
const html = document.documentElement;
const toggleBtn = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

const isDark = () => html.classList.contains('dark');

const setIcon = () => {
    themeIcon.innerHTML = isDark()
        ? `<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />`
        : `<path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />`;
};

const toggleTheme = () => {
    html.classList.toggle('dark');
    localStorage.theme = isDark() ? 'dark' : 'light';
    setIcon();
    updateCharts(); // refresh charts with new colors
};

toggleBtn.addEventListener('click', toggleTheme);
setIcon();

// toggle sidebar
function addRemoveAside() {
    const sidebar = document.getElementById('sidebar');
    const box = document.getElementById('box');

    // If sidebar is currently hidden, show it
    if (sidebar.classList.contains('hidden')) {
        sidebar.classList.remove('hidden');
        // Start animation on next frame to allow transition
        requestAnimationFrame(() => {
            sidebar.classList.remove('-translate-x-full');
            sidebar.classList.add('translate-x-0');
        });
        box.classList.remove('ml-0');
        box.classList.add('ml-64');
    } else {
        // Hide it with transition
        sidebar.classList.remove('translate-x-0');
        sidebar.classList.add('-translate-x-full');

        sidebar.classList.add('hidden');

        box.classList.remove('ml-64');
        box.classList.add('ml-15');
    }
}

// scroll butn 
let isScrolledDown = false;

function toggleScroll() {
    if (isScrolledDown) {
        // Scroll up
        window.scrollBy({
            top: -window.innerHeight, // Scroll up by one viewport height
            behavior: 'smooth'        // Smooth scrolling effect
        });

        // Change the icon to "scroll down"
        document.getElementById('scroll-path').setAttribute('d', 'M19 9l-7 7-7-7');
    } else {
        // Scroll down
        window.scrollBy({
            top: window.innerHeight,  // Scroll down by one viewport height
            behavior: 'smooth'        // Smooth scrolling effect
        });

        // Change the icon to "scroll up"
        document.getElementById('scroll-path').setAttribute('d', 'M5 15l7-7 7 7');
    }
    isScrolledDown = !isScrolledDown; // Toggle the state
}


// Chart Colors
const lightColors = {
    text: '#1e293b',
    grid: '#e2e8f0',
    tooltip: '#ffffff',
    line: '#4f46e5',
    bar: '#4f46e5',
};

const darkColors = {
    text: '#f8fafc',
    grid: '#334155',
    tooltip: '#1e293b',
    line: '#818cf8',
    bar: '#818cf8',
};

const getColors = () => (isDark() ? darkColors : lightColors);

// Charts
const chartFont = { family: 'Inter' };

let lineChart, barChart;

const createCharts = () => {

    // Line
    lineChart = new Chart(document.getElementById('lineChart'), {
        type: 'line',
        data: {
            labels: lineLabels,   // from Flask
            datasets: [{
                label: 'Reviews',
                data: lineData,    // from Flask
                fill: false,
                tension: 0.3,
                borderColor: getColors().line,
                pointBackgroundColor: getColors().line,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: {
                    ticks: { color: getColors().text, font: chartFont },
                    grid: { color: getColors().grid }
                },
                y: {
                    beginAtZero: true,
                    ticks: { color: getColors().text, font: chartFont },
                    grid: { color: getColors().grid }
                },
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: getColors().tooltip,
                    titleColor: getColors().text,
                    bodyColor: getColors().text
                },
            },
        },
    });


    // Bar
    barChart = new Chart(document.getElementById('barChart'), {
        type: 'bar',
        data: {
            labels: ['1', '2', '3', '4', '5'],
            datasets: [{
                label: 'Review Count',
                data: starData,   // dynamic data from Flask
                backgroundColor: getColors().bar,
                borderRadius: 4,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: { ticks: { color: getColors().text, font: chartFont }, grid: { display: false } },
                y: { ticks: { color: getColors().text, font: chartFont }, grid: { color: getColors().grid } },
            },
            plugins: {
                legend: { display: false },
                tooltip: { backgroundColor: getColors().tooltip, titleColor: getColors().text, bodyColor: getColors().text },
            },
        },
    });

};

const updateCharts = () => {
    [lineChart, barChart].forEach(chart => {
        if (!chart) return;
        chart.options.plugins.legend.labels.color = getColors().text;
        chart.options.scales.x && (chart.options.scales.x.ticks.color = getColors().text);
        chart.options.scales.y && (chart.options.scales.y.ticks.color = getColors().text);
        chart.options.scales.x && (chart.options.scales.x.grid.color = getColors().grid);
        chart.options.scales.y && (chart.options.scales.y.grid.color = getColors().grid);
        chart.options.plugins.tooltip.backgroundColor = getColors().tooltip;
        chart.options.plugins.tooltip.titleColor = getColors().text;
        chart.options.plugins.tooltip.bodyColor = getColors().text;

        // Update colors
        if (chart.config.type === 'line') chart.data.datasets[0].borderColor = chart.data.datasets[0].pointBackgroundColor = getColors().line;
        if (chart.config.type === 'bar') chart.data.datasets[0].backgroundColor = getColors().bar;

        chart.update();
    });
};

createCharts();