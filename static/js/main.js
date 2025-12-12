// 导航栏高亮功能
function highlightActiveNavItem() {
    // 获取当前URL路径
    const currentPath = window.location.pathname;
    
    // 获取所有导航链接
    const navLinks = document.querySelectorAll('.nav-link');
    
    // 遍历所有导航链接
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        
        // 检查当前路径是否匹配导航链接路径
        if (currentPath.startsWith(linkPath)) {
            // 添加高亮类
            link.classList.add('active', 'nav-item-active');
        } else {
            // 移除高亮类
            link.classList.remove('active', 'nav-item-active');
        }
    });
}

// 侧边栏切换功能
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const logoText = document.getElementById('logo-text');
    const navTexts = document.querySelectorAll('.nav-text');
    
    sidebar.classList.toggle('sidebar-collapsed');
    sidebar.classList.toggle('sidebar-expanded');
    mainContent.classList.toggle('main-collapsed');
    mainContent.classList.toggle('main-expanded');
    
    if (logoText) {
        logoText.classList.toggle('hidden');
    }
    
    navTexts.forEach(text => {
        text.classList.toggle('hidden');
    });
    
    // 更新CSS变量，设置header的left值为aside的宽度
    updateHeaderPosition();
    
    // 重新高亮导航项
    highlightActiveNavItem();
}

// 更新header位置函数
function updateHeaderPosition() {
    const sidebar = document.getElementById('sidebar');
    const root = document.documentElement;
    
    if (sidebar.classList.contains('sidebar-collapsed')) {
        root.style.setProperty('--sidebar-width', '64px');
    } else {
        root.style.setProperty('--sidebar-width', '240px');
    }
}

// 移动端菜单按钮功能
function toggleMobileMenu() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('sidebar-expanded');
}

// 用户菜单功能
function toggleUserMenu() {
    const userMenu = document.getElementById('user-dropdown');
    userMenu.classList.toggle('hidden');
}

// 搜索功能
function handleSearch() {
    const searchInput = document.querySelector('input[type="text"]');
    const searchTerm = searchInput.value.toLowerCase();
    // 这里可以添加搜索逻辑
    console.log('搜索:', searchTerm);
}

// 页面加载完成后初始化事件监听器
document.addEventListener('DOMContentLoaded', function() {
    // 初始化header位置
    updateHeaderPosition();
    
    // 高亮当前导航项
    highlightActiveNavItem();
    
    // 侧边栏切换按钮
    const toggleSidebarBtn = document.getElementById('toggle-sidebar');
    if (toggleSidebarBtn) {
        toggleSidebarBtn.addEventListener('click', toggleSidebar);
    }
    
    // 移动端菜单按钮
    const mobileMenuBtn = document.getElementById('mobile-menu-button');
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', toggleMobileMenu);
    }
    
    // 用户菜单按钮
    const userMenuBtn = document.getElementById('user-menu-btn');
    if (userMenuBtn) {
        userMenuBtn.addEventListener('click', toggleUserMenu);
    }
    
    // 点击页面其他地方关闭用户菜单
    document.addEventListener('click', function(event) {
        const userMenu = document.getElementById('user-dropdown');
        const userMenuBtn = document.getElementById('user-menu-btn');
        
        if (userMenu && userMenuBtn && !userMenu.contains(event.target) && !userMenuBtn.contains(event.target)) {
            userMenu.classList.add('hidden');
        }
    });
    
    // 退出登录确认
    const logoutLink = document.querySelector('a[href="/logout/"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(event) {
            // 阻止默认事件
            event.preventDefault();
            
            // 显示确认弹窗
            showConfirmModal('确认退出', '确定要退出登录吗？', function(confirmed) {
                if (confirmed) {
                    // 执行退出登录
                    window.location.href = logoutLink.href;
                }
            });
        });
    }
    
    // 搜索框回车事件
    const searchInputs = document.querySelectorAll('input[type="text"]');
    searchInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleSearch();
            }
        });
    });
    
    // 初始化图表（如果存在Chart.js）
    if (typeof Chart !== 'undefined') {
        initializeCharts();
    }
    
    // 表格行悬停效果
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.classList.add('bg-gray-50');
        });
        row.addEventListener('mouseleave', function() {
            this.classList.remove('bg-gray-50');
        });
    });
    
    // 卡片悬停效果
    const cards = document.querySelectorAll('.card-hover');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow-md');
        });
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-md');
        });
    });
    
    console.log('社区居民信息管理系统已加载完成');
});

