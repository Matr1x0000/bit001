// 系统设置页面专用JavaScript

// 初始化系统设置功能
function initializeSystemSettings() {
    // 初始化设置选项卡
    initializeSettingsTabs();
    
    // 初始化表单验证
    initializeFormValidation();
    
    // 初始化保存设置按钮
    initializeSaveSettingsButton();
}

// 初始化设置选项卡
function initializeSettingsTabs() {
    const tabs = document.querySelectorAll('ul.flex.flex-wrap.-mb-px li a');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 移除所有激活状态
            tabs.forEach(t => {
                t.classList.remove('border-primary', 'text-primary', 'font-medium');
                t.classList.add('border-transparent', 'hover:text-gray-600', 'hover:border-gray-300', 'text-gray-500');
            });
            
            // 添加当前激活状态
            this.classList.remove('border-transparent', 'hover:text-gray-600', 'hover:border-gray-300', 'text-gray-500');
            this.classList.add('border-primary', 'text-primary', 'font-medium');
            
            // 这里可以添加切换内容的逻辑
            const tabName = this.textContent.trim();
            console.log('切换到设置选项卡:', tabName);
        });
    });
}

// 初始化表单验证
function initializeFormValidation() {
    const form = document.querySelector('form');
    if (form) {
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            if (validateForm(this)) {
                saveSettings();
            }
        });
    }
}

// 验证单个字段
function validateField(field) {
    const fieldName = field.id;
    const value = field.value.trim();
    const errorElement = field.parentElement.querySelector('.text-red-500');
    
    // 清除之前的错误信息
    if (errorElement) {
        errorElement.remove();
    }
    
    // 根据字段类型进行验证
    let isValid = true;
    let errorMessage = '';
    
    switch(fieldName) {
        case 'community-name':
            if (!value) {
                isValid = false;
                errorMessage = '社区名称不能为空';
            }
            break;
        case 'community-address':
            if (!value) {
                isValid = false;
                errorMessage = '社区地址不能为空';
            }
            break;
        case 'contact-phone':
            if (!value) {
                isValid = false;
                errorMessage = '联系电话不能为空';
            } else if (!/^1[3-9]\d{9}$/.test(value)) {
                isValid = false;
                errorMessage = '请输入有效的手机号码';
            }
            break;
        case 'contact-email':
            if (!value) {
                isValid = false;
                errorMessage = '联系邮箱不能为空';
            } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                isValid = false;
                errorMessage = '请输入有效的邮箱地址';
            }
            break;
        case 'max-file-size':
            if (!value) {
                isValid = false;
                errorMessage = '最大文件上传大小不能为空';
            } else if (parseInt(value) < 1 || parseInt(value) > 100) {
                isValid = false;
                errorMessage = '最大文件上传大小必须在1-100MB之间';
            }
            break;
        case 'data-retention':
            if (!value) {
                isValid = false;
                errorMessage = '数据保留期限不能为空';
            } else if (parseInt(value) < 7 || parseInt(value) > 3650) {
                isValid = false;
                errorMessage = '数据保留期限必须在7-3650天之间';
            }
            break;
        default:
            if (field.required && !value) {
                isValid = false;
                errorMessage = '该字段不能为空';
            }
            break;
    }
    
    // 显示错误信息
    if (!isValid) {
        const errorSpan = document.createElement('p');
        errorSpan.className = 'text-red-500 text-xs mt-1';
        errorSpan.textContent = errorMessage;
        field.parentElement.appendChild(errorSpan);
    }
    
    return isValid;
}

// 验证整个表单
function validateForm(form) {
    const inputs = form.querySelectorAll('input, select, textarea');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

// 初始化保存设置按钮
function initializeSaveSettingsButton() {
    const saveButton = document.querySelector('button[type="submit"]');
    if (saveButton) {
        saveButton.addEventListener('click', function(e) {
            e.preventDefault();
            const form = this.closest('form');
            if (validateForm(form)) {
                saveSettings();
            }
        });
    }
}

// 保存设置
function saveSettings() {
    // 获取表单数据
    const formData = new FormData(document.querySelector('form'));
    const settings = {};
    
    for (let [key, value] of formData.entries()) {
        settings[key] = value;
    }
    
    // 获取复选框值
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        settings[checkbox.id] = checkbox.checked;
    });
    
    console.log('保存设置:', settings);
    
    // 显示加载状态
    showLoadingState();
    
    // 模拟API请求
    setTimeout(() => {
        hideLoadingState();
        showNotification('设置已保存', 'success');
    }, 1000);
}

// 显示加载状态
function showLoadingState() {
    const saveButton = document.querySelector('button[type="submit"]');
    if (saveButton) {
        saveButton.disabled = true;
        saveButton.innerHTML = '<i class="fa fa-spinner fa-spin mr-2"></i> 保存中...';
    }
}

// 隐藏加载状态
function hideLoadingState() {
    const saveButton = document.querySelector('button[type="submit"]');
    if (saveButton) {
        saveButton.disabled = false;
        saveButton.innerHTML = '保存设置';
    }
}

// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', function() {
    initializeSystemSettings();
    console.log('系统设置页面已初始化');
});