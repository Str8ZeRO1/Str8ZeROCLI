class EmailGuardRevenue {
    constructor() {
        this.data = {
            revenue: 0,
            users: 0,
            conversions: 0,
            startDate: new Date(),
            transactions: [],
            targets: {
                week1: 100,
                month1: 1000,
                month3: 5000,
                year1: 70000
            },
            shares: {
                user: 0.70,        // Your 70%
                partner: 0.20,     // Development partner 20%
                marketing: 0.10    // Marketing budget 10%
            }
        };
        this.loadData();
        this.setupEventListeners();
    }

    loadData() {
        const saved = localStorage.getItem('emailguard-revenue');
        if (saved) {
            this.data = { ...this.data, ...JSON.parse(saved) };
        }
    }

    saveData() {
        localStorage.setItem('emailguard-revenue', JSON.stringify(this.data));
    }

    addTransaction(amount, type = 'subscription', userId = null) {
        const transaction = {
            id: Date.now(),
            amount: parseFloat(amount),
            type: type,
            userId: userId || 'demo-' + Math.random().toString(36).substr(2, 9),
            timestamp: new Date().toISOString(),
            userShare: parseFloat(amount) * this.data.shares.user,
            partnerShare: parseFloat(amount) * this.data.shares.partner,
            marketingShare: parseFloat(amount) * this.data.shares.marketing
        };

        this.data.transactions.push(transaction);
        this.data.revenue += transaction.amount;
        
        if (type === 'subscription') {
            this.data.users += 1;
        }

        this.updateConversions();
        this.saveData();
        this.updateDisplay();
        
        return transaction;
    }

    updateConversions() {
        const visits = this.data.users + Math.floor(this.data.users * 8); // Estimate visits
        this.data.conversions = visits > 0 ? (this.data.users / visits) * 100 : 0;
    }

    getYourShare() {
        return this.data.revenue * this.data.shares.user;
    }

    getPartnerShare() {
        return this.data.revenue * this.data.shares.partner;
    }

    getMarketingBudget() {
        return this.data.revenue * this.data.shares.marketing;
    }

    getProjections() {
        const daysRunning = Math.max(1, Math.ceil((new Date() - new Date(this.data.startDate)) / (1000 * 60 * 60 * 24)));
        const dailyAverage = this.data.revenue / daysRunning;
        
        return {
            daily: dailyAverage,
            weekly: dailyAverage * 7,
            monthly: dailyAverage * 30,
            yearly: dailyAverage * 365,
            nextWeek: this.getYourShare() + (dailyAverage * this.data.shares.user * 7),
            nextMonth: this.getYourShare() + (dailyAverage * this.data.shares.user * 30)
        };
    }

    getTargetProgress() {
        const yourShare = this.getYourShare();
        return {
            week1: {
                target: this.data.targets.week1 * this.data.shares.user,
                current: yourShare,
                progress: (yourShare / (this.data.targets.week1 * this.data.shares.user)) * 100
            },
            month1: {
                target: this.data.targets.month1 * this.data.shares.user,
                current: yourShare,
                progress: (yourShare / (this.data.targets.month1 * this.data.shares.user)) * 100
            },
            month3: {
                target: this.data.targets.month3 * this.data.shares.user,
                current: yourShare,
                progress: (yourShare / (this.data.targets.month3 * this.data.shares.user)) * 100
            },
            year1: {
                target: this.data.targets.year1 * this.data.shares.user,
                current: yourShare,
                progress: (yourShare / (this.data.targets.year1 * this.data.shares.user)) * 100
            }
        };
    }

    getRecentTransactions(limit = 10) {
        return this.data.transactions
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
            .slice(0, limit);
    }

    generateReport() {
        const projections = this.getProjections();
        const progress = this.getTargetProgress();
        
        return {
            summary: {
                totalRevenue: this.data.revenue,
                yourShare: this.getYourShare(),
                partnerShare: this.getPartnerShare(),
                marketingBudget: this.getMarketingBudget(),
                activeUsers: this.data.users,
                conversionRate: this.data.conversions,
                transactionCount: this.data.transactions.length
            },
            projections,
            progress,
            recentTransactions: this.getRecentTransactions(5)
        };
    }

    updateDisplay() {
        // Update DOM elements if they exist
        const elements = {
            revenue: document.getElementById('revenue'),
            users: document.getElementById('users'),
            conversions: document.getElementById('conversions'),
            yourShare: document.getElementById('your-share'),
            partnerShare: document.getElementById('partner-share'),
            marketingBudget: document.getElementById('marketing-budget')
        };

        if (elements.revenue) {
            elements.revenue.textContent = '$' + this.getYourShare().toFixed(2);
        }
        if (elements.users) {
            elements.users.textContent = this.data.users;
        }
        if (elements.conversions) {
            elements.conversions.textContent = this.data.conversions.toFixed(1) + '%';
        }
        if (elements.yourShare) {
            elements.yourShare.textContent = '$' + this.getYourShare().toFixed(2);
        }
        if (elements.partnerShare) {
            elements.partnerShare.textContent = '$' + this.getPartnerShare().toFixed(2);
        }
        if (elements.marketingBudget) {
            elements.marketingBudget.textContent = '$' + this.getMarketingBudget().toFixed(2);
        }
    }

    setupEventListeners() {
        // Listen for demo payments
        document.addEventListener('emailguard-payment', (event) => {
            this.addTransaction(event.detail.amount, event.detail.type);
        });

        // Auto-update display every 5 seconds
        setInterval(() => {
            this.updateDisplay();
        }, 5000);
    }

    // Demo mode functions
    simulateActivity() {
        setInterval(() => {
            if (Math.random() > 0.85) {
                const amount = Math.random() > 0.7 ? 4.99 : 9.99; // Pro or Premium
                this.addTransaction(amount, 'subscription');
            }
        }, 10000);
    }

    reset() {
        this.data = {
            revenue: 0,
            users: 0,
            conversions: 0,
            startDate: new Date(),
            transactions: [],
            targets: this.data.targets,
            shares: this.data.shares
        };
        this.saveData();
        this.updateDisplay();
    }
}

// Initialize global revenue tracker
window.emailGuardRevenue = new EmailGuardRevenue();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EmailGuardRevenue;
}