// 监听URL变化事件，支持客户端路由跳转
window.addEventListener('popstate', highlightActiveNavItem);
window.addEventListener('hashchange', highlightActiveNavItem);

// 弹窗处理功能

// 通用弹窗显示函数
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        // 延迟添加flex类，确保过渡动画生效
        setTimeout(() => {
            modal.classList.add('flex', 'opacity-100', 'pointer-events-auto');
            // 获取弹窗内容元素
            const modalContent = modal.querySelector('div > div');
            if (modalContent) {
                modalContent.classList.remove('scale-95');
                modalContent.classList.add('scale-100');
            }
        }, 10);
        // 阻止背景滚动
        document.body.classList.add('overflow-hidden');
    }
}

// 通用弹窗隐藏函数
function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('opacity-100', 'pointer-events-auto');
        // 获取弹窗内容元素
        const modalContent = modal.querySelector('div > div');
        if (modalContent) {
            modalContent.classList.remove('scale-100');
            modalContent.classList.add('scale-95');
        }
        // 延迟添加hidden类，确保过渡动画完成
        setTimeout(() => {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            // 恢复背景滚动
            document.body.classList.remove('overflow-hidden');
            // 重置表单
            const form = modal.querySelector('form');
            if (form) {
                form.reset();
            }
        }, 300);
    }
}

// 表单验证函数
function validateForm(form) {
    // 检查必填字段
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('border-red-500');
            field.addEventListener('input', function() {
                this.classList.remove('border-red-500');
            }, { once: true });
        }
    });
    
    return isValid;
}

// 初始化弹窗事件
function initializeModals() {
    // 添加居民弹窗
    const addResidentBtn = document.querySelector('#add-resident-btn, [data-target="add-resident"]');
    if (addResidentBtn) {
        addResidentBtn.addEventListener('click', function() {
            showModal('add-resident-modal');
        });
    }
    
    // 添加家庭弹窗
    const addFamilyBtn = document.querySelector('#add-family-btn, [data-target="add-family"]');
    if (addFamilyBtn) {
        addFamilyBtn.addEventListener('click', function() {
            showModal('add-family-modal');
        });
    }
    

    
    // 发布通知弹窗
    const publishNotificationBtn = document.querySelector('#publish-notification-btn, [data-target="publish-notification"]');
    if (publishNotificationBtn) {
        publishNotificationBtn.addEventListener('click', function() {
            showModal('publish-notification-modal');
        });
    }
    
    // 关闭按钮事件
    document.getElementById('close-resident-modal')?.addEventListener('click', () => hideModal('add-resident-modal'));
    document.getElementById('cancel-resident-modal')?.addEventListener('click', () => hideModal('add-resident-modal'));
    
    document.getElementById('close-family-modal')?.addEventListener('click', () => hideModal('add-family-modal'));
    document.getElementById('cancel-family-modal')?.addEventListener('click', () => hideModal('add-family-modal'));
    

    
    document.getElementById('close-notification-modal')?.addEventListener('click', () => hideModal('publish-notification-modal'));
    document.getElementById('cancel-notification-modal')?.addEventListener('click', () => hideModal('publish-notification-modal'));
    
    // 点击背景关闭弹窗
    const modals = document.querySelectorAll('.fixed.inset-0.bg-black.bg-opacity-50');
    modals.forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                hideModal(this.id);
            }
        });
    });
    
    // ESC键关闭弹窗
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            // 获取所有打开的弹窗
            const openModals = document.querySelectorAll('.fixed.inset-0.bg-black.bg-opacity-50.flex.opacity-100.pointer-events-auto');
            openModals.forEach(modal => {
                hideModal(modal.id);
            });
        }
    });
    
    // 表单提交事件
    const addResidentForm = document.getElementById('add-resident-form');
    if (addResidentForm) {
        addResidentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (validateForm(this)) {
                // 这里可以添加表单提交逻辑
                showNotification('居民添加成功', 'success');
                hideModal('add-resident-modal');
            } else {
                showNotification('请填写所有必填字段', 'error');
            }
        });
    }
    
    const addFamilyForm = document.getElementById('add-family-form');
    if (addFamilyForm) {
        addFamilyForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (validateForm(this)) {
                // 这里可以添加表单提交逻辑
                showNotification('家庭添加成功', 'success');
                hideModal('add-family-modal');
            } else {
                showNotification('请填写所有必填字段', 'error');
            }
        });
    }
    

    
    const publishNotificationForm = document.getElementById('publish-notification-form');
    if (publishNotificationForm) {
        publishNotificationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (validateForm(this)) {
                // 这里可以添加表单提交逻辑
                showNotification('通知发布成功', 'success');
                hideModal('publish-notification-modal');
            } else {
                showNotification('请填写所有必填字段', 'error');
            }
        });
    }
}

