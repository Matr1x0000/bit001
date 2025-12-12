// 居民信息管理页面专用JavaScript

// API基础URL
const API_BASE_URL = '/api';

// 初始化居民管理功能
function initializeResidentManagement() {
    // 初始化筛选器功能
    initializeResidentFilters();
    
    // 初始化添加居民按钮功能
    initializeAddResidentButton();
    
    // 加载居民数据
    loadResidents();
}

// 初始化居民筛选器
function initializeResidentFilters() {
    const resetButton = document.querySelector('button i.fa-refresh').parentElement;
    
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            // 重置所有筛选器
            const selects = document.querySelectorAll('select');
            selects.forEach(select => {
                select.value = '';
            });
            const searchInputs = document.querySelectorAll('input[type="text"]');
            searchInputs.forEach(input => {
                input.value = '';
            });
            
            // 重置后刷新数据
            loadResidents();
            console.log('筛选器已重置');
        });
    }
    
    // 监听筛选器变化
    const filters = document.querySelectorAll('select, input[type="text"]');
    filters.forEach(filter => {
        filter.addEventListener('change', function() {
            applyResidentFilters();
        });
    });
    
    // 监听搜索输入框的按键事件
    const searchInput = document.querySelector('input[type="text"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(applyResidentFilters, 300);
        });
    }
}

// 应用居民筛选器
function applyResidentFilters() {
    // 获取所有筛选器的值
    const ageGroup = document.querySelector('select:nth-of-type(1)').value;
    const politicalStatus = document.querySelector('select:nth-of-type(2)').value;
    const education = document.querySelector('select:nth-of-type(3)').value;
    const nationality = document.querySelector('select:nth-of-type(4)').value;
    const searchTerm = document.querySelector('input[type="text"]').value;
    
    // 构建查询参数
    const params = new URLSearchParams();
    if (ageGroup) params.append('age_group', ageGroup);
    if (politicalStatus) params.append('political_status', politicalStatus);
    if (education) params.append('education', education);
    if (nationality) params.append('nationality', nationality);
    if (searchTerm) params.append('search', searchTerm);
    
    // 加载筛选后的数据
    loadResidents(params.toString());
}

