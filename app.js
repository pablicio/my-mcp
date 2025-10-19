// MCP Server Dashboard - JavaScript

const API_URL = 'http://localhost:5000/api';
let autoRefreshInterval;
let allTasks = [];
let allLogs = [];
let currentFilter = 'all';
let currentLogFilter = 'all';

// ========== INICIALIZAÇÃO ==========

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 MCP Dashboard inicializando...');
    
    setupTabs();
    setupForms();
    setupFilters();
    setupSearch();
    
    loadStatus();
    loadTasks();
    loadEvents();
    loadNotes();
    loadLogs();
    loadConnections();
    
    autoRefreshInterval = setInterval(() => {
        loadStatus();
        const activeTab = document.querySelector('.tab.active')?.dataset.tab;
        
        if (activeTab === 'tasks' || activeTab === 'dashboard') loadTasks();
        if (activeTab === 'calendar' || activeTab === 'dashboard') loadEvents();
        if (activeTab === 'logs') loadLogs();
        if (activeTab === 'connections') loadConnections();
    }, 5000);
    
    console.log('✅ Dashboard inicializado');
});

// ========== TABS ==========

function setupTabs() {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.content-panel').forEach(p => p.classList.remove('active'));
            
            tab.classList.add('active');
            const panelId = tab.dataset.tab;
            document.getElementById(panelId)?.classList.add('active');
            
            console.log(`📑 Tab mudada para: ${panelId}`);
        });
    });
}

// ========== STATUS ==========

async function loadStatus() {
    try {
        const response = await fetch(`${API_URL}/status`);
        const data = await response.json();
        
        const statusEl = document.getElementById('serverStatus');
        if (data.status === 'running') {
            statusEl.innerHTML = '<div class="status-dot status-online"></div><span>Online</span>';
        } else {
            statusEl.innerHTML = '<div class="status-dot status-offline"></div><span>Offline</span>';
        }
        
        const stats = data.stats || {};
        document.getElementById('noteCount').textContent = stats.notes || 0;
        
    } catch (error) {
        console.error('❌ Erro ao carregar status:', error);
        document.getElementById('serverStatus').innerHTML = '<div class="status-dot status-offline"></div><span>Erro</span>';
    }
}

// ========== TASKS ==========

async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        const data = await response.json();
        
        allTasks = data.tasks || [];
        
        const pending = allTasks.filter(t => !t.completed).length;
        const completed = allTasks.filter(t => t.completed).length;
        
        document.getElementById('taskCount').textContent = pending;
        document.getElementById('completedCount').textContent = completed;
        
        renderTasks();
        renderDashboardTasks();
        
        console.log(`✅ ${allTasks.length} tarefas carregadas`);
    } catch (error) {
        console.error('❌ Erro ao carregar tarefas:', error);
        showToast('Erro ao carregar tarefas', 'error');
    }
}

function renderTasks() {
    const container = document.getElementById('taskList');
    let filtered = allTasks;
    
    if (currentFilter === 'pending') {
        filtered = allTasks.filter(t => !t.completed);
    } else if (currentFilter === 'completed') {
        filtered = allTasks.filter(t => t.completed);
    } else if (currentFilter === 'high') {
        filtered = allTasks.filter(t => t.priority === 'high' && !t.completed);
    }
    
    const searchTerm = document.getElementById('taskSearch')?.value.toLowerCase();
    if (searchTerm) {
        filtered = filtered.filter(t => 
            t.title.toLowerCase().includes(searchTerm) ||
            t.description.toLowerCase().includes(searchTerm)
        );
    }
    
    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📋</div>
                <div class="empty-state-title">Nenhuma tarefa encontrada</div>
                <p>Crie uma nova tarefa para começar</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = filtered.map(task => `
        <div class="task-item ${task.completed ? 'completed' : ''}">
            <div class="task-content">
                <div class="task-title">
                    ${task.completed ? '✅' : '⏳'} #${task.id} ${escapeHtml(task.title)}
                </div>
                ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
                <div class="task-meta">
                    <span class="priority-badge priority-${task.priority}">
                        ${getPriorityIcon(task.priority)} ${task.priority.toUpperCase()}
                    </span>
                    ${task.due_date ? `<span>📅 ${formatDate(task.due_date)}</span>` : ''}
                    <span>🕐 ${formatDateTime(task.created_at)}</span>
                </div>
            </div>
            <div class="task-actions">
                ${!task.completed ? `
                    <button class="btn btn-success btn-sm" onclick="completeTask(${task.id})">✓</button>
                ` : ''}
                <button class="btn btn-danger btn-sm" onclick="deleteTask(${task.id})">🗑️</button>
            </div>
        </div>
    `).join('');
}