// 初始化查看详情弹窗事件
function initializeDetailModals() {
    // 关闭查看居民详情弹窗
    document.getElementById('close-view-resident-modal')?.addEventListener('click', () => hideModal('view-resident-modal'));
    document.getElementById('close-view-resident-btn')?.addEventListener('click', () => hideModal('view-resident-modal'));
    
    // 关闭查看家庭详情弹窗
    document.getElementById('close-view-family-modal')?.addEventListener('click', () => hideModal('view-family-modal'));
    document.getElementById('close-view-family-btn')?.addEventListener('click', () => hideModal('view-family-modal'));
    
    // 关闭查看地址详情弹窗
    document.getElementById('close-view-address-modal')?.addEventListener('click', () => hideModal('view-address-modal'));
    document.getElementById('close-view-address-btn')?.addEventListener('click', () => hideModal('view-address-modal'));
}

// 在页面加载完成后初始化弹窗事件
document.addEventListener('DOMContentLoaded', function() {
    initializeModals();
    initializeDetailModals();
    initializeEditModals();
    
    // 初始化查看详情功能
    initializeViewDetailFunctionality();
    
    // 初始化编辑功能
    initializeEditFunctionality();
});

// 初始化查看详情功能
function initializeViewDetailFunctionality() {
    // 查看居民详情
    const viewResidentLinks = document.querySelectorAll('.view-resident-btn, [data-target="view-resident"]');
    viewResidentLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const residentId = this.dataset.id || 1; // 默认为1，如果有data-id属性则使用该值
            viewResidentDetail(residentId);
        });
    });
    
    // 查看家庭详情
    const viewFamilyLinks = document.querySelectorAll('.view-family-btn, [data-target="view-family"]');
    viewFamilyLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const familyId = this.dataset.id || 1; // 默认为1，如果有data-id属性则使用该值
            viewFamilyDetail(familyId);
        });
    });
    
    // 查看地址详情
    const viewAddressLinks = document.querySelectorAll('.view-address-btn, [data-target="view-address"]');
    viewAddressLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const addressId = this.dataset.id || 1; // 默认为1，如果有data-id属性则使用该值
            viewAddressDetail(addressId);
        });
    });
}

// 初始化编辑弹窗事件
function initializeEditModals() {
    // 关闭编辑居民详情弹窗
    document.getElementById('close-edit-resident-modal')?.addEventListener('click', () => hideModal('edit-resident-modal'));
    document.getElementById('cancel-edit-resident-btn')?.addEventListener('click', () => hideModal('edit-resident-modal'));
    
    // 关闭编辑家庭详情弹窗
    document.getElementById('close-edit-family-modal')?.addEventListener('click', () => hideModal('edit-family-modal'));
    document.getElementById('cancel-edit-family-btn')?.addEventListener('click', () => hideModal('edit-family-modal'));
    
    // 关闭编辑地址详情弹窗
    document.getElementById('close-edit-address-modal')?.addEventListener('click', () => hideModal('edit-address-modal'));
    document.getElementById('cancel-edit-address-btn')?.addEventListener('click', () => hideModal('edit-address-modal'));
}

