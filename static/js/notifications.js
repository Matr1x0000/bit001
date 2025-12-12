// 通知发布页面专用JavaScript

// 初始化通知管理功能
function initializeNotificationManagement() {
    // 初始化通知列表功能
    initializeNotificationList();
    
    // 初始化通知详情功能
    initializeNotificationDetails();
    
    // 初始化发布通知按钮功能
    initializePublishNotificationButton();
}

// 初始化通知列表
function initializeNotificationList() {
    const notificationItems = document.querySelectorAll('.border.border-gray-200.rounded-lg');
    
    notificationItems.forEach(item => {
        item.addEventListener('click', function() {
            // 切换选中状态
            notificationItems.forEach(notification => {
                notification.classList.remove('bg-blue-50', 'border-blue-200');
            });
            this.classList.add('bg-blue-50', 'border-blue-200');
            
            // 加载通知详情
            const notificationId = this.dataset.notificationId;
            loadNotificationDetails(notificationId);
        });
    });
    
    // 初始化筛选器
    const filterButtons = document.querySelectorAll('.px-3.py-1.rounded-md.text-sm');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 切换激活状态
            filterButtons.forEach(btn => {
                btn.classList.remove('bg-primary', 'text-white');
                btn.classList.add('border', 'border-gray-300', 'text-gray-500');
            });
            this.classList.remove('border', 'border-gray-300', 'text-gray-500');
            this.classList.add('bg-primary', 'text-white');
            
            // 应用筛选
            const filterType = this.textContent.trim();
            applyNotificationFilter(filterType);
        });
    });
    
    // 自动加载第一个通知的详情
    if (notificationItems.length > 0) {
        notificationItems[0].click();
    }
}

// 加载通知详情
function loadNotificationDetails(notificationId) {
    // 获取当前选中的通知项
    const notificationItem = document.querySelector(`[data-notification-id="${notificationId}"]`);
    if (!notificationItem) return;
    
    // 获取通知数据
    const title = notificationItem.dataset.title;
    const type = notificationItem.dataset.type;
    const content = notificationItem.dataset.content;
    const date = notificationItem.dataset.date;
    const validUntil = notificationItem.dataset.validUntil;
    const total = notificationItem.dataset.total;
    const read = notificationItem.dataset.read;
    const unread = notificationItem.dataset.unread;
    
    // 更新通知详情
    document.getElementById('notification-detail-title').textContent = title;
    
    // 更新通知类型和样式
    const typeElement = document.getElementById('notification-detail-type');
    typeElement.textContent = type;
    // 根据类型更新背景色和文字颜色
    switch(type) {
        case '紧急':
            typeElement.className = 'px-2 py-0.5 bg-red-100 text-red-800 text-xs font-medium rounded-full';
            break;
        case '活动':
            typeElement.className = 'px-2 py-0.5 bg-blue-100 text-blue-800 text-xs font-medium rounded-full';
            break;
        case '普通':
            typeElement.className = 'px-2 py-0.5 bg-green-100 text-green-800 text-xs font-medium rounded-full';
            break;
        default:
            typeElement.className = 'px-2 py-0.5 bg-gray-100 text-gray-800 text-xs font-medium rounded-full';
    }
    
    // 更新通知日期和有效期
    document.getElementById('notification-detail-date').innerHTML = `<i class="fa fa-calendar mr-1"></i> ${date}`;
    document.getElementById('notification-detail-valid').innerHTML = `<i class="fa fa-clock-o mr-1"></i> 有效期至: ${validUntil}`;
    
    // 更新已读按钮样式
    const readButton = document.querySelector('button:contains("已读")');
    if (readButton) {
        if (parseInt(unread) > 0) {
            // 未读状态 - 绿色按钮
            readButton.className = 'px-3 py-1 border border-green-300 bg-green-50 rounded-md text-sm text-green-600 hover:bg-green-100 focus:outline-none flex items-center';
        } else {
            // 已读状态 - 灰色按钮
            readButton.className = 'px-3 py-1 border border-gray-300 bg-gray-50 rounded-md text-sm text-gray-600 hover:bg-gray-100 focus:outline-none flex items-center';
        }
    }
    
    // 更新通知内容
    const contentElement = document.getElementById('notification-detail-content');
    // 将文本内容转换为HTML格式
    let formattedContent = content
        .replace(/\n/g, '<br>')
        .replace(/- (\w+):/g, '<li>$1:</li>')
        .replace(/^- (\w+)/gm, '<li>$1</li>')
        .replace(/^尊敬的各位居民：/gm, '<p>尊敬的各位居民：</p>');
    
    // 处理段落格式
    const paragraphs = formattedContent.split('<br><br>');
    let htmlContent = '';
    
    paragraphs.forEach((paragraph, index) => {
        if (paragraph.includes('<li>')) {
            // 处理列表
            htmlContent += `<ul>${paragraph}</ul>`;
        } else if (paragraph.trim()) {
            // 处理普通段落
            htmlContent += `<p>${paragraph}</p>`;
        }
    });
    
    contentElement.innerHTML = `
        <div class="prose max-w-none">
            ${htmlContent}
        </div>
    `;
    

    
    console.log('通知详情已更新:', notificationId);
}



// 应用通知筛选
function applyNotificationFilter(filterType) {
    console.log('应用通知筛选:', filterType);
    // 这里可以添加应用通知筛选的逻辑
}

// 初始化通知详情
function initializeNotificationDetails() {
    // 初始化已读按钮
    const readButton = document.querySelector('button:contains("已读")');
    if (readButton) {
        readButton.addEventListener('click', function() {
            console.log('标记为已读');
            // 这里可以添加标记为已读的逻辑
            showNotification('通知已标记为已读', 'success');
        });
    }
    
    // 初始化删除按钮
    const deleteButton = document.querySelector('button:contains("删除")');
    if (deleteButton) {
        deleteButton.addEventListener('click', function() {
            if (confirm('确定要删除该通知吗？')) {
                console.log('删除通知');
                showNotification('通知已删除', 'success');
            }
        });
    }
    

}

// 初始化发布通知按钮
function initializePublishNotificationButton() {
    const publishButton = document.querySelector('button:contains("发布通知")');
    if (publishButton) {
        publishButton.addEventListener('click', function() {
            console.log('发布新通知');
            // 这里可以添加发布新通知的逻辑
        });
    }
}



// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', function() {
    initializeNotificationManagement();
    console.log('通知发布页面已初始化');
});