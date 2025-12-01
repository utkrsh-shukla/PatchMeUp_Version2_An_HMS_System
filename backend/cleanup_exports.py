#!/usr/bin/env python3
"""
Cleanup old export files (older than 24 hours)
Run this script periodically to clean up old CSV exports
"""

import os
import time
from datetime import datetime, timedelta

def cleanup_old_exports():
    """Remove export files older than 24 hours"""
    exports_dir = os.path.join(os.path.dirname(__file__), 'exports')
    
    if not os.path.exists(exports_dir):
        print("Exports directory doesn't exist")
        return
    
    # Files older than 24 hours
    cutoff_time = time.time() - (24 * 60 * 60)
    removed_count = 0
    
    for filename in os.listdir(exports_dir):
        if filename.endswith('.csv'):
            filepath = os.path.join(exports_dir, filename)
            file_time = os.path.getmtime(filepath)
            
            if file_time < cutoff_time:
                try:
                    os.remove(filepath)
                    removed_count += 1
                    print(f"Removed old export: {filename}")
                except Exception as e:
                    print(f"Error removing {filename}: {e}")
    
    print(f"Cleanup complete. Removed {removed_count} old export files.")

if __name__ == '__main__':
    cleanup_old_exports()