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
    let impactBarChart;
    let impactComboChart;
    let electricBarChart;
    let electricDoughnutChart;
    let trendsLineChart;
    let trendsBarChart;

    // Register ChartDataLabels plugin globally
    if (typeof ChartDataLabels !== 'undefined') {
        Chart.register(ChartDataLabels);
    }

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
                plugins: { 
                    legend: { position: 'bottom' },
                    datalabels: { display: false }
                },
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
                plugins: { 
                    legend: { display: false },
                    datalabels: { display: false }
                }
            }
        });

        const ctxImpactBar = document.getElementById('impactBarChart');
        if (ctxImpactBar) {
            impactBarChart = new Chart(ctxImpactBar.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ["Jan '26", "Feb '26", "Mar '26", "Apr '26 (S1)", "Apr '26 (S2)", "Apr '26 (S3)"],
                    datasets: [{
                        data: [1.35, 1.42, 1.39, 2.15, 2.58, 3.01],
                        backgroundColor: [
                            '#1d4ed8', '#1d4ed8', '#1d4ed8', 
                            '#f97316', '#ea580c', '#b91c1c'
                        ],
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { 
                        legend: { display: false },
                        datalabels: {
                            anchor: 'end',
                            align: 'top',
                            formatter: (value, context) => {
                                if (context.dataIndex === 3) return value + '\n(+54%)';
                                if (context.dataIndex === 4) return value + '\n(+85%)';
                                if (context.dataIndex === 5) return value + '\n(+116%)';
                                return value;
                            },
                            font: { weight: 'bold', size: 11 },
                            color: (context) => {
                                return context.dataIndex >= 3 ? '#b91c1c' : '#1d4ed8';
                            },
                            textAlign: 'center'
                        }
                    },
                    scales: { y: { beginAtZero: true, max: 4.0 } },
                    animation: false
                }
            });
        }

        const ctxImpactCombo = document.getElementById('impactComboChart');
        if (ctxImpactCombo) {
            impactComboChart = new Chart(ctxImpactCombo.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ["Jan '26", "Feb '26", "Mar '26", "Apr '26 (S1)", "Apr '26 (S2)", "Apr '26 (S3)"],
                    datasets: [
                        {
                            type: 'line',
                            label: 'ราคาเฉลี่ยต่อเดือน (บาท)',
                            data: [30.3, 30.3, 32.5, 50, 60, 70],
                            borderColor: '#ef4444',
                            backgroundColor: '#ef4444',
                            borderWidth: 2,
                            tension: 0.1,
                            yAxisID: 'y1',
                            datalabels: {
                                anchor: 'start',
                                align: 'top',
                                font: { weight: 'bold', size: 11 },
                                color: '#ef4444'
                            }
                        },
                        {
                            type: 'bar',
                            label: 'ปริมาณการใช้ (ลิตร)',
                            data: [45000, 46800, 42900, 43000, 43000, 43000],
                            backgroundColor: '#cbd5e1',
                            yAxisID: 'y',
                            datalabels: {
                                anchor: 'center',
                                align: 'center',
                                formatter: (val) => (val/1000).toFixed(1) + 'k',
                                font: { size: 10 },
                                color: '#64748b'
                            }
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' }
                    },
                    scales: {
                        y: { 
                            type: 'linear', 
                            display: true, 
                            position: 'left',
                            title: { display: true, text: 'ปริมาณ (ลิตร)' },
                            min: 0, max: 60000
                        },
                        y1: { 
                            type: 'linear', 
                            display: true, 
                            position: 'right',
                            title: { display: true, text: 'ราคา (บาท)' },
                            min: 0, max: 80,
                            grid: { drawOnChartArea: false }
                        }
                    },
                    animation: false
                }
            });
        }

        const ctxElectricBar = document.getElementById('electricBarChart');
        if (ctxElectricBar) {
            electricBarChart = new Chart(ctxElectricBar.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['พฤษภาคม - สิงหาคม', 'กันยายน - ธันวาคม'],
                    datasets: [{
                        data: [142752.25, 281160.43],
                        backgroundColor: ['#3b82f6', '#ef4444'],
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        datalabels: {
                            anchor: 'end',
                            align: 'top',
                            formatter: (val) => val.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}),
                            font: { size: 10 },
                            color: '#64748b'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    if (value >= 1000) return value / 1000 + 'k';
                                    return value;
                                }
                            }
                        }
                    }
                }
            });
        }

        const ctxElectricDoughnut = document.getElementById('electricDoughnutChart');
        if (ctxElectricDoughnut) {
            electricDoughnutChart = new Chart(ctxElectricDoughnut.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: ['พฤษภาคม - สิงหาคม', 'กันยายน - ธันวาคม'],
                    datasets: [{
                        data: [2039317.83, 2343803.58],
                        backgroundColor: ['#3b82f6', '#ef4444'],
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '70%',
                    plugins: {
                        legend: { position: 'bottom' },
                        datalabels: { display: false }
                    }
                }
            });
        }

        const ctxTrendsLine = document.getElementById('trendsLineChart');
        if (ctxTrendsLine) {
            trendsLineChart = new Chart(ctxTrendsLine.getContext('2d'), {
                type: 'line',
                data: {
                    labels: ['18 มี.ค. 69', '21 มี.ค. 69', '24 มี.ค. 69', '26 มี.ค. 69', '31 มี.ค. 69', '2 เม.ย. 69', '3 เม.ย. 69', '5 เม.ย. 69'],
                    datasets: [
                        { label: 'ดีเซล', data: [0.5, 0.7, 1.8, 6.0, 1.8, 3.5, 3.5, 2.8], borderColor: '#1d4ed8', backgroundColor: '#1d4ed8', tension: 0.3 },
                        { label: 'เบนซิน/โซฮอล์', data: [1.0, 1.0, 2.0, 6.0, 1.0, 1.2, 0.7, null], borderColor: '#dc2626', backgroundColor: '#dc2626', tension: 0.3, spanGaps: true },
                        { label: 'E20', data: [-0.79, 1.0, 2.0, 6.0, 1.0, 1.2, 0.7, null], borderColor: '#f59e0b', backgroundColor: '#f59e0b', tension: 0.3, spanGaps: true },
                        { label: 'E85', data: [-2.0, 1.0, 2.0, 6.0, 1.0, 1.2, 0.7, null], borderColor: '#10b981', backgroundColor: '#10b981', tension: 0.3, spanGaps: true }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { 
                        legend: { position: 'bottom' },
                        datalabels: { display: false }
                    },
                    scales: { y: { beginAtZero: false } },
                    interaction: { mode: 'index', intersect: false }
                }
            });
        }

        const ctxTrendsBar = document.getElementById('trendsBarChart');
        if (ctxTrendsBar) {
            trendsBarChart = new Chart(ctxTrendsBar.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['เบนซิน/โซฮอล์', 'E20', 'E85', 'ดีเซลธรรมดา'],
                    datasets: [{
                        data: [12.90, 11.11, 9.90, 20.60],
                        backgroundColor: ['#dc2626', '#f59e0b', '#10b981', '#1d4ed8'],
                        borderRadius: 4
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        datalabels: {
                            anchor: 'end',
                            align: 'right',
                            formatter: (val) => '+' + val.toFixed(2),
                            font: { size: 11, weight: 'bold' },
                            color: '#64748b'
                        }
                    },
                    scales: {
                        x: { beginAtZero: true, max: 25 },
                        y: { grid: { display: false } }
                    }
                }
            });
        }
    }

    function renderTrendsTH() {
        if (!fuelData || !fuelData.trends_th) return;
        const trends = fuelData.trends_th;
        const tableData = trends.table_data;

        // 1. Update Metrics
        let totalGasoline = 0;
        let totalE20 = 0;
        let totalE85 = 0;
        let totalDiesel = 0;
        let peakValue = 0;
        let peakDate = "";

        tableData.forEach(row => {
            totalGasoline += row.gasoline;
            totalE20 += row.e20;
            totalE85 += row.e85;
            totalDiesel += row.diesel;

            // Find peak in a single adjustment (any fuel)
            const maxInRow = Math.max(Math.abs(row.gasoline), Math.abs(row.e20), Math.abs(row.e85), Math.abs(row.diesel));
            if (maxInRow > peakValue) {
                peakValue = maxInRow;
                peakDate = row.date;
            }
        });

        const mDiesel = document.getElementById('trends-metric-diesel');
        const sDiesel = document.getElementById('trends-sub-diesel');
        if (mDiesel) mDiesel.innerHTML = `${totalDiesel > 0 ? '+' : ''}${totalDiesel.toFixed(2)} <span>บ./ลิตร</span>`;
        if (sDiesel) sDiesel.innerHTML = `<i class="fa-solid fa-arrow-trend-up"></i> จากการปรับเปลี่ยน ${tableData.length} ครั้ง`;

        const mGasoline = document.getElementById('trends-metric-gasoline');
        const sGasoline = document.getElementById('trends-sub-gasoline');
        if (mGasoline) mGasoline.innerHTML = `${totalGasoline > 0 ? '+' : ''}${totalGasoline.toFixed(2)} <span>บ./ลิตร</span>`;
        if (sGasoline) sGasoline.innerHTML = `<i class="fa-regular fa-calendar"></i> สะสมตั้งแต่ ${tableData[0].date}`;

        const mRank = document.getElementById('trends-metric-rank');
        const sRank = document.getElementById('trends-sub-rank');
        if (mRank) mRank.innerHTML = `อันดับ 7 <span>จาก 10</span>`;
        if (sRank) sRank.innerHTML = `<i class="fa-solid fa-circle-info"></i> ถูกกว่า ลาว พม่า กัมพูชา มาเลเซีย`;

        const mPeak = document.getElementById('trends-metric-peak');
        const sPeak = document.getElementById('trends-sub-peak');
        if (mPeak) mPeak.innerHTML = `+${peakValue.toFixed(2)} <span>บ./ลิตร</span>`;
        if (sPeak) sPeak.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> เมื่อวันที่ ${peakDate}`;

        // 2. Render Table
        const tbody = document.getElementById('trends-table-tbody');
        if (tbody) {
            tbody.innerHTML = '';
            tableData.forEach(row => {
                const tr = document.createElement('tr');
                if (Math.abs(row.gasoline) >= 5 || Math.abs(row.diesel) >= 5) tr.className = 'highlight-row';
                
                const fmt = (v) => v === 0 ? '-' : (v > 0 ? '+' : '') + v.toFixed(2);
                const cls = (v) => v < 0 ? 'negative' : '';

                tr.innerHTML = `
                    <td>${row.date}</td>
                    <td class="${cls(row.gasoline)}">${fmt(row.gasoline)}</td>
                    <td class="${cls(row.e20)}">${fmt(row.e20)}</td>
                    <td class="${cls(row.e85)}">${fmt(row.e85)}</td>
                    <td class="${cls(row.diesel)}">${fmt(row.diesel)}</td>
                `;
                tbody.appendChild(tr);
            });

            // Total Row
            const totalTr = document.createElement('tr');
            totalTr.className = 'total-row';
            totalTr.innerHTML = `
                <td>รวมทั้งหมด</td>
                <td>${totalGasoline > 0 ? '+' : ''}${totalGasoline.toFixed(2)}</td>
                <td class="val-orange">${totalE20 > 0 ? '+' : ''}${totalE20.toFixed(2)}</td>
                <td class="val-green">${totalE85 > 0 ? '+' : ''}${totalE85.toFixed(2)}</td>
                <td class="val-blue">${totalDiesel > 0 ? '+' : ''}${totalDiesel.toFixed(2)}</td>
            `;
            tbody.appendChild(totalTr);
        }

        // 3. Update Charts
        if (trendsLineChart) {
            const labels = tableData.map(r => r.date);
            
            // Calculate cumulative sums for line chart
            let sumG = 0, sumE20 = 0, sumE85 = 0, sumD = 0;
            const dataG = [], dataE20 = [], dataE85 = [], dataD = [];

            tableData.forEach(r => {
                sumG += r.gasoline;
                sumE20 += r.e20;
                sumE85 += r.e85;
                sumD += r.diesel;
                dataG.push(sumG);
                dataE20.push(sumE20);
                dataE85.push(sumE85);
                dataD.push(sumD);
            });

            trendsLineChart.data.labels = labels;
            trendsLineChart.data.datasets[0].data = dataD;
            trendsLineChart.data.datasets[1].data = dataG;
            trendsLineChart.data.datasets[2].data = dataE20;
            trendsLineChart.data.datasets[3].data = dataE85;
            trendsLineChart.update();
        }

        if (trendsBarChart) {
            trendsBarChart.data.datasets[0].data = [totalGasoline, totalE20, totalE85, totalDiesel];
            trendsBarChart.update();
        }
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
    const overviewView = document.getElementById('overview-view');
    const impactView = document.getElementById('impact-view');
    const electricView = document.getElementById('electric-impact-view');
    const trendsThView = document.getElementById('trends-th-view');
    const headerTitle = document.querySelector('.header h1');
    const headerSubtitle = document.querySelector('.header .subtitle');

    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            const type = item.getAttribute('data-type');
            
            if (type === 'trends-th') {
                overviewView.style.display = 'none';
                impactView.style.display = 'none';
                if(electricView) electricView.style.display = 'none';
                if(trendsThView) trendsThView.style.display = 'block';
                // Hide main header as custom one is used within the view
                document.querySelector('.header').style.display = 'none';
                renderTrendsTH();
            } else if (type === 'impact') {
                document.querySelector('.header').style.display = 'flex';
                overviewView.style.display = 'none';
                if(electricView) electricView.style.display = 'none';
                if(trendsThView) trendsThView.style.display = 'none';
                impactView.style.display = 'block';
                headerTitle.textContent = 'Scenario น้ำมัน';
                headerSubtitle.textContent = 'Impact evaluation of oil price adjustments';
            } else if (type === 'electric') {
                document.querySelector('.header').style.display = 'flex';
                overviewView.style.display = 'none';
                impactView.style.display = 'none';
                if(trendsThView) trendsThView.style.display = 'none';
                if(electricView) electricView.style.display = 'block';
                headerTitle.textContent = 'ค่าไฟฟ้า (Ft) ปี 2569 กรณีปรับราคาตามรัฐบาลประกาศ';
                headerSubtitle.textContent = 'อ้างอิงจากการใช้จากปี 2568';
            } else if (fuelData && fuelData[type]) {
                document.querySelector('.header').style.display = 'flex';
                overviewView.style.display = 'block';
                impactView.style.display = 'none';
                if(electricView) electricView.style.display = 'none';
                if(trendsThView) trendsThView.style.display = 'none';
                headerTitle.textContent = 'Overview';
                headerSubtitle.textContent = 'Latest retail fuel prices in Southeast Asia';
                
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

        [trendChart, barChart, impactBarChart, impactComboChart, electricBarChart, electricDoughnutChart, trendsLineChart, trendsBarChart].forEach(chart => {
            if (!chart) return;
            
            if (chart.options.scales) {
                if (chart.options.scales.x) {
                    chart.options.scales.x.grid.color = gridColor;
                    chart.options.scales.x.ticks.color = textColor;
                }
                if (chart.options.scales.y) {
                    chart.options.scales.y.grid.color = gridColor;
                    chart.options.scales.y.ticks.color = textColor;
                }
                if (chart.options.scales.y1) {
                    chart.options.scales.y1.ticks.color = textColor;
                }
            }
            if(chart.options.plugins && chart.options.plugins.legend) {
                chart.options.plugins.legend.labels.color = textColor;
            }
            chart.update();
        });
    }

    // Initialize
    initCharts();
    
    function updateScenarioStatus() {
        if (!fuelData || !fuelData['diesel']) return;
        
        // Find TH Diesel price
        const thDieselData = fuelData['diesel'].cards.find(c => c.code === 'TH');
        if (!thDieselData) return;
        
        const price = thDieselData.price;
        const statusText = document.getElementById('scenario-status-text');
        const statusContainer = document.getElementById('scenario-status-container');
        if (!statusText || !statusContainer) return;
        
        const icon = statusContainer.querySelector('i');
        
        let scenario = 0;
        if (price >= 70) scenario = 3;
        else if (price >= 60) scenario = 2;
        else if (price >= 50) scenario = 1;
        
        if (scenario > 0) {
            statusText.textContent = `เข้าสู่ Scenario ${scenario} แล้ว (ราคาจริงแตะ ${price.toFixed(2)} บ./ลิตร)`;
            statusContainer.style.backgroundColor = 'rgba(239, 68, 68, 0.05)';
            statusContainer.style.borderColor = 'rgba(239, 68, 68, 0.2)';
            icon.className = 'fa-solid fa-triangle-exclamation';
            icon.style.color = 'var(--color-th)';
        } else {
            statusText.textContent = `สถานการณ์ปกติ (ราคาจริงอยู่ที่ ${price.toFixed(2)} บ./ลิตร)`;
            statusContainer.style.backgroundColor = 'rgba(16, 185, 129, 0.05)';
            statusContainer.style.borderColor = 'rgba(16, 185, 129, 0.2)';
            icon.className = 'fa-solid fa-circle-check';
            icon.style.color = '#10b981';
        }
    }

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
            
            updateScenarioStatus();
            if (currentFuel === 'trends-th') {
                renderTrendsTH();
            } else {
                renderDashboard(currentFuel);
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            cardsContainer.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding: 40px; color: #ef4444;">Failed to load data. Please ensure you are running this on a web server or GitHub Pages, not directly from file://</div>';
        });
});