function renderDashboardTasks() {
    const container = document.getElementById('dashboardTasks');
    const recentTasks = allTasks.filter(t => !t.completed).slice(0, 5);
    
    if (recentTasks.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📋</div><p>Nenhuma tarefa ativa</p></div>';
        return;
    }
    
    container.innerHTML = `<div class="task-grid">${recentTasks.map(task => `
        <div class="task-item">
            <div class="task-content">
                <div class="task-title">⏳ ${escapeHtml(task.title)}</div>
                ${task.description ? `<div class="task-description">${escapeHtml(task.description.substring(0, 100))}...</div>` : ''}
                <div class="task-meta">
                    <span class="priority-badge priority-${task.priority}">
                        ${getPriorityIcon(task.priority)} ${task.priority.toUpperCase()}
                    </span>
                </div>
            </div>
            <div class="task-actions">
                <button class="btn btn-success btn-sm" onclick="completeTask(${task.id})">✓</button>
            </div>
        </div>
    `).join('')}</div>`;
}

async function completeTask(taskId) {
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}/complete`, { method: 'POST' });
        if (response.ok) {
            showToast('Tarefa concluída! 🎉', 'success');
            await loadTasks();
        }
    } catch (error) {
        console.error('❌ Erro ao concluir tarefa:', error);
        showToast('Erro ao concluir tarefa', 'error');
    }
}

async function deleteTask(taskId) {
    if (!confirm('Tem certeza que deseja deletar esta tarefa?')) return;
    
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, { method: 'DELETE' });
        if (response.ok) {
            showToast('Tarefa deletada', 'success');
            await loadTasks();
        }
    } catch (error) {
        console.error('❌ Erro ao deletar tarefa:', error);
        showToast('Erro ao deletar tarefa', 'error');
    }
}

// ========== EVENTS ==========

async function loadEvents() {
    try {
        const events = [
            {
                id: 1,
                title: 'Reunião de equipe',
                start: new Date().toISOString(),
                description: 'Reunião semanal da equipe'
            }
        ];
        
        document.getElementById('eventCount').textContent = events.length;
        renderEvents(events);
        renderDashboardEvents(events);
        
    } catch (error) {
        console.error('❌ Erro ao carregar eventos:', error);
    }
}

function renderEvents(events) {
    const container = document.getElementById('eventList');
    
    if (events.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📅</div>
                <div class="empty-state-title">Nenhum evento agendado</div>
            </div>
        `;
        return;
    }
    
    container.innerHTML = events.map(event => `
        <div class="event-item">
            <div class="event-title">📅 ${escapeHtml(event.title)}</div>
            <div class="event-time">🕐 ${formatDateTime(event.start)}</div>
            ${event.description ? `<div class="event-description">${escapeHtml(event.description)}</div>` : ''}
        </div>
    `).join('');
}

function renderDashboardEvents(events) {
    const container = document.getElementById('dashboardEvents');
    const upcoming = events.slice(0, 3);
    
    if (upcoming.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📅</div><p>Nenhum evento próximo</p></div>';
        return;
    }
    
    container.innerHTML = upcoming.map(event => `
        <div class="event-item">
            <div class="event-title">📅 ${escapeHtml(event.title)}</div>
            <div class="event-time">🕐 ${formatDateTime(event.start)}</div>
        </div>
    `).join('');
}

// ========== NOTES ==========

async function loadNotes() {
    try {
        const response = await fetch(`${API_URL}/notes`);
        const data = await response.json();
        
        renderNotes(data.notes || []);
    } catch (error) {
        console.error('❌ Erro ao carregar notas:', error);
    }
}

