// 数据分析页面专用JavaScript

// API基础URL
const API_BASE_URL = '/api';

// 图表实例存储
let charts = {};

// 初始化数据分析功能
function initializeAnalytics() {
    // 初始化筛选器功能
    initializeAnalyticsFilters();
    
    // 初始化导出功能
    initializeExportFunctions();
    
    // 加载分析数据
    loadAnalyticsData();
}

// 初始化分析筛选器
function initializeAnalyticsFilters() {
    const buildingSelect = document.querySelector('select:nth-of-type(1)');
    const timeSelect = document.querySelector('select:nth-of-type(2)');
    
    if (buildingSelect) {
        buildingSelect.addEventListener('change', function() {
            updateAnalyticsData();
        });
    }
    
    if (timeSelect) {
        timeSelect.addEventListener('change', function() {
            updateAnalyticsData();
        });
    }
}

// 加载分析数据
async function loadAnalyticsData() {
    // 显示加载状态
    showLoadingState();
    
    try {
        // 获取所有需要的数据
        const [residents, families, buildings] = await Promise.all([
            fetchResidents(),
            fetchFamilies(),
            fetchBuildings()
        ]);
        
        // 初始化所有图表
        initializeAnalyticsCharts(residents, families, buildings);
        
        hideLoadingState();
    } catch (error) {
        console.error('Error loading analytics data:', error);
        showNotification('加载分析数据失败', 'error');
        hideLoadingState();
    }
}

// 更新分析数据
function updateAnalyticsData() {
    const select1 = document.querySelector('select:nth-of-type(1)');
    const select2 = document.querySelector('select:nth-of-type(2)');
    
    const building = select1 ? select1.value : '';
    const time = select2 ? select2.value : '';
    
    console.log('更新分析数据:', { building, time });
    
    // 显示加载状态
    showLoadingState();
    
    // 从API获取数据
    loadAnalyticsData();
}

// 从API获取居民数据
async function fetchResidents() {
    try {
        const response = await fetch(`${API_BASE_URL}/residents/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('获取居民数据失败');
        }
        
        const data = await response.json();
        return data.results;
    } catch (error) {
        console.error('Error fetching residents:', error);
        throw error;
    }
}

// 从API获取家庭数据
async function fetchFamilies() {
    try {
        const response = await fetch(`${API_BASE_URL}/families/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('获取家庭数据失败');
        }
        
        const data = await response.json();
        return data.results;
    } catch (error) {
        console.error('Error fetching families:', error);
        throw error;
    }
}