// 初始化编辑功能
function initializeEditFunctionality() {
    // 编辑居民
    const editResidentLinks = document.querySelectorAll('.edit-resident-btn, [data-target="edit-resident"]');
    editResidentLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const residentId = this.dataset.id || 1; // 默认为1，如果有data-id属性则使用该值
            editResident(residentId);
        });
    });
    
    // 编辑家庭
    const editFamilyLinks = document.querySelectorAll('.edit-family-btn, [data-target="edit-family"]');
    editFamilyLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const familyId = this.dataset.id || 1; // 默认为1，如果有data-id属性则使用该值
            editFamily(familyId);
        });
    });
    
    // 编辑地址
    const editAddressLinks = document.querySelectorAll('.edit-address-btn, [data-target="edit-address"]');
    editAddressLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const addressId = this.dataset.id || 1; // 默认为1，如果有data-id属性则使用该值
            editAddress(addressId);
        });
    });
    
    // 编辑居民表单提交
    const editResidentForm = document.getElementById('edit-resident-form');
    if (editResidentForm) {
        editResidentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (validateForm(this)) {
                // 这里可以添加表单提交逻辑
                showNotification('居民编辑成功', 'success');
                hideModal('edit-resident-modal');
            } else {
                showNotification('请填写所有必填字段', 'error');
            }
        });
    }
    
    // 编辑家庭表单提交
    const editFamilyForm = document.getElementById('edit-family-form');
    if (editFamilyForm) {
        editFamilyForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (validateForm(this)) {
                // 这里可以添加表单提交逻辑
                showNotification('家庭编辑成功', 'success');
                hideModal('edit-family-modal');
            } else {
                showNotification('请填写所有必填字段', 'error');
            }
        });
    }
    
    // 编辑地址表单提交
    const editAddressForm = document.getElementById('edit-address-form');
    if (editAddressForm) {
        editAddressForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (validateForm(this)) {
                // 这里可以添加表单提交逻辑
                showNotification('地址编辑成功', 'success');
                hideModal('edit-address-modal');
            } else {
                showNotification('请填写所有必填字段', 'error');
            }
        });
    }
}

// 编辑居民
function editResident(residentId) {
    // 这里可以通过AJAX请求获取居民详情数据
    // 目前使用模拟数据
    const residentData = {
        id: residentId,
        name: '张明',
        gender: 1,
        id_card: '3101************',
        phone: '138****5678',
        family_id: 1,
        identity_type: 1,
        nationality: 1, // 1=汉族
        political_status: 3,
        marital_status: 2,
        education: 6,
        job: true
    };
    
    // 填充表单数据
    document.getElementById('edit-resident-id').value = residentData.id;
    document.getElementById('edit-resident-name').value = residentData.name;
    document.getElementById('edit-resident-gender').value = residentData.gender;
    document.getElementById('edit-resident-id-card').value = residentData.id_card;
    document.getElementById('edit-resident-phone').value = residentData.phone;
    document.getElementById('edit-resident-family').value = residentData.family_id;
    document.getElementById('edit-resident-nationality').value = residentData.nationality;
    document.getElementById('edit-resident-political-status').value = residentData.political_status;
    document.getElementById('edit-resident-marital-status').value = residentData.marital_status;
    document.getElementById('edit-resident-education').value = residentData.education;
    document.getElementById('edit-resident-job').value = residentData.job;
    
    // 显示弹窗
    showModal('edit-resident-modal');
}

// 编辑家庭
function editFamily(familyId) {
    // 这里可以通过AJAX请求获取家庭详情数据
    // 目前使用模拟数据
    const familyData = {
        id: familyId,
        household_number: 'F2023001',
        residential_address_id: 1,
        house_type: 1,
        contact_phone: '138****5678',
        remark: '无特殊备注'
    };
    
    // 填充表单数据
    document.getElementById('edit-family-id').value = familyData.id;
    document.getElementById('edit-family-household-number').value = familyData.household_number;
    document.getElementById('edit-family-residential-address').value = familyData.residential_address_id;
    document.getElementById('edit-family-house-type').value = familyData.house_type;
    document.getElementById('edit-family-contact-phone').value = familyData.contact_phone;
    document.getElementById('edit-family-remark').value = familyData.remark;
    
    // 显示弹窗
    showModal('edit-family-modal');
}

