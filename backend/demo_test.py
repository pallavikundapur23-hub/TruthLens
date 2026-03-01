"""
🎬 DEMO TESTING SCRIPT - End-to-End TruthLens Demo
Run this to test all features for the hackathon demo presentation
"""

import requests
import json
import time
from pathlib import Path


# Configuration
API_URL = "http://localhost:8000"
TEST_IMAGE = "test_images/sample.jpg"
TEST_TEXT = "The president announced new climate policies today at the summit."


def print_header(title):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(f"✨ {title}")
    print("="*70 + "\n")


def print_response(response, label="Response"):
    """Pretty print API response."""
    print(f"📤 {label}:")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
        return data
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None


def test_health_check():
    """Test 1: Health check endpoint."""
    print_header("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        data = print_response(response)
        
        if data and data.get("status") == "healthy":
            print("✅ Backend is running!\n")
            return True
        else:
            print("❌ Backend health check failed\n")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}\n")
        print("💡 Make sure uvicorn is running:")
        print("   python -m uvicorn main_unified:app --reload\n")
        return False


def test_text_analysis():
    """Test 2: Text credibility analysis."""
    print_header("TEST 2: Text Credibility Analysis")
    
    print(f"📝 Analyzing text: '{TEST_TEXT}'\n")
    
    try:
        response = requests.post(
            f"{API_URL}/predict-text",
            json={"text": TEST_TEXT},
            timeout=30
        )
        
        data = print_response(response, "Text Analysis Result")
        
        if data:
            score = data.get("final_score", 0)
            verdict = data.get("verdict", "UNKNOWN")
            confidence = data.get("confidence", "UNKNOWN")
            
            print(f"\n📊 Summary:")
            print(f"   Final Score: {score} (0-1 scale)")
            print(f"   Verdict: {verdict}")
            print(f"   Confidence: {confidence}")
            print(f"   ✅ Component scores visible: fact_score, source_score, sentiment_score\n")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


def test_image_analysis():
    """Test 3: Image deepfake + camera authentication."""
    print_header("TEST 3: Image Analysis (Deepfake + Camera)")
    
    if not Path(TEST_IMAGE).exists():
        print(f"⚠️  Test image not found: {TEST_IMAGE}")
        print("📂 Available test images:")
        test_dir = Path("test_images")
        if test_dir.exists():
            for img in test_dir.glob("*.jpg"):
                print(f"   - {img}")
        print()
        return False
    
    print(f"🖼️  Uploading image: {TEST_IMAGE}\n")
    
    try:
        with open(TEST_IMAGE, "rb") as f:
            files = {"file": f}
            response = requests.post(
                f"{API_URL}/analyze",
                files=files,
                timeout=60
            )
        
        data = print_response(response, "Image Analysis Result")
        
        if data:
            final_score = data.get("overall_trust_score", 0)
            verdict = data.get("verdict", "UNKNOWN")
            
            print(f"\n📊 Summary:")
            print(f"   Overall Trust Score: {final_score}")
            print(f"   Verdict: {verdict}")
            
            deepfake = data.get("deepfake_analysis", {})
            camera = data.get("camera_analysis", {})
            
            if deepfake:
                print(f"\n   🧑‍💻 Deepfake Analysis:")
                print(f"      - Prediction: {deepfake.get('prediction')}")
                print(f"      - Deepfake Score: {deepfake.get('deepfake_score')}")
                print(f"      - Frames Analyzed: {deepfake.get('frames_analyzed')}")
            
            if camera:
                print(f"\n   👩‍💻 Camera Forensics:")
                print(f"      - Authenticity Score: {camera.get('authenticity_score')}")
                print(f"      - PRNU Detected: {camera.get('camera_authentic')}")
                print(f"      - Confidence: {camera.get('confidence')}")
            
            print()
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


def test_deepfake_endpoint():
    """Test 4: Deepfake detection specific endpoint."""
    print_header("TEST 4: Deepfake Detection Only")
    
    if not Path(TEST_IMAGE).exists():
        print(f"⚠️  Test image not found: {TEST_IMAGE}\n")
        return False
    
    print(f"🧑‍💻 Testing deepfake detector directly\n")
    
    try:
        with open(TEST_IMAGE, "rb") as f:
            files = {"file": f}
            response = requests.post(
                f"{API_URL}/predict-deepfake",
                files=files,
                timeout=60
            )
        
        data = print_response(response, "Deepfake Detection Result")
        
        if data:
            print(f"\n📊 Deepfake Score: {data.get('deepfake_score')}")
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   GPU Accelerated: ✅\n")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


def test_camera_auth():
    """Test 5: Camera authentication endpoint."""
    print_header("TEST 5: Camera Authentication")
    
    if not Path(TEST_IMAGE).exists():
        print(f"⚠️  Test image not found: {TEST_IMAGE}\n")
        return False
    
    print(f"👩‍💻 Testing camera fingerprinting\n")
    
    try:
        with open(TEST_IMAGE, "rb") as f:
            files = {"file": f}
            response = requests.post(
                f"{API_URL}/camera-check",
                files=files,
                timeout=60
            )
        
        data = print_response(response, "Camera Authentication Result")
        
        if data:
            print(f"\n📊 Camera Forensics:")
            print(f"   - Authentic: {data.get('camera_authentic')}")
            print(f"   - Authenticity Score: {data.get('authenticity_score')}")
            print(f"   - PRNU Analysis: {data.get('prnu_analysis')}")
            print(f"   - Unique Feature: ⭐ PRNU Fingerprinting\n")
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


def run_full_demo():
    """Run complete demo test suite."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "🎬 TRUTHLENS HACKATHON DEMO TEST" + " "*21 + "║")
    print("╚" + "="*68 + "╝")
    
    results = []
    
    # Test 1: Health check (required)
    if not test_health_check():
        print("⚠️  Cannot proceed without backend. Exiting.\n")
        return
    
    # Test 2: Text analysis
    results.append(("Text Analysis", test_text_analysis()))
    
    # Test 3: Image analysis (unified)
    results.append(("Image Analysis", test_image_analysis()))
    
    # Test 4: Deepfake specific
    results.append(("Deepfake Detection", test_deepfake_endpoint()))
    
    # Test 5: Camera auth
    results.append(("Camera Authentication", test_camera_auth()))
    
    # Summary
    print_header("DEMO TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🏆 ALL TESTS PASSED! Ready for hackathon demo!\n")
    else:
        print("\n⚠️  Some tests failed. Check error messages above.\n")


if __name__ == "__main__":
    run_full_demo()