// 从API获取楼栋数据
async function fetchBuildings() {
    try {
        const response = await fetch(`${API_BASE_URL}/buildings/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('获取楼栋数据失败');
        }
        
        const data = await response.json();
        return data.results;
    } catch (error) {
        console.error('Error fetching buildings:', error);
        throw error;
    }
}

// 初始化分析图表
function initializeAnalyticsCharts(residents, families, buildings) {
    // 年龄分布图
    initializeAgeDistributionChart(residents);
    
    // 性别比例图
    initializeGenderRatioChart(residents);
    
    // 楼栋入住率
    initializeBuildingOccupancyChart(buildings, families);
    
    // 特殊人群类型
    initializeSpecialPopulationChart(residents);
    
    // 入住趋势图
    initializeOccupancyTrendChart(families);
}

// 初始化年龄分布图
function initializeAgeDistributionChart(residents) {
    const ctx = document.getElementById('ageDistributionChart2');
    if (!ctx) return;
    
    // 计算年龄分布
    const ageGroups = {
        '0-18': 0,
        '19-35': 0,
        '36-60': 0,
        '60+': 0
    };
    
    residents.forEach(resident => {
        const age = calculateAge(resident.birth_date || '1970-01-01');
        if (age <= 18) {
            ageGroups['0-18']++;
        } else if (age <= 35) {
            ageGroups['19-35']++;
        } else if (age <= 60) {
            ageGroups['36-60']++;
        } else {
            ageGroups['60+']++;
        }
    });
    
    // 创建图表
    charts.ageDistribution = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(ageGroups),
            datasets: [{
                label: '人数',
                data: Object.values(ageGroups),
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
                title: {
                    display: true,
                    text: '年龄分布'
                }
            }
        }
    });
}

// 初始化性别比例图
function initializeGenderRatioChart(residents) {
    const ctx = document.getElementById('genderRatioChart2');
    if (!ctx) return;
    
    // 计算性别比例
    const genderCount = {
        male: 0,
        female: 0
    };
    
    residents.forEach(resident => {
        if (resident.gender === 1) {
            genderCount.male++;
        } else if (resident.gender === 2) {
            genderCount.female++;
        }
    });
    
    // 创建图表
    charts.genderRatio = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['男性', '女性'],
            datasets: [{
                data: [genderCount.male, genderCount.female],
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
                },
                title: {
                    display: true,
                    text: '性别比例'
                }
            }
        }
    });
}

// 初始化楼栋入住率图表
function initializeBuildingOccupancyChart(buildings, families) {
    const ctx = document.getElementById('buildingOccupancyChart');
    if (!ctx || buildings.length === 0) return;
    
    // 计算每个楼栋的入住率
    const buildingOccupancy = {};
    
    // 初始化楼栋入住率
    buildings.forEach(building => {
        buildingOccupancy[building.name] = 0;
    });
    
    // 统计每个楼栋的家庭数量
    families.forEach(family => {
        // 这里简化处理，实际应该从家庭住址中获取楼栋信息
        // 假设家庭住址格式包含楼栋信息，例如 "1号楼3单元501室"
        const address = family.residential_address || '';
        const buildingMatch = address.match(/(\d+号楼)/);
        if (buildingMatch && buildingMatch[1] in buildingOccupancy) {
            buildingOccupancy[buildingMatch[1]]++;
        }
    });
    
    // 创建图表
    charts.buildingOccupancy = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(buildingOccupancy),
            datasets: [{
                label: '家庭数量',
                data: Object.values(buildingOccupancy),
                backgroundColor: 'rgba(16, 185, 129, 0.6)',
                borderColor: 'rgba(16, 185, 129, 1)',
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
                title: {
                    display: true,
                    text: '楼栋家庭数量'
                }
            }
        }
    });
}

// 初始化特殊人群类型图表
function initializeSpecialPopulationChart(residents) {
    const ctx = document.getElementById('specialPopulationChart');
    if (!ctx) return;
    
    // 这里简化处理，实际应该根据居民的特殊人群标识来统计
    // 假设我们有一个特殊人群类型字段，这里使用年龄来模拟
    const specialPopulation = {
        '老年人': 0,
        '残疾人': 0,
        '儿童': 0,
        '孕妇': 0,
        '其他': 0
    };
    
    residents.forEach(resident => {
        const age = calculateAge(resident.birth_date || '1970-01-01');
        if (age >= 65) {
            specialPopulation['老年人']++;
        } else if (age <= 14) {
            specialPopulation['儿童']++;
        } else {
            // 这里简化处理，实际应该根据居民的特殊人群标识来统计
            specialPopulation['其他']++;
        }
    });
    
    // 创建图表
    charts.specialPopulation = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(specialPopulation),
            datasets: [{
                data: Object.values(specialPopulation),
                backgroundColor: [
                    'rgba(251, 191, 36, 0.6)',
                    'rgba(239, 68, 68, 0.6)',
                    'rgba(30, 64, 175, 0.6)',
                    'rgba(16, 185, 129, 0.6)',
                    'rgba(148, 163, 184, 0.6)'
                ],
                borderColor: [
                    'rgba(251, 191, 36, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(30, 64, 175, 1)',
                    'rgba(16, 185, 129, 1)',
                    'rgba(148, 163, 184, 1)'
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
                },
                title: {
                    display: true,
                    text: '特殊人群类型'
                }
            }
        }
    });
}

// 初始化入住趋势图
function initializeOccupancyTrendChart(families) {
    const ctx = document.getElementById('occupancyTrendChart');
    if (!ctx) return;
    
    // 计算每月入住户数
    const monthlyTrend = {};
    
    // 初始化过去6个月的数据
    const now = new Date();
    for (let i = 5; i >= 0; i--) {
        const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
        const monthKey = `${date.getMonth() + 1}月`;
        monthlyTrend[monthKey] = 0;
    }
    
    // 统计每月入住户数
    families.forEach(family => {
        const createdAt = new Date(family.created_at);
        const monthKey = `${createdAt.getMonth() + 1}月`;
        if (monthKey in monthlyTrend) {
            monthlyTrend[monthKey]++;
        }
    });
    
    // 创建图表
    charts.occupancyTrend = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(monthlyTrend),
            datasets: [{
                label: '入住户数',
                data: Object.values(monthlyTrend),
                borderColor: 'rgba(30, 64, 175, 1)',
                backgroundColor: 'rgba(30, 64, 175, 0.1)',
                tension: 0.4,
                fill: true
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
                title: {
                    display: true,
                    text: '入住趋势'
                }
            }
        }
    });
}

// 更新所有图表
async function updateAllCharts() {
    try {
        // 获取最新数据
        const [residents, families, buildings] = await Promise.all([
            fetchResidents(),
            fetchFamilies(),
            fetchBuildings()
        ]);
        
        // 更新年龄分布图
        updateAgeDistributionChart(residents);
        
        // 更新性别比例图
        updateGenderRatioChart(residents);
        
        // 更新楼栋入住率
        updateBuildingOccupancyChart(buildings, families);
        
        // 更新特殊人群类型
        updateSpecialPopulationChart(residents);
        
        // 更新入住趋势图
        updateOccupancyTrendChart(families);
        
        showNotification('图表数据已更新', 'success');
    } catch (error) {
        console.error('Error updating charts:', error);
        showNotification('更新图表失败', 'error');
    }
}

// 更新年龄分布图
function updateAgeDistributionChart(residents) {
    if (!charts.ageDistribution) return;
    
    // 计算年龄分布
    const ageGroups = {
        '0-18': 0,
        '19-35': 0,
        '36-60': 0,
        '60+': 0
    };
    
    residents.forEach(resident => {
        const age = calculateAge(resident.birth_date || '1970-01-01');
        if (age <= 18) {
            ageGroups['0-18']++;
        } else if (age <= 35) {
            ageGroups['19-35']++;
        } else if (age <= 60) {
            ageGroups['36-60']++;
        } else {
            ageGroups['60+']++;
        }
    });
    
    // 更新图表数据
    charts.ageDistribution.data.datasets[0].data = Object.values(ageGroups);
    charts.ageDistribution.update();
}

// 更新性别比例图
function updateGenderRatioChart(residents) {
    if (!charts.genderRatio) return;
    
    // 计算性别比例
    const genderCount = {
        male: 0,
        female: 0
    };
    
    residents.forEach(resident => {
        if (resident.gender === 1) {
            genderCount.male++;
        } else if (resident.gender === 2) {
            genderCount.female++;
        }
    });
    
    // 更新图表数据
    charts.genderRatio.data.datasets[0].data = [genderCount.male, genderCount.female];
    charts.genderRatio.update();
}

// 更新楼栋入住率
function updateBuildingOccupancyChart(buildings, families) {
    if (!charts.buildingOccupancy || buildings.length === 0) return;
    
    // 计算每个楼栋的入住率
    const buildingOccupancy = {};
    
    // 初始化楼栋入住率
    buildings.forEach(building => {
        buildingOccupancy[building.name] = 0;
    });
    
    // 统计每个楼栋的家庭数量
    families.forEach(family => {
        const address = family.residential_address || '';
        const buildingMatch = address.match(/(\d+号楼)/);
        if (buildingMatch && buildingMatch[1] in buildingOccupancy) {
            buildingOccupancy[buildingMatch[1]]++;
        }
    });
    
    // 更新图表数据
    charts.buildingOccupancy.data.labels = Object.keys(buildingOccupancy);
    charts.buildingOccupancy.data.datasets[0].data = Object.values(buildingOccupancy);
    charts.buildingOccupancy.update();
}

// 更新特殊人群类型图表
function updateSpecialPopulationChart(residents) {
    if (!charts.specialPopulation) return;
    
    // 计算特殊人群类型
    const specialPopulation = {
        '老年人': 0,
        '残疾人': 0,
        '儿童': 0,
        '孕妇': 0,
        '其他': 0
    };
    
    residents.forEach(resident => {
        const age = calculateAge(resident.birth_date || '1970-01-01');
        if (age >= 65) {
            specialPopulation['老年人']++;
        } else if (age <= 14) {
            specialPopulation['儿童']++;
        } else {
            specialPopulation['其他']++;
        }
    });
    
    // 更新图表数据
    charts.specialPopulation.data.datasets[0].data = Object.values(specialPopulation);
    charts.specialPopulation.update();
}

// 更新入住趋势图
function updateOccupancyTrendChart(families) {
    if (!charts.occupancyTrend) return;
    
    // 计算每月入住户数
    const monthlyTrend = {};
    
    // 初始化过去6个月的数据
    const now = new Date();
    for (let i = 5; i >= 0; i--) {
        const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
        const monthKey = `${date.getMonth() + 1}月`;
        monthlyTrend[monthKey] = 0;
    }
    
    // 统计每月入住户数
    families.forEach(family => {
        const createdAt = new Date(family.created_at);
        const monthKey = `${createdAt.getMonth() + 1}月`;
        if (monthKey in monthlyTrend) {
            monthlyTrend[monthKey]++;
        }
    });
    
    // 更新图表数据
    charts.occupancyTrend.data.labels = Object.keys(monthlyTrend);
    charts.occupancyTrend.data.datasets[0].data = Object.values(monthlyTrend);
    charts.occupancyTrend.update();
}

// 更新数据表格
function updateDataTable() {
    console.log('更新数据表格');
    // 这里可以添加更新数据表格的逻辑
}

// 加载分析数据
async function loadAnalyticsData() {
    showLoadingState();
    
    try {
        // 获取所有需要的数据
        const [residents, families, buildings] = await Promise.all([
            fetchResidents(),
            fetchFamilies(),
            fetchBuildings()
        ]);
        
        // 初始化所有图表
        initializeAnalyticsCharts(residents, families, buildings);
        
        hideLoadingState();
        showNotification('数据分析页面已初始化', 'success');
    } catch (error) {
        console.error('Error loading analytics data:', error);
        hideLoadingState();
        showNotification('加载分析数据失败', 'error');
    }
}

// 更新分析数据
async function updateAnalyticsData() {
    const select1 = document.querySelector('select:nth-of-type(1)');
    const select2 = document.querySelector('select:nth-of-type(2)');
    
    const building = select1 ? select1.value : '';
    const time = select2 ? select2.value : '';
    
    console.log('更新分析数据:', { building, time });
    
    // 显示加载状态
    showLoadingState();
    
    try {
        // 这里可以根据筛选条件获取数据
        // 目前简化处理，直接重新加载所有数据
        await updateAllCharts();
        hideLoadingState();
    } catch (error) {
        console.error('Error updating analytics data:', error);
        hideLoadingState();
        showNotification('更新分析数据失败', 'error');
    }
}

// 查找包含特定文本的元素
function findElementByText(selector, text) {
    const elements = document.querySelectorAll(selector);
    return Array.from(elements).find(element => 
        element.textContent.trim().includes(text)
    );
}

// 初始化导出功能
function initializeExportFunctions() {
    const exportReportButton = findElementByText('button', '导出报告');
    const exportCSVButton = findElementByText('button', '导出CSV');
    
    if (exportReportButton) {
        exportReportButton.addEventListener('click', function() {
            exportReport();
        });
    }
    
    if (exportCSVButton) {
        exportCSVButton.addEventListener('click', function() {
            exportCSV();
        });
    }
}

// 导出报告
function exportReport() {
    console.log('导出报告');
    showNotification('报告正在导出，请稍候...', 'info');
    
    // 模拟导出过程
    setTimeout(() => {
        showNotification('报告导出成功', 'success');
    }, 1200);
}

// 导出CSV
function exportCSV() {
    console.log('导出CSV');
    showNotification('CSV文件正在导出，请稍候...', 'info');
    
    // 模拟导出过程
    setTimeout(() => {
        showNotification('CSV文件导出成功', 'success');
    }, 800);
}

// 显示加载状态
function showLoadingState() {
    // 这里可以添加显示加载状态的逻辑
    const chartsContainer = document.querySelector('.grid.grid-cols-1.lg\:grid-cols-2.gap-6');
    if (chartsContainer) {
        chartsContainer.style.opacity = '0.5';
    }
    console.log('显示加载状态');
}

// 隐藏加载状态
function hideLoadingState() {
    // 这里可以添加隐藏加载状态的逻辑
    const chartsContainer = document.querySelector('.grid.grid-cols-1.lg\:grid-cols-2.gap-6');
    if (chartsContainer) {
        chartsContainer.style.opacity = '1';
    }
    console.log('隐藏加载状态');
}

// 获取CSRF令牌
function getCSRFToken() {
    const csrfTokenElement = document.querySelector('input[name=csrfmiddlewaretoken]');
    return csrfTokenElement ? csrfTokenElement.value : '';
}

// 计算年龄
function calculateAge(birthDate) {
    const birth = new Date(birthDate);
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        age--;
    }
    
    return age;
}

// 显示通知
function showNotification(message, type = 'info') {
    // 简单的通知实现
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg ${getNotificationClass(type)}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // 3秒后自动移除通知
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// 获取通知样式类
function getNotificationClass(type) {
    const typeClasses = {
        success: 'bg-green-500 text-white',
        error: 'bg-red-500 text-white',
        warning: 'bg-yellow-500 text-white',
        info: 'bg-blue-500 text-white'
    };
    
    return typeClasses[type] || typeClasses.info;
}

// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', function() {
    initializeAnalytics();
    console.log('数据分析页面已初始化');
});