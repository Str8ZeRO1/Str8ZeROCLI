#!/usr/bin/env python3
"""
App Generator Module
-------------------
Generates complete app code based on market analysis and user requirements.
"""
import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class AppGenerator:
    """Generates app code and project structure"""
    
    def __init__(self):
        """Initialize the app generator"""
        self.templates_path = os.path.join(Path.home(), "Str8ZeROCLI", "templates")
        self.output_path = os.path.join(Path.home(), "Str8ZeROCLI", "generated_apps")
        
        # Ensure directories exist
        os.makedirs(self.templates_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)
    
    def generate_app(self, app_name, app_type, features=None, platform="all"):
        """
        Generate a complete app based on specifications
        
        Args:
            app_name (str): Name of the app
            app_type (str): Type of app (e.g., bill_monitor, scheduler)
            features (list, optional): List of features to include
            platform (str, optional): Target platform (ios, android, web, all)
            
        Returns:
            dict: Result of app generation with paths and stats
        """
        # Sanitize app name for file system
        safe_name = "".join(c if c.isalnum() else "_" for c in app_name)
        app_dir = os.path.join(self.output_path, safe_name)
        
        # Create app directory
        os.makedirs(app_dir, exist_ok=True)
        
        # Determine which platforms to generate
        platforms = []
        if platform == "all" or platform == "web":
            platforms.append("web")
        if platform == "all" or platform == "ios":
            platforms.append("ios")
        if platform == "all" or platform == "android":
            platforms.append("android")
        
        # Generate app structure for each platform
        generated_files = []
        for plat in platforms:
            plat_files = self._generate_platform(app_dir, safe_name, app_type, plat, features)
            generated_files.extend(plat_files)
        
        # Generate shared files
        shared_files = self._generate_shared_files(app_dir, safe_name, app_type, features)
        generated_files.extend(shared_files)
        
        # Generate README
        readme_path = os.path.join(app_dir, "README.md")
        with open(readme_path, 'w') as f:
            f.write(self._generate_readme(app_name, app_type, features, platforms))
        generated_files.append(readme_path)
        
        return {
            "app_name": app_name,
            "app_dir": app_dir,
            "platforms": platforms,
            "files_generated": len(generated_files),
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_platform(self, app_dir, app_name, app_type, platform, features):
        """Generate platform-specific code"""
        platform_dir = os.path.join(app_dir, platform)
        os.makedirs(platform_dir, exist_ok=True)
        
        generated_files = []
        
        if platform == "web":
            # Generate web app structure
            files = self._generate_web_app(platform_dir, app_name, app_type, features)
            generated_files.extend(files)
        elif platform == "ios":
            # Generate iOS app structure
            files = self._generate_ios_app(platform_dir, app_name, app_type, features)
            generated_files.extend(files)
        elif platform == "android":
            # Generate Android app structure
            files = self._generate_android_app(platform_dir, app_name, app_type, features)
            generated_files.extend(files)
        
        return generated_files
    
    def _generate_web_app(self, platform_dir, app_name, app_type, features):
        """Generate web app code"""
        generated_files = []
        
        # Create basic web app structure
        dirs = ["src", "src/components", "src/pages", "src/assets", "public"]
        for d in dirs:
            os.makedirs(os.path.join(platform_dir, d), exist_ok=True)
        
        # Generate index.html
        index_path = os.path.join(platform_dir, "public", "index.html")
        with open(index_path, 'w') as f:
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name}</title>
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <div id="root"></div>
    <script src="/bundle.js"></script>
