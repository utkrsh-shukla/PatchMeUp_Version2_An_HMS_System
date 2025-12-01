#!/usr/bin/env python3
"""
Hospital Management System - Setup Verification Script
This script verifies that all components are properly configured and running.
"""

import sys
import subprocess
import requests
import redis
import time
from app import create_app
from app.celery_config import celery_app

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_redis_connection():
    """Check Redis connection"""
    print("🔴 Checking Redis connection...")
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("   ✅ Redis connection - OK")
        return True
    except Exception as e:
        print(f"   ❌ Redis connection failed: {e}")
        print("   💡 Start Redis with: redis-server or start_redis.bat")
        return False

def check_flask_app():
    """Check Flask app configuration"""
    print("🌶️  Checking Flask app...")
    try:
        app = create_app()
        with app.app_context():
            print("   ✅ Flask app creation - OK")
            return True
    except Exception as e:
        print(f"   ❌ Flask app failed: {e}")
        return False

def check_celery_config():
    """Check Celery configuration"""
    print("🥬 Checking Celery configuration...")
    try:
        # Check if Celery app is configured
        if celery_app.conf.broker_url:
            print(f"   ✅ Celery broker: {celery_app.conf.broker_url}")
            return True
        else:
            print("   ❌ Celery broker not configured")
            return False
    except Exception as e:
        print(f"   ❌ Celery configuration failed: {e}")
        return False

def check_api_server():
    """Check if API server is running"""
    print("🌐 Checking API server...")
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("   ✅ API server - OK")
            return True
        else:
            print(f"   ❌ API server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ API server not running")
        print("   💡 Start with: python run.py")
        return False
    except Exception as e:
        print(f"   ❌ API server check failed: {e}")
        return False

def check_database():
    """Check database"""
    print("🗄️  Checking database...")
    try:
        app = create_app()
        with app.app_context():
            from app.models import User
            users = User.query.count()
            print(f"   ✅ Database - OK ({users} users found)")
            return True
    except Exception as e:
        print(f"   ❌ Database check failed: {e}")
        print("   💡 Initialize with: python init_db.py")
        return False

def main():
    """Main verification function"""
    print("=" * 60)
    print("🏥 Hospital Management System - Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        check_python_version(),
        check_redis_connection(),
        check_flask_app(),
        check_celery_config(),
        check_database(),
        check_api_server()
    ]
    
    print()
    print("=" * 60)
    
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"🎉 All checks passed! ({passed}/{total})")
        print()
        print("✅ Your system is ready!")
        print("📝 Next steps:")
        print("   1. Start Redis: start_redis.bat")
        print("   2. Start Celery: start_celery.bat")
        print("   3. Start Frontend: cd ../frontend && npm run dev")
        print()
        print("🌐 Access the application at: http://localhost:5173")
    else:
        print(f"❌ {total - passed} checks failed ({passed}/{total} passed)")
        print()
        print("🔧 Please fix the failed checks before proceeding.")
    
    print("=" * 60)

if __name__ == '__main__':
    main()