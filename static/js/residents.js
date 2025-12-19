// 居民信息管理页面专用JavaScript

// 获取CSRF令牌
function getCSRFToken() {
    // 首先尝试从meta标签获取
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken) {
        return metaToken.getAttribute('content') || '';
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