</body>
</html>""")
        generated_files.append(index_path)
        
        # Generate package.json
        package_path = os.path.join(platform_dir, "package.json")
        with open(package_path, 'w') as f:
            f.write(f"""{{
  "name": "{app_name.lower().replace(' ', '-')}",
  "version": "1.0.0",
  "description": "Generated by Str8ZeROCLI",
  "main": "src/index.js",
  "scripts": {{
    "start": "webpack-dev-server --mode development",
    "build": "webpack --mode production"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.10.0"
  }},
  "devDependencies": {{
    "@babel/core": "^7.21.4",
    "@babel/preset-env": "^7.21.4",
    "@babel/preset-react": "^7.18.6",
    "babel-loader": "^9.1.2",
    "css-loader": "^6.7.3",
    "html-webpack-plugin": "^5.5.1",
    "style-loader": "^3.3.2",
    "webpack": "^5.80.0",
    "webpack-cli": "^5.0.2",
    "webpack-dev-server": "^4.13.3"
  }}
}}""")
        generated_files.append(package_path)
        
        # Generate app-specific components based on app_type
        if app_type == "bill_monitor":
            components = ["BillUpload", "BillList", "AnomalyDetector", "BillChart"]
        elif app_type == "scheduler":
            components = ["Calendar", "AppointmentForm", "ReminderList", "TimeSlotPicker"]
        else:
            components = ["Dashboard", "SettingsPanel", "UserProfile"]
        
        # Add feature-specific components
        if features:
            for feature in features:
                component_name = "".join(word.capitalize() for word in feature.split("_"))
                components.append(component_name)
        
        # Generate component files
        for component in components:
            component_path = os.path.join(platform_dir, "src", "components", f"{component}.js")
            with open(component_path, 'w') as f:
                f.write(f"""import React from 'react';

function {component}() {{
  return (
    <div className="{component.lower()}">
      <h2>{component}</h2>
      {/* Generated by Str8ZeROCLI */}
    </div>
  );
}}

export default {component};""")
            generated_files.append(component_path)
        
        # Generate main index.js
        index_js_path = os.path.join(platform_dir, "src", "index.js")
        with open(index_js_path, 'w') as f:
            f.write(f"""import React from 'react';
import ReactDOM from 'react-dom/client';
import {{ BrowserRouter as Router, Routes, Route }} from 'react-router-dom';
import Dashboard from './pages/Dashboard';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={{<Dashboard />}} />
      </Routes>
    </Router>
  </React.StrictMode>
);""")
        generated_files.append(index_js_path)
        
        # Generate Dashboard page
        dashboard_path = os.path.join(platform_dir, "src", "pages", "Dashboard.js")
        with open(dashboard_path, 'w') as f:
            imports = "\n".join([f"import {comp} from '../components/{comp}';" for comp in components[:3]])
            components_jsx = "\n      ".join([f"<{comp} />" for comp in components[:3]])
            
            f.write(f"""import React from 'react';
{imports}

function Dashboard() {{
  return (
    <div className="dashboard">
      <h1>{app_name}</h1>
      {components_jsx}
    </div>
  );
}}

export default Dashboard;""")
        generated_files.append(dashboard_path)
        
        return generated_files
    
    def _generate_ios_app(self, platform_dir, app_name, app_type, features):
        """Generate iOS app code"""
        generated_files = []
        
        # Create basic iOS app structure
        dirs = ["Sources", "Sources/Views", "Sources/Models", "Resources"]
        for d in dirs:
            os.makedirs(os.path.join(platform_dir, d), exist_ok=True)
        
        # Generate AppDelegate.swift
        app_delegate_path = os.path.join(platform_dir, "Sources", "AppDelegate.swift")
        with open(app_delegate_path, 'w') as f:
            f.write(f"""import UIKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {{
    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {{
        // Generated by Str8ZeROCLI
        return true
    }}
}}""")
        generated_files.append(app_delegate_path)
        
        # Generate ContentView.swift
        content_view_path = os.path.join(platform_dir, "Sources", "Views", "ContentView.swift")
        with open(content_view_path, 'w') as f:
            f.write(f"""import SwiftUI

struct ContentView: View {{
    var body: some View {{
        NavigationView {{
            VStack {{
                Text("{app_name}")
                    .font(.largeTitle)
                    .padding()
                
                // Generated by Str8ZeROCLI
            }}
            .navigationTitle("{app_name}")
        }}
    }}
}}

