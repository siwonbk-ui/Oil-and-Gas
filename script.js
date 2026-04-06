document.addEventListener('DOMContentLoaded', () => {
    // 1. Theme Toggle Logic
    const themeToggle = document.getElementById('theme-toggle');
    const rootElements = document.documentElement;
    const themeIcon = themeToggle.querySelector('i');
    const themeText = themeToggle.querySelector('span');

    let isDark = false;

    themeToggle.addEventListener('click', () => {
        isDark = !isDark;
        if (isDark) {
            rootElements.setAttribute('data-theme', 'dark');
            themeIcon.classList.replace('fa-moon', 'fa-sun');
            themeText.textContent = 'Light Mode';
        } else {
            rootElements.removeAttribute('data-theme');
            themeIcon.classList.replace('fa-sun', 'fa-moon');
            themeText.textContent = 'Dark Mode';
        }
        updateChartTheme();
    });

    // 2. Date Display
    const dateDisplay = document.getElementById('current-date');
    const options = { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' };
    dateDisplay.textContent = new Date().toLocaleDateString('en-US', options);

    // 3. Data Structure initialization
    let fuelData = null;
    let currentFuel = 'gasoline';

    // 4. Initialization
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.color = "#64748b";

    let trendChart;
    let barChart;

    const cardsContainer = document.getElementById('price-cards-container');
    const ctxTrend = document.getElementById('trendChart').getContext('2d');
    const ctxBar = document.getElementById('barChart').getContext('2d');
    const chartTitle = document.getElementById('trend-chart-title');

    function initCharts() {
        trendChart = new Chart(ctxTrend, {
            type: 'line',
            data: { labels: [], datasets: [] },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } },
                scales: { 
                    y: { 
                        beginAtZero: false, 
                        title: { display: true, text: 'Price (THB)' } 
                    } 
                }
            }
        });

        barChart = new Chart(ctxBar, {
            type: 'bar',
            data: { labels: [], datasets: [] },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } }
            }
        });
    }

    function renderDashboard(fuelType) {
        const dataSet = fuelData[fuelType];
        
        // Update Chart Title
        if (chartTitle) {
            chartTitle.textContent = `Price Trends Overview (${dataSet.title})`;
        }

        // Render Cards
        cardsContainer.innerHTML = '';
        dataSet.cards.forEach(data => {
            const trendIcon = data.trend === 'up' ? 'fa-arrow-trend-up' : (data.trend === 'down' ? 'fa-arrow-trend-down' : 'fa-minus');
            
            const card = document.createElement('div');
            card.className = 'card';
            card.style.setProperty('--card-color', data.color);
            
            card.innerHTML = `
                <div class="card-header">
                    <span class="country-name">
                        <span style="font-size: 1.2em;">${data.flag}</span>
                        ${data.country}
                    </span>
                    <span class="gas-type">${data.type}</span>
                </div>
                <div class="price">
                    ${data.price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} 
                    <span class="price-unit">${data.unit}</span>
                </div>
                <div class="trend ${data.trend}">
                    <i class="fa-solid ${trendIcon}"></i>
                    <span>${data.change} (vs yesterday)</span>
                </div>
            `;
            cardsContainer.appendChild(card);
        });

        // Update Line Chart
        const timeRangeSelect = document.getElementById('time-range');
        const days = timeRangeSelect ? parseInt(timeRangeSelect.value) : 7;
        
        trendChart.data.labels = dataSet.history.labels.slice(-days);
        trendChart.data.datasets = dataSet.history.datasets.map(dataset => ({
            ...dataset,
            data: dataset.data.slice(-days)
        }));
        trendChart.update();

        // Update Bar Chart
        barChart.data.labels = dataSet.cards.map(c => c.code);
        
        const colorMap = {
            'TH': 'rgba(239, 68, 68, 0.8)',
            'MY': 'rgba(245, 158, 11, 0.8)',
            'SG': 'rgba(16, 185, 129, 0.8)',
            'ID': 'rgba(99, 102, 241, 0.8)',
            'VN': 'rgba(236, 72, 153, 0.8)',
            'PH': 'rgba(59, 130, 246, 0.8)',
            'LA': 'rgba(139, 92, 246, 0.8)'
        };

        barChart.data.datasets = [{
            label: 'Price in THB',
            data: dataSet.cards.map(c => c.price),
            backgroundColor: dataSet.cards.map(c => colorMap[c.code]),
            borderRadius: 6
        }];
        barChart.update();
        
        updateChartTheme();
    }

    // 5. Handle Navigation Tabs
    const navItems = document.querySelectorAll('.nav-menu .nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            const type = item.getAttribute('data-type');
            if (type && fuelData[type]) {
                currentFuel = type;
                renderDashboard(type);
            }
        });
    });

    // 6. Handle Time Range Dropdown
    const timeRangeSelect = document.getElementById('time-range');
    if (timeRangeSelect) {
        timeRangeSelect.addEventListener('change', () => {
            if (fuelData && currentFuel) {
                renderDashboard(currentFuel);
            }
        });
    }

    function updateChartTheme() {
        const textColor = isDark ? '#94a3b8' : '#64748b';
        const gridColor = isDark ? '#334155' : '#e2e8f0';

        [trendChart, barChart].forEach(chart => {
            chart.options.scales.x.grid.color = gridColor;
            chart.options.scales.y.grid.color = gridColor;
            chart.options.scales.x.ticks.color = textColor;
            chart.options.scales.y.ticks.color = textColor;
            if(chart.options.plugins.legend) {
                chart.options.plugins.legend.labels.color = textColor;
            }
            chart.update();
        });
    }

    // Initialize
    initCharts();
    
    // Fetch data from external JSON file
    fetch('data.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            fuelData = data;
            
            // Optionally update date display if timestamp is provided
            if(data.last_updated) {
                dateDisplay.textContent = `Updated: ${data.last_updated}`;
            }
            
            renderDashboard(currentFuel);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            cardsContainer.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding: 40px; color: #ef4444;">Failed to load data. Please ensure you are running this on a web server or GitHub Pages, not directly from file://</div>';
        });
});