// 编辑地址
function editAddress(addressId) {
    // 这里可以通过AJAX请求获取地址详情数据
    // 目前使用模拟数据
    const addressData = {
        id: addressId,
        address_type: 1, // 1=楼房，2=平房
        estate_id: 1,
        building_id: 1,
        unit_id: 1,
        apartment_id: 1,
        hutong_id: null,
        single_house_id: null,
        is_resident: 1 // 1=自住，2=租住，3=空房
    };
    
    // 填充表单数据
    document.getElementById('edit-address-id').value = addressData.id;
    document.getElementById('edit-address-address-type').value = addressData.address_type;
    document.getElementById('edit-address-estate').value = addressData.estate_id;
    document.getElementById('edit-address-building').value = addressData.building_id;
    document.getElementById('edit-address-unit').value = addressData.unit_id;
    document.getElementById('edit-address-apartment').value = addressData.apartment_id;
    document.getElementById('edit-address-hutong').value = addressData.hutong_id || '';
    document.getElementById('edit-address-single-house').value = addressData.single_house_id || '';
    document.getElementById('edit-address-is-resident').value = addressData.is_resident;
    
    // 显示弹窗
    showModal('edit-address-modal');
}

// 查看居民详情
function viewResidentDetail(residentId) {
    // 这里可以通过AJAX请求获取居民详情数据
    // 目前使用模拟数据
    const residentData = {
        id: residentId,
        name: '张明',
        gender: '男',
        id_card: '3101************',
        phone: '138****5678',
        family: '张家庭',
        nationality: '汉族',
        political_status: '群众',
        marital_status: '已婚',
        education: '本科',
        job: '有工作'
    };
    
    // 渲染居民详情内容
    const content = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">姓名</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${residentData.name}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">性别</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${residentData.gender}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">身份证号</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${residentData.id_card}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">联系电话</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${residentData.phone}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">所属家庭</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${residentData.family}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">民族</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${residentData.nationality}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">政治面貌</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${residentData.political_status}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">婚姻状态</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${residentData.marital_status}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">学历</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${residentData.education}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">是否有工作</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${residentData.job}</div>
            </div>
        </div>
    `;
    
    // 更新弹窗内容
    const contentDiv = document.getElementById('resident-detail-content');
    if (contentDiv) {
        contentDiv.innerHTML = content;
    }
    
    // 显示弹窗
    showModal('view-resident-modal');
}

// 查看家庭详情
function viewFamilyDetail(familyId) {
    // 这里可以通过AJAX请求获取家庭详情数据
    // 目前使用模拟数据
    const familyData = {
        id: familyId,
        household_number: 'F2023001',
        residential_address: '1号楼3单元501室',
        house_type: '自住房',
        contact_phone: '138****5678',
        remark: '无特殊备注'
    };
    
    // 渲染家庭详情内容
    const content = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">户号</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${familyData.household_number}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">居住地址</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${familyData.residential_address}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">房屋性质</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${familyData.house_type}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">联系电话</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${familyData.contact_phone}</div>
            </div>
            <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">备注</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${familyData.remark}</div>
            </div>
        </div>
    `;
    
    // 更新弹窗内容
    const contentDiv = document.getElementById('family-detail-content');
    if (contentDiv) {
        contentDiv.innerHTML = content;
    }
    
    // 显示弹窗
    showModal('view-family-modal');
}

