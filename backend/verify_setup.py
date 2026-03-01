#!/usr/bin/env python
"""
TruthLens System Verification Script
Checks if all components are properly set up and connected
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """Verify Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {sys.version.split()[0]} installed")
    return True

def check_dependencies():
    """Verify all required dependencies are installed"""
    required = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'torch': 'PyTorch',
        'timm': 'timm (model hub)',
        'cv2': 'OpenCV',
        'PIL': 'Pillow',
    }
    
    all_installed = True
    for module, name in required.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Install with: pip install -r requirements.txt")
            all_installed = False
    
    return all_installed

def check_files():
    """Verify all required files exist"""
    required_files = {
        'main.py': 'Backend API',
        'model.py': 'Deep learning model',
        'requirements.txt': 'Dependencies',
        'frontend/truthlens.html': 'Frontend UI',
    }
    
    all_exist = True
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print(f"✅ {description} ({file_path})")
        else:
            print(f"❌ {description} ({file_path}) - NOT FOUND")
            all_exist = False
    
    return all_exist

def check_gpu():
    """Check if GPU is available"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU Available: {torch.cuda.get_device_name(0)}")
            return True
        else:
            print("⚠️  GPU not available (will use CPU - slower)")
            return True
    except:
        print("❌ PyTorch GPU check failed")
        return False

def check_model_loading():
    """Test if model can be loaded"""
    try:
        print("\n📦 Testing model loading (this may take a moment)...")
        from model import DeepfakeDemoModel
        detector = DeepfakeDemoModel()
        print("✅ Model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def check_backend_structure():
    """Verify backend app can be imported"""
    try:
        from main import app, detector
        print("✅ Backend app structure valid")
        print(f"   - FastAPI app: {app.title}")
        return True
    except Exception as e:
        print(f"❌ Backend structure check failed: {e}")
        return False

def main():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("   TruthLens System Verification")
    print("="*60 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Required Files", check_files),
        ("GPU Support", check_gpu),
        ("Backend Structure", check_backend_structure),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error during check: {e}")
            results.append((name, False))
    
    # Model loading is optional but recommended
    print(f"\n🔍 Checking Model Loading (Optional)...")
    try:
        check_model_loading()
    except Exception as e:
        print(f"⚠️  Model loading skipped (will load on first use)")
    
    # Summary
    print("\n" + "="*60)
    print("   VERIFICATION SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n" + "🎉 "*15)
        print("✅ ALL SYSTEMS GO!")
        print("🎉 "*15)
        print("\nYour TruthLens system is ready!")
        print("\nQuick start:")
        print("  1. Run: python main.py (or use START_SERVER script)")
        print("  2. Open: frontend/truthlens.html in your browser")
        print("  3. Upload an image and analyze it!")
        print("\nAPI Documentation: http://127.0.0.1:8000/docs")
        return 0
    else:
        print("\n" + "⚠️ "*15)
        print("❌ SOME CHECKS FAILED")
        print("⚠️ "*15)
        print("\nPlease fix the issues above before running the system.")
        print("\nCommon solutions:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Verify Python version: python --version")
        print("  - Check file paths are correct")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print()
    sys.exit(exit_code)