function renderNotes(notes) {
    const container = document.getElementById('noteList');
    
    if (notes.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📝</div>
                <div class="empty-state-title">Nenhuma nota encontrada</div>
            </div>
        `;
        return;
    }
    
    container.innerHTML = notes.map(note => `
        <div class="note-item">
            <div class="note-title">📝 ${escapeHtml(note.title)}</div>
            <div class="note-content">${escapeHtml(note.content.substring(0, 200))}${note.content.length > 200 ? '...' : ''}</div>
            ${note.tags.length > 0 ? `
                <div class="note-tags">
                    ${note.tags.map(tag => `<span class="note-tag">🏷️ ${tag}</span>`).join('')}
                </div>
            ` : ''}
        </div>
    `).join('');
}

// ========== CONNECTIONS ==========

async function loadConnections() {
    try {
        const response = await fetch(`${API_URL}/connections`);
        const data = await response.json();
        
        const clients = data.clients || [];
        const stats = data.stats || {};
        
        // Atualizar estatísticas
        document.getElementById('activeClientsCount').textContent = data.active || 0;
        document.getElementById('totalRequestsCount').textContent = stats.total_requests || 0;
        
        // Contar ferramentas únicas usadas
        const allTools = new Set();
        clients.forEach(client => {
            if (client.tools_used) {
                client.tools_used.forEach(tool => allTools.add(tool));
            }
        });
        document.getElementById('toolsUsedCount').textContent = allTools.size;
        
        renderConnections(clients);
        
        console.log(`✅ ${clients.length} conexões carregadas`);
    } catch (error) {
        console.error('❌ Erro ao carregar conexões:', error);
        showToast('Erro ao carregar conexões', 'error');
    }
}

function renderConnections(clients) {
    const container = document.getElementById('connectionsList');
    
    if (clients.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📡</div>
                <div class="empty-state-title">Nenhum cliente conectado</div>
                <p>Aguardando conexões de clientes MCP...</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = clients.map(client => {
        const statusClass = client.status === 'active' ? 'active' : 'disconnected';
        const statusIcon = client.status === 'active' ? '✅' : '⚪';
        const statusText = client.status === 'active' ? 'Ativo' : 'Desconectado';
        
        const connectedTime = formatDateTime(client.connected_at);
        const lastActivity = formatDateTime(client.last_activity);
        
        return `
            <div class="connection-item ${statusClass}">
                <div class="connection-info">
                    <div class="connection-name">
                        ${getClientIcon(client.client_name)} ${escapeHtml(client.client_name)}
                        <span class="connection-status ${statusClass}">
                            ${statusIcon} ${statusText}
                        </span>
                    </div>
                    <div class="connection-details">
                        <div class="connection-detail">
                            <span>🔌</span>
                            <span>Conectado: ${connectedTime}</span>
                        </div>
                        <div class="connection-detail">
                            <span>⚡</span>
                            <span>Última atividade: ${lastActivity}</span>
                        </div>
                        <div class="connection-detail">
                            <span>📊</span>
                            <span>Requisições: ${client.requests_count || 0}</span>
                        </div>
                    </div>
                    ${client.tools_used && client.tools_used.length > 0 ? `
                        <div class="connection-tools">
                            <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 4px;">🔧 Ferramentas usadas:</div>
                            <div class="tools-list">
                                ${client.tools_used.slice(0, 10).map(tool => 
                                    `<span class="tool-badge">${escapeHtml(tool)}</span>`
                                ).join('')}
                                ${client.tools_used.length > 10 ? `<span class="tool-badge">+${client.tools_used.length - 10}</span>` : ''}
                            </div>
                        </div>
                    ` : ''}
                </div>
                <div class="connection-stats">
                    <div class="connection-metric">
                        <div class="connection-metric-value">${client.requests_count || 0}</div>
                        <div class="connection-metric-label">Requests</div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function getClientIcon(clientName) {
    const name = clientName.toLowerCase();
    if (name.includes('claude')) return '🤖';
    if (name.includes('server')) return '🖥️';
    if (name.includes('web')) return '🌐';
    if (name.includes('desktop')) return '💻';
    return '📡';
}

// ========== LOGS ==========

async function loadLogs() {
    try {
        const response = await fetch(`${API_URL}/logs?limit=100`);
        const data = await response.json();
        
        allLogs = data.logs || [];
        renderLogs();
        
    } catch (error) {
        console.error('❌ Erro ao carregar logs:', error);
    }
}

function renderLogs() {
    const container = document.getElementById('logContainer');
    let filtered = allLogs;
    
    if (currentLogFilter !== 'all') {
        filtered = allLogs.filter(log => {
            const lower = log.toLowerCase();
            if (currentLogFilter === 'error') return lower.includes('error');
            if (currentLogFilter === 'warning') return lower.includes('warning') || lower.includes('warn');
            if (currentLogFilter === 'success') return lower.includes('success');
            if (currentLogFilter === 'info') return lower.includes('info');
            return true;
        });
    }
    
    const searchTerm = document.getElementById('logSearch')?.value.toLowerCase();
    if (searchTerm) {
        filtered = filtered.filter(log => log.toLowerCase().includes(searchTerm));
    }
    
    if (filtered.length === 0) {
        container.innerHTML = '<div class="log-line log-info">Nenhum log encontrado</div>';
        return;
    }
    
    container.innerHTML = filtered.map(log => {
        let className = 'log-info';
        if (log.includes('ERROR')) className = 'log-error';
        else if (log.includes('WARNING') || log.includes('WARN')) className = 'log-warning';
        else if (log.includes('SUCCESS') || log.includes('✅')) className = 'log-success';
        
        return `<div class="log-line ${className}">${escapeHtml(log)}</div>`;
    }).join('');
    
    container.scrollTop = container.scrollHeight;
}

function clearLogFilters() {
    currentLogFilter = 'all';
    document.getElementById('logSearch').value = '';
    document.querySelectorAll('[data-log-filter]').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.logFilter === 'all');
    });
    renderLogs();
}

