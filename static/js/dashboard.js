// 仪表盘页面专用JavaScript

// 初始化仪表盘图表
function initializeDashboardCharts() {
    // 年龄分布图
    const ageCtx = document.getElementById('ageDistributionChart');
    if (ageCtx) {
        new Chart(ageCtx, {
            type: 'bar',
            data: {
                labels: ['0-18', '19-35', '36-60', '60+'],
                datasets: [{
                    label: '人数',
                    data: [120, 240, 220, 92],
                    backgroundColor: [
                        'rgba(249, 115, 22, 0.6)',
                        'rgba(30, 64, 175, 0.6)',
                        'rgba(16, 185, 129, 0.6)',
                        'rgba(251, 191, 36, 0.6)'
                    ],
                    borderColor: [
                        'rgba(249, 115, 22, 1)',
                        'rgba(30, 64, 175, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(251, 191, 36, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    // 性别比例图
    const genderCtx = document.getElementById('genderRatioChart');
    if (genderCtx) {
        new Chart(genderCtx, {
            type: 'doughnut',
            data: {
                labels: ['男性', '女性'],
                datasets: [{
                    data: [340, 332],
                    backgroundColor: [
                        'rgba(30, 64, 175, 0.6)',
                        'rgba(239, 68, 68, 0.6)'
                    ],
                    borderColor: [
                        'rgba(30, 64, 175, 1)',
                        'rgba(239, 68, 68, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

// 更新仪表盘统计数据
function updateDashboardStats() {
    // 这里可以添加从API获取最新统计数据的逻辑
    console.log('更新仪表盘统计数据');
}

// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', function() {
    initializeDashboardCharts();
    updateDashboardStats();
    
    // 定时更新数据
    setInterval(updateDashboardStats, 30000); // 每30秒更新一次
    
    console.log('仪表盘页面已初始化');
});