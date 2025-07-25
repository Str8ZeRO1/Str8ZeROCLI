import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox, 
                            QTabWidget, QProgressBar, QFrame, QGridLayout, QSpacerItem,
                            QSizePolicy, QCheckBox, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon

# Add parent directory to path to import CLI modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cli.market_analysis import MarketAnalyzer
from cli.app_generator import AppGenerator
from cli.str8zero_core import Str8ZeroCore

class WorkerThread(QThread):
    """Worker thread to run operations without freezing UI"""
    update_signal = pyqtSignal(dict)
    finished_signal = pyqtSignal(dict)
    
    def __init__(self, operation, params):
        super().__init__()
        self.operation = operation
        self.params = params
        
    def run(self):
        try:
            result = {}
            
            if self.operation == "market_analysis":
                analyzer = MarketAnalyzer()
                result = analyzer.analyze_market(
                    category=self.params.get("category"),
                    keywords=self.params.get("keywords")
                )
                self.update_signal.emit({"status": "Analyzing market data..."})
                
            elif self.operation == "generate_app":
                generator = AppGenerator()
                result = generator.generate_app(
                    app_name=self.params.get("app_name"),
                    app_type=self.params.get("app_type"),
                    features=self.params.get("features"),
                    platform=self.params.get("platform")
                )
                self.update_signal.emit({"status": "Generating app code..."})
                
            elif self.operation == "build":
                core = Str8ZeroCore(
                    user_context=self.params.get("profile", "default"),
                    prompt=self.params.get("prompt")
                )
                self.update_signal.emit({"status": "Analyzing prompt..."})
                result = core.build()
                
            self.finished_signal.emit({"operation": self.operation, "result": result})
            
        except Exception as e:
            self.finished_signal.emit({"operation": self.operation, "error": str(e)})