// ========== FORMS ==========

function setupForms() {
    // Task form
    document.getElementById('createTaskForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const taskData = {
            title: document.getElementById('taskTitle').value,
            description: document.getElementById('taskDescription').value,
            priority: document.getElementById('taskPriority').value,
            due_date: document.getElementById('taskDueDate').value
        };
        
        try {
            const response = await fetch(`${API_URL}/tasks`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(taskData)
            });
            
            if (response.ok) {
                showToast('Tarefa criada com sucesso! ✅', 'success');
                closeModals();
                document.getElementById('createTaskForm').reset();
                await loadTasks();
            }
        } catch (error) {
            console.error('❌ Erro ao criar tarefa:', error);
            showToast('Erro ao criar tarefa', 'error');
        }
    });
    
    // Event form
    document.getElementById('createEventForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        showToast('Funcionalidade em desenvolvimento', 'info');
        closeModals();
    });
    
    // Note form
    document.getElementById('createNoteForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const noteData = {
            title: document.getElementById('noteTitle').value,
            content: document.getElementById('noteContent').value,
            tags: document.getElementById('noteTags').value
        };
        
        try {
            const response = await fetch(`${API_URL}/notes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(noteData)
            });
            
            if (response.ok) {
                showToast('Nota criada com sucesso! ✅', 'success');
                closeModals();
                document.getElementById('createNoteForm').reset();
                await loadNotes();
            }
        } catch (error) {
            console.error('❌ Erro ao criar nota:', error);
            showToast('Erro ao criar nota', 'error');
        }
    });
}

// ========== FILTERS ==========

function setupFilters() {
    // Task filters
    document.querySelectorAll('.filter-btn[data-filter]').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn[data-filter]').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderTasks();
        });
    });
    
    // Log filters
    document.querySelectorAll('[data-log-filter]').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('[data-log-filter]').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentLogFilter = btn.dataset.logFilter;
            renderLogs();
        });
    });
}

// ========== SEARCH ==========

function setupSearch() {
    document.getElementById('taskSearch')?.addEventListener('input', renderTasks);
    document.getElementById('logSearch')?.addEventListener('input', renderLogs);
}

// ========== MODALS ==========

function showCreateTaskModal() {
    document.getElementById('modalOverlay').classList.add('active');
    document.getElementById('taskModal').classList.add('active');
}

function showCreateEventModal() {
    document.getElementById('modalOverlay').classList.add('active');
    document.getElementById('eventModal').classList.add('active');
}

function showCreateNoteModal() {
    document.getElementById('modalOverlay').classList.add('active');
    document.getElementById('noteModal').classList.add('active');
}

function closeModals() {
    document.getElementById('modalOverlay').classList.remove('active');
    document.querySelectorAll('.modal').forEach(m => m.classList.remove('active'));
}

// ========== TOAST ==========

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div class="toast-icon">${getToastIcon(type)}</div>
        <div class="toast-content">
            <div class="toast-title">${message}</div>
        </div>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

function getToastIcon(type) {
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    return icons[type] || 'ℹ️';
}

// ========== UTILS ==========

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getPriorityIcon(priority) {
    const icons = {
        high: '🔴',
        medium: '🟡',
        low: '🟢'
    };
    return icons[priority] || '⚪';
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('pt-BR');
}

function formatDateTime(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleString('pt-BR', { 
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Cleanup on unload
window.addEventListener('beforeunload', () => {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});
