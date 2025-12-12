// 家庭档案管理页面专用JavaScript

// API基础URL
const API_BASE_URL = '/api';

// 初始化家庭管理功能
function initializeFamilyManagement() {
    // 初始化重置按钮功能
    initializeResetButton();
    
    // 初始化搜索功能
    initializeSearchFunctionality();
    
    // 初始化添加家庭按钮功能
    initializeAddFamilyButton();
    
    // 加载家庭数据
    loadFamilies();
}

// 初始化重置按钮
function initializeResetButton() {
    const resetButton = document.getElementById('reset-btn');
    
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            // 重置搜索输入框
            const searchInputs = document.querySelectorAll('input[type="text"]');
            searchInputs.forEach(input => {
                input.value = '';
            });
            
            // 重置后刷新数据
            loadFamilies();
            console.log('搜索已重置');
        });
    }
}

// 初始化搜索功能
function initializeSearchFunctionality() {
    // 监听搜索输入框的按键事件
    const searchInput = document.querySelector('input[type="text"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                // 获取搜索值
                const searchTerm = searchInput.value;
                
                // 构建查询参数
                const params = new URLSearchParams();
                if (searchTerm) params.append('search', searchTerm);
                
                // 加载搜索后的数据
                loadFamilies(params.toString());
            }, 300);
        });
    }
}

// 加载家庭数据
async function loadFamilies(queryParams = '') {
    showLoadingState();
    
    try {
        const response = await fetch(`${API_BASE_URL}/families/?${queryParams}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('加载家庭数据失败');
        }
        
        const data = await response.json();
        renderFamilyCards(data.results);
    } catch (error) {
        console.error('Error loading families:', error);
        showNotification('加载家庭数据失败', 'error');
    } finally {
        hideLoadingState();
    }
}

// 渲染家庭卡片
function renderFamilyCards(families) {
    const container = document.querySelector('.grid.grid-cols-1.md\:grid-cols-2.lg\:grid-cols-3.gap-6');
    if (!container) return;
    
    // 清空容器内容
    container.innerHTML = '';
    
    // 添加家庭卡片
    families.forEach(family => {
        const card = document.createElement('div');
        card.className = 'border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow';
        card.dataset.familyId = family.id;
        
        // 房屋性质文本转换
        const houseTypeMap = {
            1: '自住房',
            2: '出租房',
            3: '空置房'
        };
        const houseTypeText = houseTypeMap[family.house_type] || '未知';
        
        // 房屋性质样式转换
        const houseTypeClassMap = {
            1: 'bg-green-100 text-green-800',
            2: 'bg-blue-100 text-blue-800',
            3: 'bg-yellow-100 text-yellow-800'
        };
        const houseTypeClass = houseTypeClassMap[family.house_type] || 'bg-gray-100 text-gray-800';
        
        card.innerHTML = `
            <div class="bg-primary bg-opacity-10 p-4 border-b border-gray-200">
                <div class="flex items-center justify-between">
                    <h3 class="text-lg font-semibold text-primary">${family.household_number} 家庭</h3>
                    <span class="px-2 py-1 ${houseTypeClass} text-xs font-medium rounded-full">${houseTypeText}</span>
                </div>
                <p class="text-sm text-gray-600 mt-1">户号: ${family.household_number}</p>
            </div>
            <div class="p-6 min-h-[180px]">
                <div class="flex items-start mb-4">
                    <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-primary">
                        <i class="fa fa-home"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-gray-700">住址</p>
                        <p class="text-sm text-gray-500">${family.residential_address || '未填写'}</p>
                    </div>
                </div>
                <div class="flex items-start">
                    <div class="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-success">
                        <i class="fa fa-users"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-gray-700">家庭成员</p>
                        <div class="flex flex-wrap gap-1 mt-1">
                            <!-- 家庭成员信息将通过API获取后动态添加 -->
                            <span class="px-2 py-0.5 bg-blue-50 text-blue-700 text-xs rounded-full">加载中...</span>
                        </div>
                    </div>
                </div>

            </div>
            <div class="bg-gray-50 p-3 border-t border-gray-200 flex justify-end space-x-2">
                <button class="px-3 py-1 text-sm text-gray-600 hover:text-primary focus:outline-none view-btn">
                    <i class="fa fa-eye mr-1"></i> 查看详情
                </button>
                <button class="px-3 py-1 text-sm text-gray-600 hover:text-primary focus:outline-none edit-btn">
                    <i class="fa fa-edit mr-1"></i> 编辑
                </button>
            </div>
        `;
        
        container.appendChild(card);
        
        // 加载家庭成员信息
        loadFamilyMembers(family.id, card);
    });
    
    // 添加空状态
    if (families.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'col-span-full text-center py-12';
        emptyState.innerHTML = `
            <div class="text-gray-400 mb-4">
                <i class="fa fa-home text-4xl"></i>
            </div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">暂无家庭数据</h3>
            <p class="text-sm text-gray-500">请尝试调整搜索条件或添加新家庭</p>
        `;
        container.appendChild(emptyState);
    }
    
    // 初始化卡片按钮事件
    initializeFamilyCardButtons();
}

// 加载家庭成员信息
async function loadFamilyMembers(familyId, card) {
    try {
        const response = await fetch(`${API_BASE_URL}/residents/?family=${familyId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('加载家庭成员失败');
        }
        
        const data = await response.json();
        const membersContainer = card.querySelector('.flex.flex-wrap.gap-1.mt-1');
        
        if (membersContainer) {
            membersContainer.innerHTML = '';
            
            data.results.forEach(member => {
                // 根据性别设置颜色类
                const genderClass = member.gender === 1 ? 'bg-blue-50 text-blue-700' : 'bg-red-50 text-red-700';
                
                const memberSpan = document.createElement('span');
                memberSpan.className = `px-2 py-0.5 ${genderClass} text-xs rounded-full`;
                memberSpan.textContent = member.name;
                membersContainer.appendChild(memberSpan);
            });
            
            if (data.results.length === 0) {
                membersContainer.innerHTML = '<span class="px-2 py-0.5 bg-gray-50 text-gray-700 text-xs rounded-full">暂无家庭成员</span>';
            }
        }
    } catch (error) {
        console.error('Error loading family members:', error);
    }
}

// 初始化家庭卡片按钮事件
function initializeFamilyCardButtons() {
    // 查看详情按钮
    const viewButtons = document.querySelectorAll('.view-btn');
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.border.border-gray-200.rounded-lg');
            const familyId = card.dataset.familyId;
            viewFamilyDetails(familyId);
        });
    });
    
    // 编辑按钮
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.border.border-gray-200.rounded-lg');
            const familyId = card.dataset.familyId;
            editFamily(familyId);
        });
    });
}

