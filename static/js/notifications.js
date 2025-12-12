// 通知发布页面专用JavaScript

// 初始化通知管理功能
function initializeNotificationManagement() {
    // 初始化通知列表功能
    initializeNotificationList();
    
    // 初始化通知详情功能
    initializeNotificationDetails();
    
    // 初始化发布通知按钮功能
    initializePublishNotificationButton();
    
    // 初始化筛选功能
    initializeNotificationFilter();
    
    // 初始化搜索功能
    initializeNotificationSearch();
}

// 初始化筛选功能
function initializeNotificationFilter() {
    console.log('初始化筛选功能');
    
    // 从URL获取当前筛选条件
    const urlParams = new URLSearchParams(window.location.search);
    const currentType = urlParams.get('notification_type');
    
    // 获取筛选按钮
    const filterContainer = document.querySelector('.flex.flex-wrap.items-center.justify-between.gap-4.mb-6');
    if (!filterContainer) {
        console.error('未找到筛选容器');
        return;
    }
    
    const filterButtons = filterContainer.querySelectorAll('button');
    console.log('找到筛选按钮数量:', filterButtons.length);
    
    // 映射类型文本到类型值
    const typeMap = {
        '全部': '',
        '紧急': '1',
        '普通': '2',
        '活动': '3'
    };
    
    // 反向映射，用于设置当前选中状态
    const reverseTypeMap = {
        '': '全部',
        '1': '紧急',
        '2': '普通',
        '3': '活动'
    };
    
    // 设置当前选中的筛选按钮
    const currentTypeText = reverseTypeMap[currentType || ''];
    
    filterButtons.forEach(button => {
        const buttonText = button.textContent.trim();
        // 只处理筛选按钮（全部、紧急、普通、活动）
        if (['全部', '紧急', '普通', '活动'].includes(buttonText)) {
            // 设置初始选中状态
            if (buttonText === currentTypeText) {
                button.classList.add('bg-primary', 'text-white');
                button.classList.remove('border', 'border-gray-300', 'bg-gray-50', 'text-gray-500');
            } else {
                button.classList.remove('bg-primary', 'text-white');
                button.classList.add('border', 'border-gray-300', 'bg-gray-50', 'text-gray-500');
            }
            
            button.addEventListener('click', function() {
                console.log('筛选按钮点击:', buttonText);
                // 获取对应的类型值
                const typeValue = typeMap[buttonText];
                
                // 更新URL参数
                const newUrlParams = new URLSearchParams(window.location.search);
                if (typeValue) {
                    newUrlParams.set('notification_type', typeValue);
                } else {
                    newUrlParams.delete('notification_type');
                }
                // 重置到第一页
                newUrlParams.set('page', '1');
                
                // 重新加载页面
                const newUrl = `${window.location.pathname}?${newUrlParams.toString()}`;
                window.location.href = newUrl;
            });
        }
    });
}

// 初始化搜索功能
function initializeNotificationSearch() {
    console.log('初始化搜索功能');
    
    // 获取搜索输入框
    const searchInput = document.querySelector('input[placeholder="搜索通知..."]');
    if (!searchInput) {
        console.error('未找到搜索输入框');
        return;
    }
    
    // 从URL获取当前搜索关键词，设置到输入框中
    const urlParams = new URLSearchParams(window.location.search);
    const currentSearch = urlParams.get('search_query');
    if (currentSearch) {
        searchInput.value = currentSearch;
    }
    
    // 添加事件监听器，处理搜索操作
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            console.log('搜索回车触发');
            // 获取搜索关键词
            const searchQuery = this.value.trim();
            
            // 更新URL参数
            const newUrlParams = new URLSearchParams(window.location.search);
            if (searchQuery) {
                newUrlParams.set('search_query', searchQuery);
            } else {
                newUrlParams.delete('search_query');
            }
            // 重置到第一页
            newUrlParams.set('page', '1');
            
            // 重新加载页面
            const newUrl = `${window.location.pathname}?${newUrlParams.toString()}`;
            window.location.href = newUrl;
        }
    });
    
    // 添加搜索按钮事件监听器（如果有）
    const searchButton = searchInput.parentElement.querySelector('button');
    if (searchButton) {
        searchButton.addEventListener('click', function() {
            console.log('搜索按钮点击触发');
            // 获取搜索关键词
            const searchQuery = searchInput.value.trim();
            
            // 更新URL参数
            const newUrlParams = new URLSearchParams(window.location.search);
            if (searchQuery) {
                newUrlParams.set('search_query', searchQuery);
            } else {
                newUrlParams.delete('search_query');
            }
            // 重置到第一页
            newUrlParams.set('page', '1');
            
            // 重新加载页面
            const newUrl = `${window.location.pathname}?${newUrlParams.toString()}`;
            window.location.href = newUrl;
        });
    }
}

