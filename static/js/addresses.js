// 地址管理页面专用JavaScript

// 初始化地址管理功能
function initializeAddressManagement() {
    // 初始化筛选器功能
    initializeAddressFilters();
    
    // 初始化地址列表功能
    initializeAddressList();
    
    // 初始化添加地址按钮
    initializeAddAddressButton();
}

// 初始化地址筛选器
function initializeAddressFilters() {
    const searchInput = document.querySelector('input[type="text"]');
    const selectElements = document.querySelectorAll('select');
    const filterButton = document.querySelector('button:contains("筛选")');
    const resetButton = document.querySelector('button:contains("重置")');
    
    // 搜索输入框事件监听
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(applyAddressFilters, 300);
        });
    }
    
    // 下拉选择框事件监听
    selectElements.forEach(select => {
        select.addEventListener('change', function() {
            applyAddressFilters();
        });
    });
    
    // 筛选按钮事件监听
    if (filterButton) {
        filterButton.addEventListener('click', function() {
            applyAddressFilters();
        });
    }
    
    // 重置按钮事件监听
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            resetAddressFilters();
        });
    }
}

// 应用地址筛选器
function applyAddressFilters() {
    const searchTerm = document.querySelector('input[type="text"]').value;
    const community = document.querySelector('select:nth-of-type(1)').value;
    const building = document.querySelector('select:nth-of-type(2)').value;
    const unit = document.querySelector('select:nth-of-type(3)').value;
    
    console.log('应用地址筛选器:', { searchTerm, community, building, unit });
    
    // 显示加载状态
    showLoadingState();
    
    // 模拟API请求
    setTimeout(() => {
        hideLoadingState();
        // 这里可以添加更新地址列表的逻辑
    }, 500);
}

// 重置地址筛选器
function resetAddressFilters() {
    const searchInput = document.querySelector('input[type="text"]');
    const selectElements = document.querySelectorAll('select');
    
    if (searchInput) {
        searchInput.value = '';
    }
    
    selectElements.forEach(select => {
        select.value = '';
    });
    
    console.log('重置地址筛选器');
    
    // 显示加载状态
    showLoadingState();
    
    // 模拟API请求
    setTimeout(() => {
        hideLoadingState();
        // 这里可以添加更新地址列表的逻辑
    }, 500);
}

// 初始化地址列表
function initializeAddressList() {
    const addressRows = document.querySelectorAll('tbody tr');
    
    addressRows.forEach(row => {
        // 查看按钮事件监听
        const viewButton = row.querySelector('a:contains("查看")');
        if (viewButton) {
            viewButton.addEventListener('click', function(e) {
                e.preventDefault();
                viewAddressDetails(row);
            });
        }
        
        // 编辑按钮事件监听
        const editButton = row.querySelector('a:contains("编辑")');
        if (editButton) {
            editButton.addEventListener('click', function(e) {
                e.preventDefault();
                editAddress(row);
            });
        }
        
        // 删除按钮事件监听
        const deleteButton = row.querySelector('a:contains("删除")');
        if (deleteButton) {
            deleteButton.addEventListener('click', function(e) {
                e.preventDefault();
                deleteAddress(row);
            });
        }
        
        // 复选框事件监听
        const checkbox = row.querySelector('input[type="checkbox"]');
        if (checkbox) {
            checkbox.addEventListener('change', function() {
                updateSelectedAddresses();
            });
        }
    });
    
    // 全选复选框事件监听
    const selectAllCheckbox = document.querySelector('thead input[type="checkbox"]');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            toggleSelectAllAddresses(this.checked);
        });
    }
}

// 查看地址详情
function viewAddressDetails(row) {
    // 这里可以添加查看地址详情的逻辑
    console.log('查看地址详情');
    showNotification('查看地址详情功能开发中', 'info');
}

// 编辑地址
function editAddress(row) {
    // 这里可以添加编辑地址的逻辑
    console.log('编辑地址');
    showNotification('编辑地址功能开发中', 'info');
}

// 删除地址
function deleteAddress(row) {
    showConfirmModal('确认删除', '确定要删除该地址吗？', function(confirmed) {
        if (confirmed) {
            // 这里可以添加删除地址的逻辑
            console.log('删除地址');
            row.remove();
            updateSelectedAddresses();
            showNotification('地址已删除', 'success');
        }
    });
}

// 更新已选择的地址数量
function updateSelectedAddresses() {
    const checkedCheckboxes = document.querySelectorAll('tbody input[type="checkbox"]:checked');
    const count = checkedCheckboxes.length;
    console.log('已选择', count, '个地址');
    // 这里可以添加更新已选择地址数量的逻辑
}

// 全选/取消全选地址
function toggleSelectAllAddresses(checked) {
    const checkboxes = document.querySelectorAll('tbody input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = checked;
    });
    updateSelectedAddresses();
}

// 初始化添加地址按钮
function initializeAddAddressButton() {
    const addButton = document.querySelector('button:contains("添加地址")');
    if (addButton) {
        addButton.addEventListener('click', function() {
            // 这里可以添加添加地址的逻辑
            console.log('添加新地址');
            showNotification('添加地址功能开发中', 'info');
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
    initializeAddressManagement();
    console.log('地址管理页面已初始化');
});