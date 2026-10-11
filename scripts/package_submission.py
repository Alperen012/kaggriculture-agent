#!/usr/bin/env python3
"""
Packaging script for Kaggle Kaggriculture submissions.
Packages src/main.py, LICENSE, and NOTICE into a clean tar.gz archive.
"""

import os
import tarfile
import sys

def package_submission(output_path=None):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_main = os.path.join(root_dir, "src", "main.py")
    license_file = os.path.join(root_dir, "LICENSE")
    notice_file = os.path.join(root_dir, "NOTICE")
    
    if output_path is None:
        submissions_dir = os.path.join(root_dir, "submissions")
        os.makedirs(submissions_dir, exist_ok=True)
        output_path = os.path.join(submissions_dir, "submission.tar.gz")

    if not os.path.exists(src_main):
        print(f"Error: {src_main} not found!", file=sys.stderr)
        sys.exit(1)

    print(f"Packaging {src_main} -> {output_path}...")
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(src_main, arcname="main.py")
        if os.path.exists(license_file):
            tar.add(license_file, arcname="LICENSE.txt")
        if os.path.exists(notice_file):
            tar.add(notice_file, arcname="NOTICE.txt")

    archive_size = os.path.getsize(output_path)
    print(f"Successfully packaged submission!")
    print(f"Output: {output_path} ({archive_size / 1024:.1f} KB)")
    
    with tarfile.open(output_path, "r:gz") as tar:
        print("\nArchive contents:")
        for member in tar.getmembers():
            print(f"  - {member.name} ({member.size:,} bytes)")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else None
    package_submission(out)
