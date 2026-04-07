/**
 * API请求模块
 * 封装所有与后端的通信
 */

const API = {
    // 基础URL
    baseURL: '/api',
    
    // 获取Token
    getToken() {
        return localStorage.getItem('token');
    },
    
    // 设置Token
    setToken(token) {
        localStorage.setItem('token', token);
    },
    
    // 清除Token
    clearToken() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    },
    
    // 获取用户信息
    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },
    
    // 设置用户信息
    setUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    },
    
    // 通用请求方法
    async request(url, options = {}) {
        const token = this.getToken();
        
        const defaultHeaders = {
            'Content-Type': 'application/json',
        };
        
        if (token) {
            defaultHeaders['Authorization'] = `Bearer ${token}`;
        }
        
        const config = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...options.headers,
            },
        };
        
        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }
        
        try {
            const response = await fetch(`${this.baseURL}${url}`, config);
            const data = await response.json();
            
            // 处理401未授权
            if (response.status === 401) {
                this.clearToken();
                window.location.href = '/login/';
                return null;
            }
            
            return data;
        } catch (error) {
            console.error('API请求错误:', error);
            throw error;
        }
    },
    
    // GET请求
    get(url, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const fullUrl = queryString ? `${url}?${queryString}` : url;
        return this.request(fullUrl, { method: 'GET' });
    },
    
    // POST请求
    post(url, data = {}) {
        return this.request(url, {
            method: 'POST',
            body: data,
        });
    },
    
    // PUT请求
    put(url, data = {}) {
        return this.request(url, {
            method: 'PUT',
            body: data,
        });
    },
    
    // DELETE请求
    delete(url) {
        return this.request(url, { method: 'DELETE' });
    },
    
    // ==================== 认证相关 ====================
    
    // 登录
    login(username, password) {
        return this.post('/auth/login/', { username, password });
    },
    
    // 退出登录
    logout() {
        return this.post('/auth/logout/');
    },
    
    // 获取当前用户信息
    getUserInfo() {
        return this.get('/auth/user/');
    },
    
    // ==================== 仪表盘 ====================
    
    // 获取仪表盘数据
    getDashboard() {
        return this.get('/dashboard/');
    },
    
    // ==================== 单位管理 ====================
    
    getUnits(params = {}) {
        return this.get('/units/', params);
    },
    
    createUnit(data) {
        return this.post('/units/', data);
    },
    
    updateUnit(id, data) {
        return this.put(`/units/${id}/`, data);
    },
    
    deleteUnit(id) {
        return this.delete(`/units/${id}/`);
    },
    
    // ==================== 品类管理 ====================
    
    getCategories(params = {}) {
        return this.get('/categories/', params);
    },
    
    createCategory(data) {
        return this.post('/categories/', data);
    },
    
    updateCategory(id, data) {
        return this.put(`/categories/${id}/`, data);
    },
    
    deleteCategory(id) {
        return this.delete(`/categories/${id}/`);
    },
    
    // ==================== 品种管理 ====================
    
    getVarieties(params = {}) {
        return this.get('/varieties/', params);
    },
    
    createVariety(data) {
        return this.post('/varieties/', data);
    },
    
    updateVariety(id, data) {
        return this.put(`/varieties/${id}/`, data);
    },
    
    deleteVariety(id) {
        return this.delete(`/varieties/${id}/`);
    },
    
    // ==================== 货物管理 ====================
    
    getGoods(params = {}) {
        return this.get('/goods/', params);
    },
    
    createGoods(data) {
        return this.post('/goods/', data);
    },
    
    updateGoods(id, data) {
        return this.put(`/goods/${id}/`, data);
    },
    
    deleteGoods(id) {
        return this.delete(`/goods/${id}/`);
    },
    
    // ==================== 入库管理 ====================
    
    getStockIns(params = {}) {
        return this.get('/stock-in/', params);
    },
    
    createStockIn(data) {
        return this.post('/stock-in/', data);
    },
    
    // ==================== 出库管理 ====================
    
    getStockOuts(params = {}) {
        return this.get('/stock-out/', params);
    },
    
    createStockOut(data) {
        return this.post('/stock-out/', data);
    },
    
    // ==================== 预警管理 ====================
    
    getWarnings(params = {}) {
        return this.get('/warnings/', params);
    },
    
    markWarningRead(id) {
        return this.put(`/warnings/${id}/read/`);
    },
    
    // ==================== 审批管理 ====================
    
    getApprovals(params = {}) {
        return this.get('/approvals/', params);
    },
    
    handleApproval(id, action, remark = '') {
        return this.put(`/approvals/${id}/`, { action, remark });
    },
    
    // ==================== 人员管理 ====================
    
    getAttendancePersons(params = {}) {
        return this.get('/attendance-persons/', params);
    },
    
    createAttendancePerson(data) {
        return this.post('/attendance-persons/', data);
    },
    
    updateAttendancePerson(id, data) {
        return this.put(`/attendance-persons/${id}/`, data);
    },
    
    deleteAttendancePerson(id) {
        return this.delete(`/attendance-persons/${id}/`);
    },
    
    getStockOutPersons(params = {}) {
        return this.get('/stock-out-persons/', params);
    },
    
    createStockOutPerson(data) {
        return this.post('/stock-out-persons/', data);
    },
    
    updateStockOutPerson(id, data) {
        return this.put(`/stock-out-persons/${id}/`, data);
    },
    
    deleteStockOutPerson(id) {
        return this.delete(`/stock-out-persons/${id}/`);
    },
    
    // ==================== 报表管理 ====================
    
    getDailyReport(params = {}) {
        return this.get('/daily-report/', params);
    },
    
    // 获取系统监控数据 (使用psutil)
    getSystemMonitor() {
        return this.get('/system-monitor/');
    },
    
    // 导出数据 (使用openpyxl)
    exportData(type) {
        const token = this.getToken();
        window.open(`${this.baseURL}/export/?type=${type}&token=${token}`, '_blank');
    },
    
    // ==================== 数据导入导出 (django-import-export) ====================
    
    // 导出数据（支持xlsx/csv/json格式）
    importExportDownload(type, format = 'xlsx') {
        const token = this.getToken();
        window.open(`${this.baseURL}/import-export/?type=${type}&format=${format}&token=${token}`, '_blank');
    },
    
    // 导入数据
    async importData(type, file) {
        const formData = new FormData();
        formData.append('type', type);
        formData.append('file', file);
        
        const token = this.getToken();
        const response = await fetch(`${this.baseURL}/import-export/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData,
        });
        return response.json();
    },
};

// 导出
window.API = API;