struct ContentView_Previews: PreviewProvider {{
    static var previews: some View {{
        ContentView()
    }}
}}""")
        generated_files.append(content_view_path)
        
        # Generate Info.plist
        info_plist_path = os.path.join(platform_dir, "Resources", "Info.plist")
        with open(info_plist_path, 'w') as f:
            f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>$(DEVELOPMENT_LANGUAGE)</string>
    <key>CFBundleExecutable</key>
    <string>$(EXECUTABLE_NAME)</string>
    <key>CFBundleIdentifier</key>
    <string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundlePackageType</key>
    <string>$(PRODUCT_BUNDLE_PACKAGE_TYPE)</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>UIApplicationSceneManifest</key>
    <dict>
        <key>UIApplicationSupportsMultipleScenes</key>
        <false/>
    </dict>
    <key>UILaunchScreen</key>
    <dict/>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>armv7</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
    </array>
</dict>
</plist>""")
        generated_files.append(info_plist_path)
        
        return generated_files
    
    def _generate_android_app(self, platform_dir, app_name, app_type, features):
        """Generate Android app code"""
        generated_files = []
        
        # Create basic Android app structure
        dirs = [
            "app/src/main/java/com/str8zero/app",
            "app/src/main/res/layout",
            "app/src/main/res/values"
        ]
        for d in dirs:
            os.makedirs(os.path.join(platform_dir, d), exist_ok=True)
        
        # Generate MainActivity.java
        main_activity_path = os.path.join(platform_dir, "app/src/main/java/com/str8zero/app", "MainActivity.java")
        with open(main_activity_path, 'w') as f:
            f.write(f"""package com.str8zero.app;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // Generated by Str8ZeROCLI
    }}
}}""")
        generated_files.append(main_activity_path)
        
        # Generate activity_main.xml
        layout_path = os.path.join(platform_dir, "app/src/main/res/layout", "activity_main.xml")
        with open(layout_path, 'w') as f:
            f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{app_name}"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>""")
        generated_files.append(layout_path)
        
        # Generate strings.xml
        strings_path = os.path.join(platform_dir, "app/src/main/res/values", "strings.xml")
        with open(strings_path, 'w') as f:
            f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{app_name}</string>
</resources>""")
        generated_files.append(strings_path)
        
        return generated_files
    
    def _generate_shared_files(self, app_dir, app_name, app_type, features):
        """Generate shared files for the app"""
        generated_files = []
        
        # Generate .gitignore
        gitignore_path = os.path.join(app_dir, ".gitignore")
        with open(gitignore_path, 'w') as f:
            f.write("""# Node.js
node_modules/
npm-debug.log
yarn-error.log

# iOS
ios/Pods/
ios/build/
*.pbxuser
*.mode1v3
*.mode2v3
*.perspectivev3
*.xcuserstate
project.xcworkspace/
xcuserdata/

# Android
android/app/build/
android/build/
android/.gradle/
android/local.properties
android/*.iml

# General
.DS_Store
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Build
/dist
/build""")
        generated_files.append(gitignore_path)
        
        # Generate package.json for the root
        package_path = os.path.join(app_dir, "package.json")
        with open(package_path, 'w') as f:
            f.write(f"""{{
  "name": "{app_name.lower().replace(' ', '-')}",
  "version": "1.0.0",
  "private": true,
  "description": "Generated by Str8ZeROCLI",
  "scripts": {{
    "start": "react-native start",
    "android": "react-native run-android",
    "ios": "react-native run-ios",
    "web": "cd web && npm start"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-native": "^0.71.7"
  }},
  "devDependencies": {{
    "@babel/core": "^7.21.4",
    "@babel/preset-env": "^7.21.4",
    "@babel/runtime": "^7.21.0",
    "metro-react-native-babel-preset": "^0.76.3"
  }}
}}""")
        generated_files.append(package_path)
        
        return generated_files
    
    def _generate_readme(self, app_name, app_type, features, platforms):
        """Generate README.md for the app"""
        features_list = ""
        if features:
            features_list = "\n".join([f"- {feature.replace('_', ' ').title()}" for feature in features])
        else:
            features_list = "- Basic functionality"
        
        platforms_list = "\n".join([f"- {platform.title()}" for platform in platforms])
        
        return f"""# {app_name}

Generated by Str8ZeROCLI - AI-powered app generator.

## Overview

This is a {app_type.replace('_', ' ')} app with the following features:

{features_list}

## Platforms

This app is available for:

{platforms_list}

## Getting Started

### Web

```bash
cd web
npm install
npm start
```

### iOS

```bash
cd ios
pod install
cd ..
npm run ios
```

### Android

```bash
npm run android
```

## License

This app is proprietary and confidential.
Copyright (c) {datetime.now().year} - All Rights Reserved.
"""

# Example usage
if __name__ == "__main__":
    generator = AppGenerator()
    result = generator.generate_app(
        "Bill Monitor Pro", 
        "bill_monitor", 
        ["bill_upload", "anomaly_detection", "auto_inquiry"],
        "all"
    )
    print(json.dumps(result, indent=2))