// 查看家庭详情
async function viewFamilyDetails(familyId) {
    try {
        const response = await fetch(`${API_BASE_URL}/families/${familyId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('获取家庭详情失败');
        }
        
        const family = await response.json();
        console.log('家庭详情:', family);
        // 这里可以添加查看家庭详情的逻辑，例如打开模态框显示详情
        showNotification('家庭详情已加载', 'info');
    } catch (error) {
        console.error('Error viewing family details:', error);
        showNotification('获取家庭详情失败', 'error');
    }
}

// 编辑家庭
async function editFamily(familyId) {
    try {
        const response = await fetch(`${API_BASE_URL}/families/${familyId}/`, {
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
        
        const family = await response.json();
        console.log('编辑家庭:', family);
        // 这里可以添加编辑家庭的逻辑，例如打开编辑表单
        showNotification('编辑功能开发中', 'info');
    } catch (error) {
        console.error('Error editing family:', error);
        showNotification('获取家庭数据失败', 'error');
    }
}

// 初始化添加家庭按钮功能
function initializeAddFamilyButton() {
    const addButton = document.querySelector('button i.fa-plus').parentElement;
    if (addButton) {
        addButton.addEventListener('click', function() {
            console.log('添加新家庭');
            // 这里可以添加添加新家庭的逻辑，例如打开模态框
            showNotification('添加功能开发中', 'info');
        });
    }
}

// 显示加载状态
function showLoadingState() {
    // 这里可以添加显示加载状态的逻辑
    const cardsContainer = document.querySelector('.grid.grid-cols-1.md\:grid-cols-2.lg\:grid-cols-3.gap-6');
    if (cardsContainer) {
        cardsContainer.style.opacity = '0.5';
    }
    console.log('显示加载状态');
}

// 隐藏加载状态
function hideLoadingState() {
    // 这里可以添加隐藏加载状态的逻辑
    const cardsContainer = document.querySelector('.grid.grid-cols-1.md\:grid-cols-2.lg\:grid-cols-3.gap-6');
    if (cardsContainer) {
        cardsContainer.style.opacity = '1';
    }
    console.log('隐藏加载状态');
}

// 获取CSRF令牌
function getCSRFToken() {
    const csrfTokenElement = document.querySelector('input[name=csrfmiddlewaretoken]');
    return csrfTokenElement ? csrfTokenElement.value : '';
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
    initializeFamilyManagement();
    console.log('家庭档案管理页面已初始化');
});