// 初始化通知列表
function initializeNotificationList() {
    // 直接选择带有data-notification-id属性的元素，确保只选择左侧的通知列表项
    const notificationItems = document.querySelectorAll('[data-notification-id]');
    
    console.log('找到的通知列表项数量:', notificationItems.length);
    
    notificationItems.forEach(item => {
        item.addEventListener('click', function() {
            console.log('点击了通知列表项:', this.dataset.notificationId);
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
    
    // 自动加载第一个通知的详情
    if (notificationItems.length > 0) {
        console.log('自动加载第一个通知详情:', notificationItems[0].dataset.notificationId);
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
    const publisher = notificationItem.dataset.publisher;
    const total = notificationItem.dataset.total;
    const read = notificationItem.dataset.read;
    const unread = notificationItem.dataset.unread;
    const remark = notificationItem.dataset.remark;
    
    // 更新通知详情
    document.getElementById('notification-detail-title').textContent = title;
    
    // 更新通知类型和样式
    const typeElement = document.getElementById('notification-detail-type');
    typeElement.textContent = type;
    // 根据类型更新背景色和文字颜色
    switch(type) {
        case '紧急':
            typeElement.className = 'px-2 py-0.5 bg-red-500 text-white text-xs font-medium rounded-full shadow-sm';
            break;
        case '活动':
            typeElement.className = 'px-2 py-0.5 bg-blue-500 text-white text-xs font-medium rounded-full shadow-sm';
            break;
        case '普通':
            typeElement.className = 'px-2 py-0.5 bg-green-500 text-white text-xs font-medium rounded-full shadow-sm';
            break;
        default:
            typeElement.className = 'px-2 py-0.5 bg-gray-500 text-white text-xs font-medium rounded-full shadow-sm';
    }
    
    // 更新通知发布人、日期和有效期
    document.getElementById('notification-detail-author').innerHTML = `<i class="fa fa-user mr-1"></i> ${publisher}`;
    document.getElementById('notification-detail-date').innerHTML = `<i class="fa fa-calendar mr-1"></i> ${date}`;
    document.getElementById('notification-detail-valid').innerHTML = `<i class="fa fa-clock-o mr-1"></i> 有效期至: ${validUntil}`;
    
    // 更新已读按钮样式和数据属性
    const allButtons = document.querySelectorAll('button');
    let readButton = null;
    
    allButtons.forEach(button => {
        const buttonText = button.textContent.trim();
        if ((buttonText.includes('已读') || buttonText.includes('未读')) && 
            (button.outerHTML.includes('fa-check') || button.outerHTML.includes('fa-times'))) {
            readButton = button;
        }
    });
    
    if (readButton) {
        console.log('找到已读/未读按钮，更新状态:', readButton);
        // 从数据属性获取是否已读
        const isRead = notificationItem.dataset.isRead === 'true';
        
        // 为按钮添加必要的数据属性
        readButton.dataset.notificationId = notificationId;
        readButton.dataset.isRead = isRead;
        
        // 更新按钮状态
        updateReadButtonStatus(readButton, isRead, notificationId);
        
        // 调用API检查最新的已读状态，确保数据准确性
        checkNotificationReadStatus(notificationId, readButton);
    } else {
        console.log('未找到已读/未读按钮');
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
    
    // 更新备注信息
    const remarkElement = document.getElementById('notification-detail-remark');
    if (remark && remark.trim()) {
        remarkElement.textContent = remark;
    } else {
        remarkElement.textContent = '无备注';
    }
    
    // 加载通知附件
    loadNotificationAttachments(notificationId);
    
    console.log('通知详情已更新:', notificationId);
}

// 加载通知附件
function loadNotificationAttachments(notificationId) {
    const attachmentsList = document.getElementById('attachments-list');
    
    // 显示加载状态
    attachmentsList.innerHTML = '<div class="text-gray-500 flex items-center"><i class="fa fa-spinner fa-spin mr-2"></i> 加载附件中...</div>';
    
    // 从API获取附件列表
    fetch(`/api/notification-attachments/?notification=${notificationId}`)
        .then(response => {
            console.log('附件API响应状态:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('附件数据:', data);
            if (data.results && Array.isArray(data.results)) {
                // 如果返回的是分页数据
                const attachments = data.results;
                if (attachments.length > 0) {
                    // 生成附件列表
                    let html = '';
                    attachments.forEach(attachment => {
                        html += `
                            <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                                <div class="flex items-center gap-3">
                                    <i class="fa fa-file text-gray-500 text-lg"></i>
                                    <div>
                                        <div class="text-sm font-medium text-gray-900 truncate max-w-xs">${attachment.filename}</div>
                                        <div class="text-xs text-gray-500 mt-1">
                                            <span class="mr-4">${formatFileSize(attachment.file_size)}</span>
                                            <span>${formatDate(attachment.upload_time)}</span>
                                        </div>
                                    </div>
                                </div>
                                <a href="${attachment.file}" download="${attachment.filename}" 
                                   class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-primary flex items-center gap-2 text-sm">
                                    <i class="fa fa-download"></i>
                                    <span>下载</span>
                                </a>
                            </div>
                        `;
                    });
                    attachmentsList.innerHTML = html;
                } else {
                    // 无附件
                    attachmentsList.innerHTML = '<div class="text-gray-500">无附件</div>';
                }
            } else if (Array.isArray(data)) {
                // 如果直接返回数组
                if (data.length > 0) {
                    // 生成附件列表
                    let html = '';
                    data.forEach(attachment => {
                        html += `
                            <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                                <div class="flex items-center gap-3">
                                    <i class="fa fa-file text-gray-500 text-lg"></i>
                                    <div>
                                        <div class="text-sm font-medium text-gray-900 truncate max-w-xs">${attachment.filename}</div>
                                        <div class="text-xs text-gray-500 mt-1">
                                            <span class="mr-4">${formatFileSize(attachment.file_size)}</span>
                                            <span>${formatDate(attachment.upload_time)}</span>
                                        </div>
                                    </div>
                                </div>
                                <a href="${attachment.file}" download="${attachment.filename}" 
                                   class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-primary flex items-center gap-2 text-sm">
                                    <i class="fa fa-download"></i>
                                    <span>下载</span>
                                </a>
                            </div>
                        `;
                    });
                    attachmentsList.innerHTML = html;
                } else {
                    // 无附件
                    attachmentsList.innerHTML = '<div class="text-gray-500">无附件</div>';
                }
            } else {
                console.error('无效的附件数据格式:', data);
                attachmentsList.innerHTML = '<div class="text-red-500 flex items-center"><i class="fa fa-exclamation-circle mr-2"></i> 附件数据格式错误</div>';
            }
        })
        .catch(error => {
            console.error('加载附件失败:', error);
            attachmentsList.innerHTML = '<div class="text-red-500 flex items-center"><i class="fa fa-exclamation-circle mr-2"></i> 加载附件失败</div>';
        });
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}





// 检查并更新通知已读状态
async function checkNotificationReadStatus(notificationId, button) {
    try {
        // 显示加载状态
        button.innerHTML = '<i class="fa fa-spinner fa-spin mr-1"></i> 检查中...';
        button.disabled = true;
        
        // 调用API检查通知已读状态
        const response = await fetch(`/api/notification-read-status/${notificationId}/`);
        const data = await response.json();
        
        if (data.success) {
            updateReadButtonStatus(button, data.is_read, notificationId);
        } else {
            console.error('检查通知已读状态失败:', data.message);
            showNotification('检查通知状态失败', 'error');
        }
    } catch (error) {
        console.error('检查通知已读状态时发生错误:', error);
        showNotification('网络错误，请稍后重试', 'error');
    } finally {
        button.disabled = false;
    }
}

// 更新已读按钮状态
function updateReadButtonStatus(button, isRead, notificationId) {
    if (isRead) {
        // 已读状态
        button.className = 'px-3 py-1 border border-green-300 bg-green-50 rounded-md text-sm text-green-600 hover:bg-green-100 focus:outline-none flex items-center';
        button.innerHTML = '<i class="fa fa-check-circle mr-1"></i> 已读';
    } else {
        // 未读状态
        button.className = 'px-3 py-1 border border-red-300 bg-red-50 rounded-md text-sm text-red-600 hover:bg-red-100 focus:outline-none flex items-center';
        button.innerHTML = '<i class="fa fa-times-circle mr-1"></i> 未读';
    }
    
    // 更新按钮的data属性
    button.dataset.isRead = isRead;
    button.dataset.notificationId = notificationId;
}

// 切换通知已读状态
async function toggleNotificationReadStatus(button) {
    const notificationId = button.dataset.notificationId;
    const currentIsRead = button.dataset.isRead === 'true';
    
    // 如果已经是已读状态，不执行任何操作
    if (currentIsRead) {
        // 添加视觉反馈，提示用户该通知已读
        button.classList.add('opacity-75', 'cursor-not-allowed');
        setTimeout(() => {
            button.classList.remove('opacity-75', 'cursor-not-allowed');
        }, 500);
        showNotification('该通知已读，无需重复操作', 'info');
        return;
    }
    
    try {
        // 显示加载状态
        button.innerHTML = '<i class="fa fa-spinner fa-spin mr-1"></i> 更新中...';
        button.disabled = true;
        
        // 调用API更新通知已读状态，只处理未读→已读的情况
        const response = await fetch(`/api/notification-read-status/${notificationId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: 'action=read'
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 更新按钮状态
            updateReadButtonStatus(button, true, notificationId);
            showNotification(data.message, 'success');
            
            // 更新列表中对应通知的阅读状态
            const notificationItem = document.querySelector(`[data-notification-id="${notificationId}"]`);
            if (notificationItem) {
                // 更新通知项的data-is-read属性
                notificationItem.dataset.isRead = 'true';
                
                // 更新通知项中的阅读状态显示
                const statusElement = notificationItem.querySelector('.text-green-600, .text-red-600');
                if (statusElement) {
                    statusElement.className = 'text-green-600';
                    statusElement.innerHTML = '<i class="fa fa-check-circle mr-1"></i> 已读';
                }
                
                // 更新通知项的view_count
                const viewCountElement = notificationItem.querySelector('.fa-eye').nextSibling;
                if (viewCountElement) {
                    // 移除空格并转换为数字
                    const currentViewCount = parseInt(viewCountElement.textContent.trim());
                    viewCountElement.textContent = ` ${currentViewCount + 1}`;
                }
            }
            
            // 刷新页面
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            console.error('更新通知已读状态失败:', data.message);
            showNotification('更新通知状态失败', 'error');
            // 恢复按钮原始状态
            updateReadButtonStatus(button, false, notificationId);
        }
    } catch (error) {
        console.error('更新通知已读状态时发生错误:', error);
        showNotification('网络错误，请稍后重试', 'error');
        // 恢复按钮原始状态
        updateReadButtonStatus(button, false, notificationId);
    } finally {
        button.disabled = false;
    }
}

// 初始化通知详情
function initializeNotificationDetails() {
    console.log('开始初始化通知详情');
    
    // 添加一个直接的事件监听器到详情面板区域，确保能捕获按钮点击
    const detailPanel = document.querySelector('.lg\\:col-span-2 .bg-white');
    if (detailPanel) {
        detailPanel.addEventListener('click', function(e) {
            const target = e.target.closest('button');
            if (target) {
                const buttonText = target.textContent.trim();
                
                if (buttonText.includes('已读') || buttonText.includes('未读')) {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('详情面板监听器捕获到已读/未读按钮点击:', target);
                    
                    // 确保按钮有正确的数据属性
                    const selectedItem = document.querySelector('.bg-blue-50.border-blue-200');
                    if (selectedItem) {
                        const notificationId = selectedItem.dataset.notificationId;
                        const isRead = selectedItem.dataset.isRead === 'true';
                        
                        target.dataset.notificationId = notificationId;
                        target.dataset.isRead = isRead;
                        console.log('已为按钮添加数据属性:', notificationId, isRead);
                        
                        toggleNotificationReadStatus(target);
                    } else {
                        console.error('未找到选中的通知项，无法获取通知ID');
                        showNotification('请先选择一个通知', 'error');
                    }
                }
            }
        });
    }
    
    // 直接查找所有按钮，通过文字内容和图标来判断
    const allButtons = document.querySelectorAll('button');
    console.log('找到所有按钮数量:', allButtons.length);
    
    let readButton = null;
    let deleteButton = null;
    
    allButtons.forEach(button => {
        const buttonText = button.textContent.trim();
        const buttonHtml = button.outerHTML;
        
        console.log('检查按钮:', buttonText, buttonHtml);
        
        // 通过文字内容和图标判断是否为已读/未读按钮
        if ((buttonText.includes('已读') || buttonText.includes('未读'))) {
            readButton = button;
            console.log('找到已读/未读按钮:', button);
        } 
        // 判断是否为删除按钮
        else if (buttonText.includes('删除') && buttonHtml.includes('fa-trash')) {
            deleteButton = button;
            console.log('找到删除按钮:', button);
        }
    });
    
    // 为已读/未读按钮添加点击事件
    if (readButton) {
        console.log('为已读/未读按钮添加点击事件');
        readButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('已读/未读按钮被点击:', this);
            
            // 确保按钮有正确的数据属性
            const selectedItem = document.querySelector('.bg-blue-50.border-blue-200');
            if (selectedItem) {
                const notificationId = selectedItem.dataset.notificationId;
                const isRead = selectedItem.dataset.isRead === 'true';
                
                this.dataset.notificationId = notificationId;
                this.dataset.isRead = isRead;
                console.log('已为按钮添加数据属性:', notificationId, isRead);
                
                toggleNotificationReadStatus(this);
            } else {
                console.error('未找到选中的通知项，无法获取通知ID');
                showNotification('请先选择一个通知', 'error');
            }
        });
    }
    
    // 初始化删除按钮
    if (deleteButton) {
        deleteButton.addEventListener('click', function() {
            showConfirmModal('确认删除', '确定要删除该通知吗？', function(confirmed) {
                if (confirmed) {
                    console.log('删除通知');
                    showNotification('通知已删除', 'success');
                }
            });
        });
    }
}

// 初始化发布通知功能
function initializePublishNotificationButton() {
    const publishButton = document.getElementById('publish-notification-btn');
    const modal = document.getElementById('publish-notification-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const form = document.getElementById('publish-notification-form');
    const titleInput = document.getElementById('notification-title');
    const contentInput = document.getElementById('notification-content');
    const remarkInput = document.getElementById('notification-remark');
    const validUntilContainer = document.getElementById('valid-until-container');
    const validUntilInput = document.getElementById('valid-until');
    const timeTypeRadios = document.querySelectorAll('input[name="notification_time_type"]');
    const titleCount = document.getElementById('title-count');
    const contentCount = document.getElementById('content-count');
    const remarkCount = document.getElementById('remark-count');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const fileInput = document.getElementById('notification-attachments');
    const fileList = document.getElementById('file-list');
    const submitBtn = document.getElementById('submit-notification-btn');
    const publishTimeInput = document.getElementById('publish-time');
    
    // 设置当前时间为发布时间
    const now = new Date();
    publishTimeInput.value = now.toISOString().slice(0, 19).replace('T', ' ');
    
    // 设置日期时间选择器的最小值为当前时间
    validUntilInput.min = now.toISOString().slice(0, 16);
    
    // 模态框控制
    function openModal() {
        modal.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
    }
    
    function closeModal() {
        modal.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
    }
    
    // 打开发布通知模态框
    if (publishButton) {
        publishButton.addEventListener('click', openModal);
    }
    
    // 关闭模态框
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }
    
    // 点击模态框背景关闭
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // 标题字符计数
    if (titleInput && titleCount) {
        titleInput.addEventListener('input', function() {
            const length = this.value.length;
            titleCount.textContent = length;
            updateProgress();
        });
    }
    
    // 内容字符计数
    if (contentInput && contentCount) {
        contentInput.addEventListener('input', function() {
            const length = this.value.length;
            contentCount.textContent = length;
            updateProgress();
        });
    }
    
    // 备注字符计数
    if (remarkInput && remarkCount) {
        remarkInput.addEventListener('input', function() {
            const length = this.value.length;
            remarkCount.textContent = length;
            updateProgress();
        });
    }
    
    // 时间类型选择处理
    timeTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === '2') {
                // 定期有效，显示日期选择器
                validUntilContainer.classList.remove('hidden');
                validUntilInput.required = true;
            } else {
                // 长期有效，隐藏日期选择器
                validUntilContainer.classList.add('hidden');
                validUntilInput.required = false;
                validUntilInput.value = '';
            }
            updateProgress();
        });
    });
    
    // 文件上传处理
    if (fileInput && fileList) {
        fileInput.addEventListener('change', function() {
            const files = Array.from(this.files);
            if (files.length > 0) {
                fileList.innerHTML = '';
                files.forEach(file => {
                    const fileItem = document.createElement('div');
                    fileItem.className = 'flex items-center justify-between bg-gray-50 px-4 py-2 rounded-lg';
                    fileItem.innerHTML = `
                        <div class="flex items-center gap-2">
                            <i class="fa fa-file text-gray-500"></i>
                            <span class="text-sm truncate">${file.name}</span>
                            <span class="text-xs text-gray-500">(${formatFileSize(file.size)})</span>
                        </div>
                        <button type="button" class="text-red-500 hover:text-red-700 remove-file-btn" data-filename="${file.name}">
                            <i class="fa fa-times"></i>
                        </button>
                    `;
                    fileList.appendChild(fileItem);
                });
                fileList.classList.remove('hidden');
            } else {
                fileList.classList.add('hidden');
            }
        });
        
        // 文件删除处理
        fileList.addEventListener('click', function(e) {
            if (e.target.closest('.remove-file-btn')) {
                const btn = e.target.closest('.remove-file-btn');
                btn.parentElement.remove();
                if (fileList.children.length === 0) {
                    fileList.classList.add('hidden');
                }
                // 重置文件输入，这会清除所有文件
                fileInput.value = '';
            }
        });
    }
    
    // 表单验证
    function validateField(field, errorId, validationFn) {
        const errorElement = document.getElementById(errorId);
        const isValid = validationFn(field);
        
        if (isValid) {
            field.classList.remove('border-red-500');
            errorElement.classList.add('hidden');
        } else {
            field.classList.add('border-red-500');
            errorElement.classList.remove('hidden');
        }
        
        return isValid;
    }
    
    // 标题验证
    function validateTitle() {
        return validateField(titleInput, 'title-error', (field) => {
            const value = field.value.trim();
            return value.length >= 5 && value.length <= 100;
        });
    }
    
    // 内容验证
    function validateContent() {
        return validateField(contentInput, 'content-error', (field) => {
            const value = field.value.trim();
            return value.length > 0;
        });
    }
    
    // 备注验证
    function validateRemark() {
        return validateField(remarkInput, 'remark-error', (field) => {
            const value = field.value.trim();
            return value.length > 0;
        });
    }
    
    // 日期验证
    function validateValidUntil() {
        if (validUntilInput.required) {
            return validateField(validUntilInput, 'valid-until-error', (field) => {
                const value = field.value;
                if (!value) return false;
                
                const selectedDate = new Date(value);
                const now = new Date();
                return selectedDate >= now;
            });
        }
        return true;
    }
    
    // 表单整体验证
    function validateForm() {
        const titleValid = validateTitle();
        const contentValid = validateContent();
        const remarkValid = validateRemark();
        const validUntilValid = validateValidUntil();
        
        return titleValid && contentValid && remarkValid && validUntilValid;
    }
    
    // 实时验证
    titleInput.addEventListener('blur', validateTitle);
    contentInput.addEventListener('blur', validateContent);
    remarkInput.addEventListener('blur', validateRemark);
    validUntilInput.addEventListener('blur', validateValidUntil);
    
    // 表单填写进度计算
    function updateProgress() {
        let completed = 0;
        let total = 4; // 标题、内容、类型、备注
        
        // 标题
        if (titleInput.value.trim().length >= 5) completed++;
        
        // 内容
        if (contentInput.value.trim().length > 0) completed++;
        
        // 类型
        const typeSelected = document.querySelector('input[name="notification_type"]:checked');
        if (typeSelected) completed++;
        
        // 备注
        if (remarkInput.value.trim().length > 0) completed++;
        
        // 有效期
        const timeType = document.querySelector('input[name="notification_time_type"]:checked').value;
        if (timeType === '1' || (timeType === '2' && validUntilInput.value)) {
            completed++;
            total++;
        }
        
        const progress = Math.round((completed / total) * 100);
        progressBar.style.width = `${progress}%`;
        progressText.textContent = `${progress}%`;
    }
    
    // 格式化文件大小
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // 显示提示
    function showToast(message, type = 'success') {
        const toast = document.getElementById(type === 'success' ? 'success-toast' : 'error-toast');
        const messageElement = document.getElementById(`${type === 'success' ? 'success' : 'error'}-message`);
        
        messageElement.textContent = message;
        toast.classList.remove('opacity-0');
        toast.classList.add('opacity-100');
        
        // 3秒后自动隐藏
        setTimeout(() => {
            toast.classList.remove('opacity-100');
            toast.classList.add('opacity-0');
        }, 3000);
    }
    
    // 表单提交
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 验证表单
        if (!validateForm()) {
            // 滚动到第一个错误字段
            const firstError = document.querySelector('.border-red-500');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            showToast('请检查表单填写是否正确', 'error');
            return;
        }
        
        // 禁用提交按钮
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa fa-spinner fa-spin mr-2"></i> 发布中...';
        
        // 构建表单数据
        const formData = new FormData(this);
        
        // 发送请求
        fetch('/api/notifications/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                // 成功
                showToast('通知发布成功', 'success');
                
                // 清空表单
                form.reset();
                
                // 重置UI
                validUntilContainer.classList.add('hidden');
                fileList.innerHTML = '';
                fileList.classList.add('hidden');
                titleCount.textContent = '0';
                contentCount.textContent = '0';
                remarkCount.textContent = '0';
                progressBar.style.width = '0%';
                progressText.textContent = '0%';
                
                // 关闭模态框
                closeModal();
                
                // 刷新页面或通知列表
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                // 失败
                showToast('通知发布失败', 'error');
            }
        })
        .catch(error => {
            console.error('发布通知失败:', error);
            showToast('发布失败，请稍后重试', 'error');
        })
        .finally(() => {
            // 恢复提交按钮
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fa fa-paper-plane mr-2"></i> 发布通知';
        });
    });
    
    console.log('发布通知功能已初始化');
}



// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', function() {
    console.log('DOM加载完成，开始初始化通知管理功能');
    initializeNotificationManagement();
    console.log('通知发布页面已初始化');
});

// 确保函数在window对象上可用，方便调试
window.initializeNotificationManagement = initializeNotificationManagement;
window.initializeNotificationList = initializeNotificationList;
window.loadNotificationDetails = loadNotificationDetails;