// 加载居民数据
async function loadResidents(queryParams = '') {
    showLoadingState();
    
    try {
        const response = await fetch(`${API_BASE_URL}/residents/?${queryParams}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('加载居民数据失败');
        }
        
        const data = await response.json();
        renderResidentTable(data.results);
    } catch (error) {
        console.error('Error loading residents:', error);
        showNotification('加载居民数据失败', 'error');
    } finally {
        hideLoadingState();
    }
}

// 渲染居民表格
function renderResidentTable(residents) {
    const tbody = document.querySelector('tbody');
    if (!tbody) return;
    
    // 清空表格内容
    tbody.innerHTML = '';
    
    // 添加居民数据行
    residents.forEach(resident => {
        const row = document.createElement('tr');
        row.dataset.id = resident.id;
        
        // 性别显示转换
        const genderText = resident.gender === 1 ? '男' : '女';
        
        // 民族转换
        const nationalityMap = {
            1: '汉族', 2: '蒙古族', 3: '回族', 4: '藏族', 5: '维吾尔族', 6: '苗族', 7: '彝族', 8: '壮族',
            9: '布依族', 10: '朝鲜族', 11: '满族', 12: '侗族', 13: '瑶族', 14: '白族', 15: '土家族', 16: '哈尼族',
            17: '哈萨克族', 18: '傣族', 19: '黎族', 20: '傈僳族', 21: '佤族', 22: '畲族', 23: '高山族', 24: '拉祜族',
            25: '水族', 26: '东乡族', 27: '纳西族', 28: '景颇族', 29: '柯尔克孜族', 30: '土族',
            31: '达斡尔族', 32: '仫佬族', 33: '羌族', 34: '布朗族', 35: '撒拉族', 36: '毛难族', 37: '仡佬族', 38: '锡伯族',
            39: '阿昌族', 40: '普米族', 41: '塔吉克族', 42: '怒族', 43: '乌孜别克族', 44: '俄罗斯族', 45: '鄂温克族',
            46: '崩龙族', 47: '保安族', 48: '裕固族', 49: '京族', 50: '塔塔尔族', 51: '独龙族', 52: '鄂伦春族',
            53: '赫哲族', 54: '门巴族', 55: '珞巴族', 56: '基诺族', 57: '其他'
        };
        const nationalityText = nationalityMap[resident.nationality] || '未知';
        
        // 政治面貌转换
        const politicalStatusMap = {
            1: '中国共产党党员',
            2: '中国共产党预备党员',
            3: '中国共产主义青年团团员',
            4: '中国国民党革命委员会党员',
            5: '中国民主同盟盟员',
            6: '中国民主建国会会员',
            7: '中国民主促进会会员',
            8: '中国农工民主党党员',
            9: '中国致公党党员',
            10: '九三学社社员',
            11: '台湾民主自治同盟盟员',
            12: '无党派民主人士',
            13: '群众'
        };
        const politicalStatusText = politicalStatusMap[resident.political_status] || '未知';
        
        row.innerHTML = `
            <td class="px-4 py-3 whitespace-nowrap">
                <input type="checkbox" class="rounded text-primary focus:ring-primary">
            </td>
            <td class="px-4 py-3 whitespace-nowrap">
                <div>
                    <p class="text-sm font-medium text-gray-900">${resident.name}</p>
                </div>
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${genderText}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${nationalityText}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${resident.id_card}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${resident.phone}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">${resident.residential_address || '未填写'}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm font-medium">
                <a href="#" class="text-primary hover:text-blue-700 mr-3 view-btn">查看</a>
                <a href="#" class="text-gray-600 hover:text-gray-900 mr-3 edit-btn">编辑</a>
                <a href="#" class="text-red-600 hover:text-red-900 delete-btn">删除</a>
            </td>
        `;
        
        tbody.appendChild(row);
    });
    
    // 初始化表格操作按钮事件
    initializeTableButtons();
    
    // 初始化复选框事件
    initializeCheckboxEvents();
}

// 初始化表格操作按钮
function initializeTableButtons() {
    // 查看按钮事件
    const viewButtons = document.querySelectorAll('.view-btn');
    viewButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const residentId = this.closest('tr').dataset.id;
            viewResidentDetails(residentId);
        });
    });
    
    // 编辑按钮事件
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const residentId = this.closest('tr').dataset.id;
            editResident(residentId);
        });
    });
    
    // 删除按钮事件
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const residentId = this.closest('tr').dataset.id;
            deleteResident(residentId);
        });
    });
}

// 初始化复选框事件
function initializeCheckboxEvents() {
    const checkboxes = document.querySelectorAll('tbody input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateSelectedCount();
        });
    });
    
    // 全选功能
    const selectAllCheckbox = document.querySelector('thead input[type="checkbox"]');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const tbodyCheckboxes = document.querySelectorAll('tbody input[type="checkbox"]');
            tbodyCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateSelectedCount();
        });
    }
}

// 更新已选择居民数量
function updateSelectedCount() {
    const checkedCheckboxes = document.querySelectorAll('tbody input[type="checkbox"]:checked');
    const count = checkedCheckboxes.length;
    console.log('已选择', count, '名居民');
    // 这里可以添加更新已选择数量的逻辑
}

// 查看居民详情
async function viewResidentDetails(residentId) {
    try {
        const response = await fetch(`${API_BASE_URL}/residents/${residentId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('获取居民详情失败');
        }
        
        const resident = await response.json();
        console.log('居民详情:', resident);
        // 调用main.js中的viewResidentDetail函数显示详情
        window.viewResidentDetail(residentId);
    } catch (error) {
        console.error('Error viewing resident details:', error);
        showNotification('获取居民详情失败', 'error');
    }
}

// 编辑居民
async function editResident(residentId) {
    // 调用main.js中的编辑居民函数
    window.editResident(residentId);
}

// 删除居民
async function deleteResident(residentId) {
    if (confirm('确定要删除该居民吗？')) {
        try {
            const response = await fetch(`${API_BASE_URL}/residents/${residentId}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                throw new Error('删除居民失败');
            }
            
            console.log('居民已删除:', residentId);
            // 重新加载居民数据
            loadResidents();
            showNotification('居民已删除', 'success');
        } catch (error) {
            console.error('Error deleting resident:', error);
            showNotification('删除居民失败', 'error');
        }
    }
}

// 初始化添加居民按钮
function initializeAddResidentButton() {
    const addButton = document.querySelector('button i.fa-plus').parentElement;
    if (addButton) {
        addButton.addEventListener('click', function() {
            console.log('添加新居民');
            // 这里可以添加添加新居民的逻辑，例如打开模态框
            showNotification('添加功能开发中', 'info');
        });
    }
}

// 显示加载状态
function showLoadingState() {
    // 这里可以添加显示加载状态的逻辑
    const tableContainer = document.querySelector('.overflow-x-auto');
    if (tableContainer) {
        tableContainer.style.opacity = '0.5';
    }
    console.log('显示加载状态');
}

// 隐藏加载状态
function hideLoadingState() {
    // 这里可以添加隐藏加载状态的逻辑
    const tableContainer = document.querySelector('.overflow-x-auto');
    if (tableContainer) {
        tableContainer.style.opacity = '1';
    }
    console.log('隐藏加载状态');
}



// 获取CSRF令牌
function getCSRFToken() {
    // 首先尝试从meta标签获取
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken) {
        return metaToken.getAttribute('content');
    }
    
    // 然后尝试从表单输入获取
    const formToken = document.querySelector('input[name=csrfmiddlewaretoken]');
    return formToken ? formToken.value : '';
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

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
}

// 显示通知
function showNotification(message, type = 'info') {
    // 这里可以添加显示通知的逻辑
    console.log(`${type.toUpperCase()}: ${message}`);
    
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
    initializeResidentManagement();
    console.log('居民信息管理页面已初始化');
});