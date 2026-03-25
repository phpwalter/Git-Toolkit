// This file will contain the JavaScript for the new UI.
document.addEventListener('DOMContentLoaded', function() {
    // Initialize MDC components
    const drawer = mdc.drawer.MDCDrawer.attachTo(document.querySelector('.mdc-drawer'));
    const topAppBar = mdc.topAppBar.MDCTopAppBar.attachTo(document.querySelector('.mdc-top-app-bar'));
    const fab = new mdc.ripple.MDCRipple(document.querySelector('.mdc-fab'));

    topAppBar.setScrollTarget(document.getElementById('main-content'));
    topAppBar.listen('MDCTopAppBar:nav', () => {
        drawer.open = !drawer.open;
    });

    // --- FAKE DATA ---
    const healthData = {
        uptime: "99.98%",
        latency: "120ms",
        alerts: [
            { severity: 'error', message: 'Production deployment failed' },
            { severity: 'warning', message: 'High memory usage on runner-2' },
            { severity: 'success', message: 'All systems operational' }
        ]
    };

    const repoStatusData = [
        { name: 'webapp-frontend', branch: 'main', status: 'Clean' },
        { name: 'backend-api', branch: 'develop', status: 'Dirty' },
        { name: 'mobile-app', branch: 'feature/new-login', status: 'Clean' }
    ];

    const workflowStatsData = [
        { name: 'Build & Test', success: 95, failure: 5 },
        { name: 'Staging Deploy', success: 100, failure: 0 },
        { name: 'Production Deploy', success: 80, failure: 20 }
    ];

    const securityAuditData = {
        vulnerabilities: 3,
        passed: 124,
        failed: 3
    };

    const userActivityData = [
        { user: 'Alice', action: 'pushed to backend-api', time: '15m ago' },
        { user: 'Bob', action: 'merged PR #123', time: '1h ago' },
        { user: 'Charlie', action: 'commented on issue #45', time: '3h ago' }
    ];

    // --- RENDER FUNCTIONS ---
    function renderHealthOverview() {
        document.getElementById('uptime').textContent = healthData.uptime;
        document.getElementById('latency').textContent = healthData.latency;
        const alertsList = document.getElementById('alerts-list');
        alertsList.innerHTML = healthData.alerts.map(alert => `
            <div class="alert-item ${alert.severity}">
                <i class="material-icons">${alert.severity === 'error' ? 'error' : alert.severity === 'warning' ? 'warning' : 'check_circle'}</i>
                <span>${alert.message}</span>
            </div>
        `).join('');
    }

    function renderRepoStatus() {
        const repoList = document.getElementById('repo-list');
        repoList.innerHTML = repoStatusData.map(repo => `
            <div class="repo-item repo-status-grid">
                <span>${repo.name} <small>(${repo.branch})</small></span>
                <span style="color: ${repo.status === 'Clean' ? 'green' : 'orange'};">${repo.status}</span>
                <div class="repo-actions">
                    <button class="mdc-button">Push</button>
                    <button class="mdc-button">Pull</button>
                </div>
            </div>
        `).join('');
    }

    function renderWorkflowStats() {
        const workflowList = document.getElementById('workflow-list');
        workflowList.innerHTML = workflowStatsData.map(wf => `
            <tr>
                <td>${wf.name}</td>
                <td>${wf.success}%</td>
                <td>${wf.failure}%</td>
            </tr>
        `).join('');
    }

    function renderSecurityAudit() {
        document.getElementById('vulnerabilities').textContent = securityAuditData.vulnerabilities;
        // Chart rendering will go here
    }

    function renderUserActivity() {
        const activityList = document.getElementById('user-activity-list');
        activityList.innerHTML = userActivityData.map(act => `
            <div class="user-activity-item">
                <i class="material-icons">account_circle</i>
                <div>
                    <strong>${act.user}</strong> ${act.action}<br>
                    <small>${act.time}</small>
                </div>
            </div>
        `).join('');
    }

    // --- CHARTING ---
    function renderCharts() {
        // Using Chart.js for simplicity
        const securityCtx = document.getElementById('security-chart').getContext('2d');
        new Chart(securityCtx, {
            type: 'doughnut',
            data: {
                labels: ['Passed', 'Failed'],
                datasets: [{
                    data: [securityAuditData.passed, securityAuditData.failed],
                    backgroundColor: ['#4caf50', '#f44336'],
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: { display: false }
            }
        });

        const workflowCtx = document.getElementById('workflow-chart').getContext('2d');
        new Chart(workflowCtx, {
            type: 'bar',
            data: {
                labels: workflowStatsData.map(wf => wf.name),
                datasets: [
                    {
                        label: 'Success',
                        data: workflowStatsData.map(wf => wf.success),
                        backgroundColor: '#4caf50'
                    },
                    {
                        label: 'Failure',
                        data: workflowStatsData.map(wf => wf.failure),
                        backgroundColor: '#f44336'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { stacked: true },
                    y: { stacked: true, beginAtZero: true }
                }
            }
        });
    }


    // --- INITIAL RENDER ---
    renderHealthOverview();
    renderRepoStatus();
    renderWorkflowStats();
    renderSecurityAudit();
    renderUserActivity();
    renderCharts();
});
