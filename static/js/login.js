// 登录页面专用JavaScript

// 初始化登录功能
function initializeLogin() {
    // 初始化表单验证
    initializeLoginFormValidation();
    
    // 初始化登录按钮
    initializeLoginButton();
    
    // 初始化键盘事件
    initializeKeyboardEvents();
}

// 初始化登录表单验证
function initializeLoginFormValidation() {
    const form = document.querySelector('form');
    if (form) {
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        
        if (usernameInput) {
            usernameInput.addEventListener('blur', function() {
                validateUsername(this);
            });
        }
        
        if (passwordInput) {
            passwordInput.addEventListener('blur', function() {
                validatePassword(this);
            });
        }
        
        form.addEventListener('submit', function(e) {
            if (!validateLoginForm()) {
                e.preventDefault();
            }
        });
    }
}

// 验证用户名
function validateUsername(input) {
    const value = input.value.trim();
    const errorElement = input.parentElement.querySelector('.text-red-500');
    
    // 清除之前的错误信息
    if (errorElement) {
        errorElement.remove();
    }
    
    let isValid = true;
    let errorMessage = '';
    
    if (!value) {
        isValid = false;
        errorMessage = '用户名不能为空';
    }
    
    // 显示错误信息
    if (!isValid) {
        const errorSpan = document.createElement('p');
        errorSpan.className = 'text-red-500 text-xs mt-1';
        errorSpan.textContent = errorMessage;
        input.parentElement.appendChild(errorSpan);
    }
    
    return isValid;
}

// 验证密码
function validatePassword(input) {
    const value = input.value.trim();
    const errorElement = input.parentElement.querySelector('.text-red-500');
    
    // 清除之前的错误信息
    if (errorElement) {
        errorElement.remove();
    }
    
    let isValid = true;
    let errorMessage = '';
    
    if (!value) {
        isValid = false;
        errorMessage = '密码不能为空';
    } else if (value.length < 6) {
        isValid = false;
        errorMessage = '密码长度不能少于6位';
    }
    
    // 显示错误信息
    if (!isValid) {
        const errorSpan = document.createElement('p');
        errorSpan.className = 'text-red-500 text-xs mt-1';
        errorSpan.textContent = errorMessage;
        input.parentElement.appendChild(errorSpan);
    }
    
    return isValid;
}

// 验证登录表单
function validateLoginForm() {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    const isUsernameValid = validateUsername(usernameInput);
    const isPasswordValid = validatePassword(passwordInput);
    
    return isUsernameValid && isPasswordValid;
}

// 初始化登录按钮
function initializeLoginButton() {
    const loginButton = document.querySelector('button[type="submit"]');
    if (loginButton) {
        loginButton.addEventListener('click', function(e) {
            const isValid = validateLoginForm();
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
}

// 初始化键盘事件
function initializeKeyboardEvents() {
    // 监听回车键
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const loginButton = document.querySelector('button[type="submit"]');
            if (loginButton) {
                loginButton.click();
            }
        }
    });
}

// 显示加载状态
function showLoadingState() {
    const loginButton = document.querySelector('button[type="submit"]');
    if (loginButton) {
        loginButton.disabled = true;
        loginButton.innerHTML = '<i class="fa fa-spinner fa-spin mr-2"></i> 登录中...';
    }
}

// 隐藏加载状态
function hideLoadingState() {
    const loginButton = document.querySelector('button[type="submit"]');
    if (loginButton) {
        loginButton.disabled = false;
        loginButton.innerHTML = '<i class="fa fa-sign-in mr-2"></i> 登录';
    }
}

// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', function() {
    initializeLogin();
    console.log('登录页面已初始化');
    
    // 自动聚焦到用户名输入框
    const usernameInput = document.getElementById('username');
    if (usernameInput) {
        usernameInput.focus();
    }
});