class Str8ZeroCockpit(QMainWindow):
    """Main cockpit interface for Str8ZeROCLI"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Str8ZeRO Command Cockpit")
        self.setMinimumSize(1200, 800)
        
        # Set dark theme
        self.set_dark_theme()
        
        # Initialize UI
        self.init_ui()
        
        # Status updates
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(5000)  # Update every 5 seconds
        
    def set_dark_theme(self):
        """Set dark theme for the application"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(dark_palette)
        
    def init_ui(self):
        """Initialize the user interface"""
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #1E1E1E; border-radius: 10px;")
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("Str8ZeRO Command Cockpit")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #00F0FF;")
        
        status_label = QLabel("Status: Ready")
        status_label.setStyleSheet("color: #00FF00;")
        self.status_label = status_label
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        
        # Tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #444; 
                background-color: #2D2D2D;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #1E1E1E;
                color: white;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #2D2D2D;
                border-bottom: 2px solid #00F0FF;
            }
        """)
        
        # Create tabs
        market_tab = self.create_market_tab()
        build_tab = self.create_build_tab()
        generate_tab = self.create_generate_tab()
        monitor_tab = self.create_monitor_tab()
        
        # Add tabs
        tab_widget.addTab(market_tab, "Market Analysis")
        tab_widget.addTab(build_tab, "Build App")
        tab_widget.addTab(generate_tab, "Generate Code")
        tab_widget.addTab(monitor_tab, "Monitor")
        
        # Add widgets to main layout
        main_layout.addWidget(header_frame)
        main_layout.addWidget(tab_widget, 1)
        
        # Set main widget
        self.setCentralWidget(main_widget)
        
    def create_market_tab(self):
        """Create market analysis tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Controls
        controls_frame = QFrame()
        controls_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 5px;")
        controls_layout = QGridLayout(controls_frame)
        
        # Category
        controls_layout.addWidget(QLabel("Category:"), 0, 0)
        category_combo = QComboBox()
        category_combo.addItems(["productivity", "finance", "lifestyle", "health", 
                                "utilities", "social", "education", "entertainment"])
        controls_layout.addWidget(category_combo, 0, 1)
        self.category_combo = category_combo
        
        # Keywords
        controls_layout.addWidget(QLabel("Keywords:"), 1, 0)
        keywords_input = QLineEdit()
        keywords_input.setPlaceholderText("Enter keywords separated by commas")
        controls_layout.addWidget(keywords_input, 1, 1)
        self.keywords_input = keywords_input
        
        # Analyze button
        analyze_button = QPushButton("Analyze Market")
        analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #00A3FF;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0078D7;
            }
        """)
        analyze_button.clicked.connect(self.analyze_market)
        controls_layout.addWidget(analyze_button, 2, 0, 1, 2)
        
        # Results
        results_frame = QFrame()
        results_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 5px;")
        results_layout = QVBoxLayout(results_frame)
        
        results_label = QLabel("Market Analysis Results")
        results_label.setFont(QFont("Arial", 12, QFont.Bold))
        results_layout.addWidget(results_label)
        
        results_text = QTextEdit()
        results_text.setReadOnly(True)
        results_text.setStyleSheet("background-color: #1E1E1E; color: white; border-radius: 5px;")
        results_layout.addWidget(results_text)
        self.market_results_text = results_text
        
        # Add to layout
        layout.addWidget(controls_frame)
        layout.addWidget(results_frame, 1)
        
        return tab
        
    def create_build_tab(self):
        """Create build app tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Prompt input
        prompt_frame = QFrame()
        prompt_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 5px;")
        prompt_layout = QVBoxLayout(prompt_frame)
        
        prompt_label = QLabel("Enter your app idea:")
        prompt_label.setFont(QFont("Arial", 12, QFont.Bold))
        prompt_layout.addWidget(prompt_label)
        
        prompt_input = QTextEdit()
        prompt_input.setPlaceholderText("Describe your app idea in detail...")
        prompt_input.setStyleSheet("background-color: #1E1E1E; color: white; border-radius: 5px;")
        prompt_layout.addWidget(prompt_input)
        self.prompt_input = prompt_input
        
        # Options
        options_frame = QFrame()
        options_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 5px;")
        options_layout = QGridLayout(options_frame)
        
        # Platform
        options_layout.addWidget(QLabel("Platform:"), 0, 0)
        platform_combo = QComboBox()
        platform_combo.addItems(["all", "ios", "android", "web"])
        options_layout.addWidget(platform_combo, 0, 1)
        self.build_platform_combo = platform_combo
        
        # Profile
        options_layout.addWidget(QLabel("Profile:"), 1, 0)
        profile_combo = QComboBox()
        profile_combo.addItems(["default", "development", "creative"])
        options_layout.addWidget(profile_combo, 1, 1)
        self.profile_combo = profile_combo
        
        # Explain
        options_layout.addWidget(QLabel("Detailed explanation:"), 2, 0)
        explain_check = QCheckBox()
        options_layout.addWidget(explain_check, 2, 1)
        self.explain_check = explain_check
        
        # Build button
        build_button = QPushButton("Build App")
        build_button.setStyleSheet("""
            QPushButton {
                background-color: #00A3FF;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0078D7;
            }
        """)
        build_button.clicked.connect(self.build_app)
        options_layout.addWidget(build_button, 3, 0, 1, 2)
        
        # Results
        results_frame = QFrame()
        results_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 5px;")
        results_layout = QVBoxLayout(results_frame)
        
        results_label = QLabel("Build Results")
        results_label.setFont(QFont("Arial", 12, QFont.Bold))
        results_layout.addWidget(results_label)
        
        results_text = QTextEdit()
        results_text.setReadOnly(True)
        results_text.setStyleSheet("background-color: #1E1E1E; color: white; border-radius: 5px;")
        results_layout.addWidget(results_text)
        self.build_results_text = results_text
        
        # Add to layout
        layout.addWidget(prompt_frame)
        layout.addWidget(options_frame)
        layout.addWidget(results_frame, 1)
        
        return tab
        
    def create_generate_tab(self):
        """Create generate code tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # App details
        details_frame = QFrame()
        details_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 5px;")
        details_layout = QGridLayout(details_frame)
        
        # App name
        details_layout.addWidget(QLabel("App Name:"), 0, 0)
        app_name_input = QLineEdit()
        app_name_input.setPlaceholderText("Enter app name")
        details_layout.addWidget(app_name_input, 0, 1)
        self.app_name_input = app_name_input
        
        # App type
        details_layout.addWidget(QLabel("App Type:"), 1, 0)
        app_type_combo = QComboBox()
        app_type_combo.addItems(["bill_monitor", "scheduler", "donation_pickup", "generic"])
        details_layout.addWidget(app_type_combo, 1, 1)
        self.app_type_combo = app_type_combo
        
        # Features
        details_layout.addWidget(QLabel("Features:"), 2, 0)
        features_input = QLineEdit()
        features_input.setPlaceholderText("Enter features separated by commas")
        details_layout.addWidget(features_input, 2, 1)
        self.features_input = features_input
        
        # Platform
        details_layout.addWidget(QLabel("Platform:"), 3, 0)
        platform_combo = QComboBox()
        platform_combo.addItems(["all", "ios", "android", "web"])
        details_layout.addWidget(platform_combo, 3, 1)
        self.gen_platform_combo = platform_combo
        
        # Generate button
        generate_button = QPushButton("Generate Code")
        generate_button.setStyleSheet("""
            QPushButton {
                background-color: #00A3FF;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0078D7;
            }
        """)
        generate_button.clicked.connect(self.generate_code)
        details_layout.addWidget(generate_button, 4, 0, 1, 2)
        
        # Results
        results_frame = QFrame()
        results_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 5px;")
        results_layout = QVBoxLayout(results_frame)
        
        results_label = QLabel("Generation Results")
        results_label.setFont(QFont("Arial", 12, QFont.Bold))
        results_layout.addWidget(results_label)
        
        results_text = QTextEdit()
        results_text.setReadOnly(True)
        results_text.setStyleSheet("background-color: #1E1E1E; color: white; border-radius: 5px;")
        results_layout.addWidget(results_text)
        self.generate_results_text = results_text
        
        # Add to layout
        layout.addWidget(details_frame)
        layout.addWidget(results_frame, 1)
        
        return tab
        
    def create_monitor_tab(self):
        """Create monitor tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Stats
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 5px;")
        stats_layout = QGridLayout(stats_frame)
        
        # Apps generated
        stats_layout.addWidget(QLabel("Apps Generated:"), 0, 0)
        apps_generated_label = QLabel("0")
        apps_generated_label.setStyleSheet("color: #00F0FF; font-weight: bold;")
        stats_layout.addWidget(apps_generated_label, 0, 1)
        self.apps_generated_label = apps_generated_label
        
        # Market analyses
        stats_layout.addWidget(QLabel("Market Analyses:"), 1, 0)
        analyses_label = QLabel("0")
        analyses_label.setStyleSheet("color: #00F0FF; font-weight: bold;")
        stats_layout.addWidget(analyses_label, 1, 1)
        self.analyses_label = analyses_label
        
        # Estimated revenue
        stats_layout.addWidget(QLabel("Est. Monthly Revenue:"), 2, 0)
        revenue_label = QLabel("$0.00")
        revenue_label.setStyleSheet("color: #00F0FF; font-weight: bold;")
        stats_layout.addWidget(revenue_label, 2, 1)
        self.revenue_label = revenue_label
        
        # Log
        log_frame = QFrame()
        log_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 5px;")
        log_layout = QVBoxLayout(log_frame)
        
        log_label = QLabel("Activity Log")
        log_label.setFont(QFont("Arial", 12, QFont.Bold))
        log_layout.addWidget(log_label)
        
        log_text = QTextEdit()
        log_text.setReadOnly(True)
        log_text.setStyleSheet("background-color: #1E1E1E; color: white; border-radius: 5px;")
        log_layout.addWidget(log_text)
        self.log_text = log_text
        
        # Add initial log entry
        self.add_log_entry("System initialized")
        
        # Add to layout
        layout.addWidget(stats_frame)
        layout.addWidget(log_frame, 1)
        
        return tab
    
    def analyze_market(self):
        """Analyze market based on user input"""
        category = self.category_combo.currentText()
        keywords_text = self.keywords_input.text()
        keywords = keywords_text.split(",") if keywords_text else None
        
        self.status_label.setText("Status: Analyzing market...")
        self.add_log_entry(f"Starting market analysis for category: {category}")
        
        # Start worker thread
        self.worker = WorkerThread("market_analysis", {
            "category": category,
            "keywords": keywords
        })
        self.worker.update_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.handle_result)
        self.worker.start()
    
    def build_app(self):
        """Build app based on user prompt"""
        prompt = self.prompt_input.toPlainText()
        platform = self.build_platform_combo.currentText()
        profile = self.profile_combo.currentText()
        explain = self.explain_check.isChecked()
        
        if not prompt:
            self.build_results_text.setText("Please enter an app idea.")
            return
        
        self.status_label.setText("Status: Building app...")
        self.add_log_entry(f"Starting app build for prompt: {prompt[:50]}...")
        
        # Start worker thread
        self.worker = WorkerThread("build", {
            "prompt": prompt,
            "platform": platform,
            "profile": profile,
            "explain": explain
        })
        self.worker.update_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.handle_result)
        self.worker.start()
    
    def generate_code(self):
        """Generate code based on user input"""
        app_name = self.app_name_input.text()
        app_type = self.app_type_combo.currentText()
        features_text = self.features_input.text()
        platform = self.gen_platform_combo.currentText()
        
        if not app_name:
            self.generate_results_text.setText("Please enter an app name.")
            return
        
        features = features_text.split(",") if features_text else None
        
        self.status_label.setText("Status: Generating code...")
        self.add_log_entry(f"Starting code generation for app: {app_name}")
        
        # Start worker thread
        self.worker = WorkerThread("generate_app", {
            "app_name": app_name,
            "app_type": app_type,
            "features": features,
            "platform": platform
        })
        self.worker.update_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.handle_result)
        self.worker.start()
    
    def update_progress(self, data):
        """Update progress based on worker thread signal"""
        if "status" in data:
            self.status_label.setText(f"Status: {data['status']}")
    
    def handle_result(self, data):
        """Handle result from worker thread"""
        operation = data.get("operation")
        
        if "error" in data:
            error_message = data.get("error")
            if operation == "market_analysis":
                self.market_results_text.setText(f"Error: {error_message}")
            elif operation == "build":
                self.build_results_text.setText(f"Error: {error_message}")
            elif operation == "generate_app":
                self.generate_results_text.setText(f"Error: {error_message}")
            
            self.status_label.setText("Status: Error")
            self.add_log_entry(f"Error in {operation}: {error_message}")
            return
        
        result = data.get("result", {})
        
        if operation == "market_analysis":
            # Update market analysis results
            opportunities = result.get("opportunities", [])
            competition = result.get("competition_analysis", {})
            
            output = f"Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            output += f"Apps analyzed: {result.get('apps_analyzed', 0)}\n"
            output += f"Competition level: {competition.get('level', 'unknown').upper()}\n\n"
            
            output += f"Opportunities found: {len(opportunities)}\n\n"
            
            for i, opp in enumerate(opportunities):
                output += f"{i+1}. {opp.get('type', '').replace('_', ' ').title()}\n"
                output += f"   {opp.get('description', '')}\n"
                output += f"   Potential: {opp.get('potential', '').upper()}\n\n"
            
            self.market_results_text.setText(output)
            self.analyses_label.setText(str(int(self.analyses_label.text()) + 1))
            
        elif operation == "build":
            # Update build results
            intent = result.get("intent", {})
            logic = result.get("logic", {})
            monetization = result.get("monetization", {})
            
            output = f"Build completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            output += f"App Type: {logic.get('app_type', 'unknown')}\n"
            output += f"Domain: {intent.get('domain', 'unknown')}\n"
            output += f"Features: {', '.join(logic.get('features', []))}\n\n"
            
            output += f"Monetization Model: {monetization.get('model', 'unknown')}\n"
            revenue = monetization.get("revenue_potential", {})
            output += f"Estimated Monthly Revenue: ${revenue.get('estimated_monthly_revenue', 0)}\n"
            output += f"Estimated Annual Revenue: ${revenue.get('estimated_annual_revenue', 0)}\n\n"
            
            output += f"Deployment Targets: {', '.join(result.get('deployment', {}).get('targets', []))}\n"
            
            self.build_results_text.setText(output)
            self.apps_generated_label.setText(str(int(self.apps_generated_label.text()) + 1))
            
            # Update revenue
            current_revenue = float(self.revenue_label.text().replace("$", ""))
            new_revenue = current_revenue + revenue.get('estimated_monthly_revenue', 0)
            self.revenue_label.setText(f"${new_revenue:.2f}")
            
        elif operation == "generate_app":
            # Update generate results
            output = f"Code generation completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            output += f"App Name: {result.get('app_name', 'unknown')}\n"
            output += f"Files Generated: {result.get('files_generated', 0)}\n"
            output += f"Platforms: {', '.join(result.get('platforms', []))}\n\n"
            
            output += f"App Directory: {result.get('app_dir', '')}\n"
            
            self.generate_results_text.setText(output)
            self.apps_generated_label.setText(str(int(self.apps_generated_label.text()) + 1))
        
        self.status_label.setText("Status: Ready")
        self.add_log_entry(f"Completed {operation}")
    
    def add_log_entry(self, message):
        """Add entry to log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def update_status(self):
        """Update status periodically"""
        # This would normally check system status, running jobs, etc.
        pass

def main():
    app = QApplication(sys.argv)
    window = Str8ZeroCockpit()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()