// 查看地址详情
function viewAddressDetail(addressId) {
    // 这里可以通过AJAX请求获取地址详情数据
    // 目前使用模拟数据
    const addressData = {
        id: addressId,
        address_type: '楼房',
        estate: '阳光花园',
        building: '1号楼',
        unit: '3单元',
        apartment: '501室',
        hutong: '',
        single_house: '',
        is_resident: '自住'
    };
    
    // 渲染地址详情内容
    const content = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">地址类型</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${addressData.address_type}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">所属小区</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${addressData.estate}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">所属楼栋</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${addressData.building}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">所属单元</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${addressData.unit}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">楼房房号</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${addressData.apartment}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">所属胡同</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${addressData.hutong || '无'}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">平房房号</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${addressData.single_house || '无'}</div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">居住状态</label>
                <div class="bg-gray-50 border border-gray-200 rounded-md p-3">${addressData.is_resident}</div>
            </div>
        </div>
    `;
    
    // 更新弹窗内容
    const contentDiv = document.getElementById('address-detail-content');
    if (contentDiv) {
        contentDiv.innerHTML = content;
    }
    
    // 显示弹窗
    showModal('view-address-modal');
}

// 初始化图表
function initializeCharts() {
    // 这里可以添加默认的图表初始化逻辑
    // 具体的图表配置将在各个页面的专用JS文件中实现
    console.log('图表初始化函数已准备就绪');
}

// 通用的AJAX请求函数
function ajaxRequest(url, method, data = null, successCallback, errorCallback) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    
    // 添加CSRF令牌
    let csrfToken = '';
    
    // 首先尝试从meta标签获取
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken) {
        csrfToken = metaToken.getAttribute('content');
    } else {
        // 然后尝试从表单输入获取
        const formToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (formToken) {
            csrfToken = formToken.value;
        }
    }
    
    if (csrfToken) {
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
    }
    
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
            const response = JSON.parse(xhr.responseText);
            if (successCallback) {
                successCallback(response);
            }
        } else {
            if (errorCallback) {
                errorCallback(xhr.status, xhr.statusText);
            } else {
                console.error('请求失败:', xhr.status, xhr.statusText);
                showNotification('请求失败: ' + xhr.statusText, 'error');
            }
        }
    };
    
    xhr.onerror = function() {
        if (errorCallback) {
            errorCallback(0, '网络错误');
        } else {
            console.error('网络错误');
            showNotification('网络错误', 'error');
        }
    };
    
    if (data) {
        xhr.send(JSON.stringify(data));
    } else {
        xhr.send();
    }
}

// 显示通知
function showNotification(message, type = 'info', duration = 3000) {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} fixed top-4 right-4 z-50`;
    notification.innerHTML = `
        <div class="flex items-start">
            <div class="flex-shrink-0">
                <i class="fa fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'warning' : 'info-circle'} text-${type === 'success' ? 'success' : type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'primary'}"></i>
            </div>
            <div class="ml-3 flex-1">
                <p class="text-sm font-medium text-gray-800">${message}</p>
            </div>
            <button class="ml-3 text-gray-400 hover:text-gray-600" onclick="this.parentElement.parentElement.remove()">
                <i class="fa fa-times"></i>
            </button>
        </div>
    `;
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 自动移除
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

// 显示退出登录弹窗
function showLogoutModal() {
    const modal = document.getElementById('logout-modal');
    const modalContent = document.getElementById('logout-modal-content');
    
    if (modal && modalContent) {
        // 显示弹窗背景
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        
        // 延迟添加动画类，确保过渡效果生效
        setTimeout(() => {
            modal.classList.add('opacity-100');
            modalContent.classList.remove('scale-95', 'opacity-0');
            modalContent.classList.add('scale-100', 'opacity-100');
        }, 10);
        
        // 阻止背景滚动
        document.body.classList.add('overflow-hidden');
        
        // 绑定取消按钮事件
        const cancelBtn = document.getElementById('cancel-logout-btn');
        if (cancelBtn) {
            cancelBtn.onclick = hideLogoutModal;
        }
        
        // 点击背景关闭弹窗
        modal.onclick = function(e) {
            if (e.target === this) {
                hideLogoutModal();
            }
        };
        
        // ESC键关闭弹窗
        document.addEventListener('keydown', function handleEscKey(e) {
            if (e.key === 'Escape') {
                hideLogoutModal();
                document.removeEventListener('keydown', handleEscKey);
            }
        });
    }
}

// 隐藏退出登录弹窗
function hideLogoutModal() {
    const modal = document.getElementById('logout-modal');
    const modalContent = document.getElementById('logout-modal-content');
    
    if (modal && modalContent) {
        // 移除动画类，开始退出动画
        modal.classList.remove('opacity-100');
        modalContent.classList.remove('scale-100', 'opacity-100');
        modalContent.classList.add('scale-95', 'opacity-0');
        
        // 延迟隐藏弹窗，确保过渡动画完成
        setTimeout(() => {
            modal.classList.remove('flex');
            modal.classList.add('hidden');
            
            // 恢复背景滚动
            document.body.classList.remove('overflow-hidden');
        }, 300);
    }
}

// 表单验证函数
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('border-red-300');
            input.classList.add('focus:ring-red-400');
        } else {
            input.classList.remove('border-red-300');
            input.classList.remove('focus:ring-red-400');
        }
    });
    
    return isValid;
}

// 日期格式化函数
function formatDate(date) {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 数字格式化函数
function formatNumber(num) {
    return num.toLocaleString('zh-CN');
}

// 复制到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => {
            showNotification('已复制到剪贴板', 'success');
        })
        .catch(err => {
            console.error('复制失败:', err);
            showNotification('复制失败', 'error');
        });
}