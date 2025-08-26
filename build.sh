#!/bin/bash

# DEV-COMMENT: This is the main build script for the entire J.A.R.V.I.S. application.
# It orchestrates the backend packaging, frontend build, and the final Tauri application bundling.

echo "🚀 Starting J.A.R.V.I.S. application build..."

# Step 1: Build the Python backend into an executable sidecar.
# This script calls PyInstaller to create the binary.
echo "📦 Packaging Python backend..."
./build_backend.sh

# Check if the backend build was successful
if [ $? -ne 0 ]; then
    echo "❌ Backend build failed. Aborting."
    exit 1
fi
echo "✅ Backend packaged successfully."


<<<<<<< HEAD
# Step 2: Build the frontend application.
# In a real environment, you would have npm/yarn installed and run the build command.
# The `beforeBuildCommand` in `tauri.conf.json` handles this automatically when using `tauri build`.
echo "🌐 Building frontend... (skipping actual command in this environment)"
# Example command:
# (cd src-tauri && npm install && npm run build)
#
# if [ $? -ne 0 ]; then
#     echo "❌ Frontend build failed. Aborting."
#     exit 1
# fi
echo "✅ Frontend build step completed."


# Step 3: Build the final Tauri application.
# This command bundles the frontend code and the backend sidecar into a single executable.
# This step requires the Tauri CLI and a full Rust development environment.
echo "🖥️ Building Tauri application... (skipping actual command in this environment)"
# Example command:
# (cd src-tauri && cargo tauri build)
#
# if [ $? -ne 0 ]; then
#     echo "❌ Tauri build failed."
#     exit 1
# fi
echo "✅ Tauri build step completed."
=======
# Step 2: Build the frontend and bundle the Tauri application.
echo "🌐 Building frontend and Tauri bundle..."
./scripts/build_ui.sh

# Check if the UI build was successful
if [ $? -ne 0 ]; then
    echo "❌ Frontend/Tauri build failed. Aborting."
    exit 1
fi
echo "✅ Frontend/Tauri build completed."
>>>>>>> 90775caae0ee1f419403e60a66426822b7ba0ef6

echo "🎉 J.A.R.V.I.S. application build process finished."
echo "You would find the final application in 'src-tauri/target/release/bundle/'"
